import sqlite3

# Connect to SQLite DB (creates if not exists)
conn = sqlite3.connect("news.db")
c = conn.cursor()

# Create table for news
c.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    source TEXT,
    summary TEXT
)
""")

# Insert some sample data (run only once)
sample_news = [
    ("AI Chatbot Breakthrough Shakes Tech World", "Tech", "TechCrunch", "A new AI model revolutionizes chatbots."),
    ("Global Climate Summit: Key Takeaways", "Environment", "BBC", "Leaders discuss climate action strategies."),
    ("Health Tips: Benefits of Daily Meditation", "Health", "Healthline", "Meditation improves mental and physical health."),
    ("SpaceX Launches Starlink Satellites", "Science", "Space.com", "Starlink satellites launched into orbit successfully.")
]

# Insert sample news
c.executemany("INSERT INTO news (title, category, source, summary) VALUES (?, ?, ?, ?)", sample_news)

conn.commit()
conn.close()

print("Database created and sample data inserted!")
