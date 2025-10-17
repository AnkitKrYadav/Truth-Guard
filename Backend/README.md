# Truth-Guard Backend (Flask)

This document explains how to run and deploy the backend for Truth-Guard.

## Quick start (local)

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
# then edit .env to add your keys (OPENAI_API_KEY, etc.)
```

4. Run the server (dev):

```powershell
$env:DEBUG = 'True'; python app.py
```

## Health check

The app exposes a simple health endpoint:

```
GET /_health -> {"status":"ok"}
```

PowerShell example:

```powershell
Invoke-RestMethod http://127.0.0.1:10000/_health
```

## Production (Render) checklist

1. Build the frontend and make the `Frontend/react-app/build` folder available to the backend. If you will serve the frontend from the backend (recommended single-origin deployment), build the frontend and copy the `build` folder into `Frontend/react-app/build` on the server.

2. Environment variables to set in production:

- `OPENAI_API_KEY` (optional) — enable AI verification
- `NEWS_API_KEY` (optional)
- `FACTCHECK_API_KEY` (optional)
- `DEBUG=false`

3. Procfile (Render/Heroku):

```
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

4. Deploy steps (Render):

- Create a new web service and point it to this repository.
- Set Build Command (if needed): `pip install -r Backend/requirements.txt` (Render typically auto-detects Python)
- Set Start Command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
- Add environment variables (OPENAI_API_KEY etc.) via the Render dashboard.

5. Verify the deployment:

- Visit `https://<your-app>.onrender.com/_health` and confirm `{"status":"ok"}`.

## Notes

- If `OPENAI_API_KEY` is not set, `/api/verify` will still work using a fallback heuristic, but results will be less precise.
- The backend serves the static frontend from `../Frontend/react-app/build` when present.
- The SQLite DB is created under `Backend/database/news.db` and seeded with sample data if empty.

## Troubleshooting

- If the app fails to start on Render due to missing packages, ensure `requirements.txt` in `Backend/` is correct and includes `gunicorn`.
- Use the Render logs to inspect runtime errors and stack traces.

## Useful commands (PowerShell)

```powershell
# Build frontend (from repo root)
cd Frontend/react-app
# on Windows PowerShell
$env:REACT_APP_API_BASE = 'https://<your-backend>' ; npm run build
``` 

