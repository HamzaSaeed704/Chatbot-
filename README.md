# Eliza-like Chatbot (Python + React)

This project contains:
- `backend/`: Flask API with an Eliza-style chatbot using **55 regex rules**.
- `frontend/`: React (Vite) chat UI that calls the backend.

## Backend Setup

```bash
cd backend
python -m venv ../.venv
../.venv/bin/python -m pip install -r requirements.txt
../.venv/bin/python app.py
```

Backend runs at `http://localhost:5001` by default.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

The Vite dev server proxies `/api/*` to `http://localhost:5001`, so chat requests hit the Flask backend without extra config.

## API

- `GET /api/health`
- `POST /api/chat`

Example:

```json
{
  "message": "I feel anxious about exams"
}
```

Response:

```json
{
  "response": "When do you feel most anxious?"
}
```
