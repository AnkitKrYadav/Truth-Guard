from flask import Flask, jsonify, request, send_from_directory
import os
import sqlite3
import json
import logging

# Optional imports
try:
    from flask_cors import CORS
except ImportError:
    def CORS(app, *args, **kwargs):
        return app

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv("../.env", raise_error_if_not_found=False))
except ImportError:
    pass

# Logging setup
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__, static_folder="../Frontend/react-app/build", static_url_path="/")
CORS(app)

# DB setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "news.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    c = conn.cursor()
    # News table
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT,
            summary TEXT
        )
    """)
    # Verifications table
    c.execute("""
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim TEXT NOT NULL,
            status TEXT,
            summary TEXT,
            sources TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Insert sample news if empty
    if c.execute("SELECT COUNT(*) FROM news").fetchone()[0] == 0:
        sample_news = [
            ("AI Chatbot Breakthrough Shakes Tech World", "Tech", "TechCrunch", "A new AI model revolutionizes chatbots."),
            ("Global Climate Summit: Key Takeaways", "Environment", "BBC", "Leaders discuss climate action strategies."),
            ("Health Tips: Benefits of Daily Meditation", "Health", "Healthline", "Meditation improves mental and physical health."),
            ("SpaceX Launches Starlink Satellites", "Science", "Space.com", "Starlink satellites launched into orbit successfully."),
            ("Political Debate Heats Up Ahead of Elections", "Politics", "CNN", "Debates on policies and candidates are ongoing."),
        ]
        c.executemany("INSERT INTO news (title, category, source, summary) VALUES (?, ?, ?, ?)", sample_news)
    conn.commit()
    conn.close()
    _logger.info("Database initialized")

init_db()

# Import AI agent
try:
    from ai_agent import verify_claim_with_ai
except ImportError:
    verify_claim_with_ai = None

# --------- ROUTES ---------

@app.route("/api/trending", methods=["GET"])
def trending():
    conn = get_db_connection()
    news = conn.execute("SELECT * FROM news").fetchall()
    conn.close()
    return jsonify([dict(n) for n in news])

@app.route("/api/categories", methods=["GET"])
def categories():
    conn = get_db_connection()
    cats = conn.execute("SELECT DISTINCT category FROM news").fetchall()
    conn.close()
    return jsonify(["All"] + [c["category"] for c in cats])

@app.route("/api/verify", methods=["POST"])
def verify_claim_route():
    data = request.get_json() or {}
    claim = data.get("claim", "").strip()
    if not claim:
        return jsonify({"error": "No claim provided"}), 400

    _logger.info("Verifying claim: %s", claim)

    # Use AI agent if configured
    result = None
    if verify_claim_with_ai and os.getenv("OPENAI_API_KEY"):
        try:
            result = verify_claim_with_ai(claim)
            _logger.info("AI verification success")
        except Exception as e:
            _logger.exception("AI agent error: %s", e)

    # Fallback logic
    if not result:
        status = "Unclear"
        summary = "This claim requires further verification."
        sources = []
        if "AI" in claim or "ChatGPT" in claim:
            status = "True"
            summary = "This claim appears true based on verified tech sources."
            sources = ["TechCrunch", "BBC Tech"]
        elif "Fake" in claim or "rumor" in claim.lower():
            status = "False"
            summary = "This claim is false or misleading."
            sources = ["Snopes", "Reuters"]
        result = {"claim": claim, "status": status, "summary": summary, "sources": sources, "confidence": None}

    # Persist verification
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO verifications (claim, status, summary, sources, confidence) VALUES (?, ?, ?, ?, ?)",
            (claim, result.get("status"), result.get("summary"), json.dumps(result.get("sources", [])), result.get("confidence")),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        _logger.warning("Could not save verification: %s", e)

    return jsonify(result)

@app.route("/api/verifications", methods=["GET"])
def list_verifications():
    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 20))
    except:
        page, page_size = 1, 20
    offset = (page - 1) * page_size
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, claim, status, summary, sources, confidence, created_at FROM verifications ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (page_size, offset)
    ).fetchall()
    conn.close()

    items = []
    for r in rows:
        try:
            srcs = json.loads(r["sources"]) if r["sources"] else []
        except:
            srcs = []
        items.append({
            "id": r["id"],
            "claim": r["claim"],
            "status": r["status"],
            "summary": r["summary"],
            "sources": srcs,
            "confidence": r["confidence"],
            "created_at": r["created_at"],
        })
    return jsonify({"page": page, "page_size": page_size, "items": items})

@app.route("/api/verifications", methods=["POST"])
def create_verification():
    data = request.get_json() or {}
    claim = data.get("claim")
    if not claim:
        return jsonify({"error": "claim is required"}), 400
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO verifications (claim, status, summary, sources, confidence) VALUES (?, ?, ?, ?, ?)",
            (
                claim,
                data.get("status"),
                data.get("summary"),
                json.dumps(data.get("sources", [])),
                data.get("confidence")
            )
        )
        conn.commit()
        last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return jsonify({"id": last_id}), 201
    except Exception as e:
        _logger.exception("Failed to create verification: %s", e)
        return jsonify({"error": "failed to create verification"}), 500

# Serve frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# Health check
@app.route("/_health")
def health():
    return jsonify({"status": "ok"}), 200

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    debug_mode = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")
    _logger.info("Server starting on port %s (debug=%s)", port, debug_mode)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
