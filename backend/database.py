import sqlite3
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'playback_history.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playback_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT NOT NULL UNIQUE,
            video_name TEXT,
            video_format TEXT DEFAULT 'mp4',
            last_position REAL DEFAULT 0,
            play_count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_video_url ON playback_history(video_url)
    ''')
    conn.commit()
    conn.close()

def add_playback_record(video_url, video_name='', video_format='mp4', last_position=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, play_count FROM playback_history WHERE video_url = ?
    ''', (video_url,))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE playback_history 
            SET video_name = ?, video_format = ?, last_position = ?, 
                play_count = play_count + 1, updated_at = ?
            WHERE video_url = ?
        ''', (video_name, video_format, last_position, datetime.now(), video_url))
    else:
        cursor.execute('''
            INSERT INTO playback_history (video_url, video_name, video_format, last_position, play_count)
            VALUES (?, ?, ?, ?, 1)
        ''', (video_url, video_name, video_format, last_position))
    
    conn.commit()
    conn.close()

def get_all_playback_records(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM playback_history 
        ORDER BY updated_at DESC 
        LIMIT ?
    ''', (limit,))
    records = cursor.fetchall()
    conn.close()
    return [dict(row) for row in records]

def delete_playback_record(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM playback_history WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def clear_all_playback_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM playback_history')
    conn.commit()
    conn.close()

def update_playback_position(video_url, last_position):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE playback_history 
        SET last_position = ?, updated_at = ?
        WHERE video_url = ?
    ''', (last_position, datetime.now(), video_url))
    conn.commit()
    conn.close()
