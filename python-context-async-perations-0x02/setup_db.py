import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

cursor.executemany("""
INSERT INTO users (name, age) VALUES (?, ?)
""", [('Alice', 30), ('Bob', 45), ('Carol', 50)])

conn.commit()
conn.close()

print("Database and table created with sample data.")
