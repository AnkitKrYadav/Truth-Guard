from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="../Frontend/react-app/build", static_url_path="/")
CORS(app)  # Allow frontend to call API

DB_PATH = "database/news.db"  # Point to the database file

# --------- Database Helper ---------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB if not exists
def init_db():
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                source TEXT,
                summary TEXT
            )
        """)
        sample_news = [
            ("AI Chatbot Breakthrough Shakes Tech World", "Tech", "TechCrunch", "A new AI model revolutionizes chatbots."),
            ("Global Climate Summit: Key Takeaways", "Environment", "BBC", "Leaders discuss climate action strategies."),
            ("Health Tips: Benefits of Daily Meditation", "Health", "Healthline", "Meditation improves mental and physical health."),
            ("SpaceX Launches Starlink Satellites", "Science", "Space.com", "Starlink satellites launched into orbit successfully."),
            ("Political Debate Heats Up Ahead of Elections", "Politics", "CNN", "Debates on policies and candidates are ongoing.")
        ]
        c.executemany("INSERT INTO news (title, category, source, summary) VALUES (?, ?, ?, ?)", sample_news)
        conn.commit()
        conn.close()
        print("Database initialized with sample data!")

init_db()

# --------- API Routes ---------

@app.route("/api/trending")
def trending():
    conn = get_db_connection()
    news = conn.execute("SELECT * FROM news").fetchall()
    conn.close()
    return jsonify([dict(n) for n in news])

@app.route("/api/categories")
def categories():
    conn = get_db_connection()
    cats = conn.execute("SELECT DISTINCT category FROM news").fetchall()
    conn.close()
    category_list = ["All"] + [c["category"] for c in cats]
    return jsonify(category_list)

# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# --------- Run Server ---------
if __name__ == "__main__":
    app.run(debug=True)
