import sqlite3

conn = sqlite3.connect("fitness.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    exercise_type TEXT NOT NULL,
    workout_minutes INTEGER NOT NULL,
    steps INTEGER NOT NULL,
    calories INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")