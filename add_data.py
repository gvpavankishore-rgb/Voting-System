import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Clear old data
c.execute("DELETE FROM parties")

# Insert parties (correct way)
c.execute("INSERT INTO parties (name, symbol) VALUES (?, ?)", ("BJP", "/static/BJP.png"))
c.execute("INSERT INTO parties (name, symbol) VALUES (?, ?)", ("Janasena", "/static/JSP.png"))
c.execute("INSERT INTO parties (name, symbol) VALUES (?, ?)", ("TDP", "/static/TDP.png"))
c.execute("INSERT INTO parties (name, symbol) VALUES (?, ?)", ("YSRCP", "/static/YSRCP.png"))

conn.commit()
conn.close()

print("Parties added ✅")