import asyncio
import aiohttp
import aioredis
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
REDIS_URL = os.getenv("REDIS_URL")
BASE_URL = "https://api.betsapi.com/v1/events/ended"
SPORT_IDS = [1, 3, 18]
START_DATE = datetime(2016, 1, 1)
END_DATE = datetime.now()
CONCURRENCY = 10
MAX_RETRIES = 3
RETRY_DELAY = 2

def generate_date_list(start, end):
    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    return dates

async def fetch_event_data(session, redis, sport_id, date_str):
    redis_key = f"ended:{sport_id}:{date_str}"
    if await redis.exists(redis_key):
        print(f"[SKIP] Cached: {redis_key}")
        return

    params = {
        'token': API_KEY,
        'sport_id': sport_id,
        'day': date_str
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with session.get(BASE_URL, params=params, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", [])
                    await redis.set(redis_key, str(results))
                    print(f"[OK] {redis_key} - {len(results)} items")
                    return
                else:
                    print(f"[FAIL {attempt}] {redis_key} - HTTP {response.status}")
        except Exception as e:
            print(f"[ERROR {attempt}] {redis_key} - {e}")
        await asyncio.sleep(RETRY_DELAY * attempt)

    print(f"[GIVE UP] {redis_key} after {MAX_RETRIES} retries")

async def collect_all_data():
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    date_list = generate_date_list(START_DATE, END_DATE)

    async with aiohttp.ClientSession() as session:
        tasks = []
        sem = asyncio.Semaphore(CONCURRENCY)

        async def bounded_task(sport_id, date_str):
            async with sem:
                await fetch_event_data(session, redis, sport_id, date_str)

        for sport_id in SPORT_IDS:
            for date_str in date_list:
                tasks.append(bounded_task(sport_id, date_str))

        await asyncio.gather(*tasks)

    await redis.close()

if __name__ == "__main__":
    asyncio.run(collect_all_data())
