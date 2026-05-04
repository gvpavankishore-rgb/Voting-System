import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# 🔴 Old tables remove cheyyadam (important)
c.execute("DROP TABLE IF EXISTS voters")
c.execute("DROP TABLE IF EXISTS parties")
c.execute("DROP TABLE IF EXISTS votes")

# ---------------- VOTERS TABLE ----------------
c.execute("""
CREATE TABLE voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,                -- 👈 NEW (important)
    voter_id TEXT UNIQUE,
    aadhar TEXT UNIQUE,
    has_voted INTEGER DEFAULT 0
)
""")

# ---------------- PARTIES TABLE ----------------
c.execute("""
CREATE TABLE parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    symbol TEXT
)
""")

# ---------------- VOTES TABLE ----------------
c.execute("""
CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voter_id INTEGER,
    party_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database setup completed ✅")