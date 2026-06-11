# Backend

FastAPI backend scaffold for the waybill-driven reporting platform.

## Local run

```powershell
cd backend
python -m venv .venv
..\.venv\Scripts\python -m pip install -r requirements.txt
..\.venv\Scripts\python -m uvicorn app.main:app --reload
```

OpenAPI is available at `http://127.0.0.1:8000/docs`.

The first scaffold uses an in-memory store so the API can start before MySQL
persistence is implemented.
