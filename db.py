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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER,
            predicted_department TEXT,
            correct_department TEXT,
            predicted_urgency TEXT,
            correct_urgency TEXT,
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
    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return complaint_id

def insert_feedback(complaint_id, predicted_department, correct_department, predicted_urgency, correct_urgency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (
            complaint_id,
            predicted_department,
            correct_department,
            predicted_urgency,
            correct_urgency,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            complaint_id,
            predicted_department,
            correct_department,
            predicted_urgency,
            correct_urgency,
            datetime.now(IST).isoformat()
        )
    )
    conn.commit()
    conn.close()

def get_all_complaints():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM complaints ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    complaints = [dict(row) for row in rows]
    conn.close()
    
    return complaints

def get_all_feedback():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM feedback ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    feedback = [dict(row) for row in rows]
    conn.close()
    
    return feedback

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")