# Backend (FastAPI)

## Quickstart
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env  # 필요 시 수정
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/api/v1/docs
- Health:  http://localhost:8000/api/v1/health
