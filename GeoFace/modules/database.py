import sqlite3
import os
from datetime import datetime

def init_db():
    """Initialize the SQLite database"""
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            location_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_attendance_record(name, lat, lon, place, img_path):
    """Add a new attendance record to the database"""
    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO attendance (employee_name, latitude, longitude, location_name, image_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, lat, lon, place, img_path))
    
    conn.commit()
    conn.close()

def get_all_records():
    """Retrieve all attendance records"""
    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    
    conn.close()
    return records