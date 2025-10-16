from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__, static_folder="../Frontend/react-app/build", static_url_path="/")
CORS(app)

# Use deterministic DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "news.db")


# --------- DATABASE SETUP ---------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT,
            summary TEXT
        )
        """
    )

    existing = c.execute("SELECT COUNT(*) as cnt FROM news").fetchone()[0]
    if existing == 0:
        sample_news = [
            ("AI Chatbot Breakthrough Shakes Tech World", "Tech", "TechCrunch", "A new AI model revolutionizes chatbots."),
            ("Global Climate Summit: Key Takeaways", "Environment", "BBC", "Leaders discuss climate action strategies."),
            ("Health Tips: Benefits of Daily Meditation", "Health", "Healthline", "Meditation improves mental and physical health."),
            ("SpaceX Launches Starlink Satellites", "Science", "Space.com", "Starlink satellites launched into orbit successfully."),
            ("Political Debate Heats Up Ahead of Elections", "Politics", "CNN", "Debates on policies and candidates are ongoing."),
        ]
        c.executemany("INSERT INTO news (title, category, source, summary) VALUES (?, ?, ?, ?)", sample_news)
        conn.commit()
        print("✅ Database initialized with sample data!")
    conn.close()


init_db()


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
    category_list = ["All"] + [c["category"] for c in cats]
    return jsonify(category_list)


# --------- AI VERIFICATION ---------
try:
    from ai_agent import verify_claim_with_ai
except Exception:
    verify_claim_with_ai = None


@app.route("/api/verify", methods=["POST"])
def verify_claim_route():
    data = request.get_json()
    claim = data.get("claim", "")
    print("🟢 Received claim:", claim)

    if not claim:
        return jsonify({"error": "No claim provided"}), 400

    # Use AI agent if available
    if verify_claim_with_ai and os.getenv("OPENAI_API_KEY"):
        try:
            result = verify_claim_with_ai(claim)
            print("✅ AI Verification result:", result)
            return jsonify(result)
        except Exception as e:
            print("❌ AI agent error:", e)

    # Fallback simple logic
    verified_status = "Unclear"
    summary = "This claim requires further verification."
    sources = []

    if "AI" in claim or "ChatGPT" in claim:
        verified_status = "True"
        summary = "This claim appears true based on verified tech sources."
        sources = ["TechCrunch", "BBC Tech"]
    elif "Fake" in claim or "rumor" in claim.lower():
        verified_status = "False"
        summary = "This claim is false or misleading."
        sources = ["Snopes", "Reuters"]

    result = {"claim": claim, "status": verified_status, "summary": summary, "sources": sources}
    print("⚙️ Fallback verification result:", result)
    return jsonify(result)


# --------- SERVE FRONTEND ---------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# --------- RUN SERVER ---------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
