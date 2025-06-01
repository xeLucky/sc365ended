# 🏟️ BetsAPI Ended Events Collector (Async + Redis)

이 프로젝트는 [BetsAPI](https://betsapi.com/)의 "Ended Events" 데이터를 2016년부터 현재까지 **비동기 방식으로 병렬 수집하고**, Redis에 캐싱하는 Python 스크립트입니다.

- ⚡ `asyncio` + `aiohttp` 기반 고속 병렬 수집
- 🧠 Redis를 활용한 캐싱 및 중복 수집 방지
- 🔁 네트워크/응답 실패 시 자동 재시도 기능 포함
- 🗂️ 일별, 종목별 데이터 저장 구조 (`ended:{sport_id}:{date}`)

---

## 📦 설치 방법

```bash
git clone https://github.com/xeLucky/sc365ended.git
cd sc365ended
pip install -r requirements.txt
```

---

## ⚙️ 환경 변수 설정

루트 디렉토리에 `.env` 파일을 생성하고 아래 항목을 입력하세요.

```env
API_KEY=YOUR_BETSAPI_API_KEY
REDIS_URL=redis://localhost:6379
```

---

## 🚀 실행 방법

```bash
python collect.py
```

자동으로 2016년부터 오늘까지, 설정한 스포츠 종목(sport_id)에 대해 데이터가 Redis에 저장됩니다.

---

## 🧰 주요 설정

| 설정 항목         | 설명                              |
|------------------|-----------------------------------|
| `SPORT_IDS`       | 수집할 스포츠 종목 ID 리스트       |
| `START_DATE`      | 수집 시작 날짜 (`datetime`)        |
| `END_DATE`        | 수집 종료 날짜 (`datetime`)        |
| `CONCURRENCY`     | 병렬 실행 개수 (`Semaphore`)       |
| `MAX_RETRIES`     | 요청 실패 시 최대 재시도 횟수       |
| `RETRY_DELAY`     | 재시도 시 대기 시간 (초)           |

---

## 🗃️ Redis 키 구조

- 키 형식: `ended:{sport_id}:{yyyy-mm-dd}`
- 값(Value): JSON 문자열로 직렬화된 `results` 배열

---

## 🛠 개발에 사용된 기술

- Python 3.8+
- [aiohttp](https://docs.aiohttp.org/)
- [aioredis](https://github.com/aio-libs/aioredis)
- [BetsAPI](https://betsapi.com/)
- asyncio, dotenv 등

---

## 📌 참고 사항

- **BetsAPI의 무료 플랜은 호출량 제한이 있습니다.** 과도한 요청은 429(Too Many Requests) 오류로 이어질 수 있으므로, `CONCURRENCY`를 적절히 조정하세요.
- 실제 서비스에 적용한 /DB 저장, 리그 필터링, 스케줄러 크론 연동 등은 제외하였습니다.

---

## 📄 라이선스

MIT License
