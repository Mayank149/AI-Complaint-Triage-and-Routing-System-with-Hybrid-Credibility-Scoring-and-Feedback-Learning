import sqlite3
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours = 5, minutes = 30))

DB_NAME = "complaints.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            predicted_department TEXT,
            department_confidence REAL,
            predicted_urgency TEXT,
            urgency_confidence REAL,
            credibility_score INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_complaint(text, predicted_department, department_confidence, predicted_urgency, urgency_confidence, credibility_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (
            text,
            predicted_department,
            department_confidence,
            predicted_urgency,
            urgency_confidence,
            credibility_score,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            text,
            predicted_department,
            department_confidence,
            predicted_urgency,
            urgency_confidence,
            credibility_score,
            datetime.now(IST).isoformat()
        )
    )
    conn.commit()
    conn.close()



if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")