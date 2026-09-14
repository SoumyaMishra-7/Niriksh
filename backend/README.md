# Niriksh Intelligence Backend

FastAPI service for deterministic edge-intelligence demos. It stores operational metadata only—never faces, biometric embeddings, raw video, persistent visitor IDs, or cross-store identities.

```bash
cd backend
python -m pip install -r requirements.txt
python -m app.db.seed
uvicorn app.main:app --reload
```

Swagger: `http://localhost:8000/docs`. Use `POST /api/v1/demo/start`, `/demo/stop`, `/demo/reset`, and `/demo/connectivity`. Live events: `ws://localhost:8000/ws/stores/store-hyd`. Run tests with `pytest`.
