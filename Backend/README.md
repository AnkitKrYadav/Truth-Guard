# Backend (Flask)

Quick steps to run the backend locally.

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set values (if you want AI support):

```powershell
copy .env.example .env
# then edit .env to add your keys
```

Required keys:

- `GEMINI_API_KEY` – Google AI Studio API key for Gemini
- `GEMINI_MODEL` – optional (defaults to `gemini-2.5-flash`)
- `NEWS_API_KEY` – optional, enables richer source results
- `FACTCHECK_API_KEY` – optional, enables Google Fact Check lookups

4. Run the server:

```powershell
python app.py
```

Notes:
- The API serves the built React frontend from `../Frontend/react-app/build` when available.
- `/api/verify` will use a minimal AI agent if `GEMINI_API_KEY` is set. Otherwise it falls back to simple placeholder logic.
- The SQLite DB is created under `Backend/database/news.db` and seeded with sample data if empty.
