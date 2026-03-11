from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DB_PATH = '/data/play_records.db'

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS play_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            video_title TEXT NOT NULL,
            video_url TEXT NOT NULL,
            play_time DATETIME NOT NULL,
            client_ip TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/play-records', methods=['GET'])
def get_play_records():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, video_id, video_title, video_url, play_time, client_ip
        FROM play_records
        ORDER BY play_time DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'video_id': row['video_id'],
            'video_title': row['video_title'],
            'video_url': row['video_url'],
            'play_time': row['play_time'],
            'client_ip': row['client_ip']
        })
    
    return jsonify(records)

@app.route('/api/play-records', methods=['POST'])
def add_play_record():
    data = request.get_json()
    
    video_id = data.get('video_id')
    video_title = data.get('video_title')
    video_url = data.get('video_url')
    
    if not video_id or not video_title or not video_url:
        return jsonify({'error': 'Missing required fields'}), 400
    
    client_ip = request.remote_addr
    play_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO play_records (video_id, video_title, video_url, play_time, client_ip)
        VALUES (?, ?, ?, ?, ?)
    ''', (video_id, video_title, video_url, play_time, client_ip))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': record_id,
        'video_id': video_id,
        'video_title': video_title,
        'video_url': video_url,
        'play_time': play_time,
        'client_ip': client_ip
    }), 201

@app.route('/api/videos', methods=['GET'])
def get_videos():
    video_data = [
        {
            'id': 1,
            'title': '示例视频 1 - MP4格式',
            'cover': 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=225&fit=crop',
            'duration': '10:30',
            'format': 'mp4',
            'url': 'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4',
            'description': '这是一个示例视频，展示了MP4格式的播放效果。',
            'date': '2024-01-15'
        },
        {
            'id': 2,
            'title': '示例视频 2 - WebM格式',
            'cover': 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44c?w=400&h=225&fit=crop',
            'duration': '08:45',
            'format': 'webm',
            'url': 'https://sample-videos.com/video123/webm/720/big_buck_bunny_720p_1mb.webm',
            'description': 'WebM格式的视频示例，支持高清播放。',
            'date': '2024-01-16'
        },
        {
            'id': 3,
            'title': '示例视频 3 - HLS拉流',
            'cover': 'https://images.unsplash.com/photo-1536240478700-b869070f9279?w=400&h=225&fit=crop',
            'duration': '15:20',
            'format': 'm3u8',
            'url': 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8',
            'description': 'HLS直播流测试视频，展示拉流播放功能。',
            'date': '2024-01-17'
        },
        {
            'id': 4,
            'title': '示例视频 4 - 高清测试',
            'cover': 'https://images.unsplash.com/photo-1516280440614-6697288d5d38?w=400&h=225&fit=crop',
            'duration': '12:10',
            'format': 'mp4',
            'url': 'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4',
            'description': '高清视频测试，检查播放质量和性能。',
            'date': '2024-01-18'
        },
        {
            'id': 5,
            'title': '示例视频 5 - 移动端优化',
            'cover': 'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=400&h=225&fit=crop',
            'duration': '06:30',
            'format': 'mp4',
            'url': 'https://sample-videos.com/video321/mp4/480/big_buck_bunny_480p_1mb.mp4',
            'description': '针对移动端优化的视频，适合手机观看。',
            'date': '2024-01-19'
        },
        {
            'id': 6,
            'title': '示例视频 6 - DASH拉流',
            'cover': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&h=225&fit=crop',
            'duration': '09:15',
            'format': 'dash',
            'url': 'https://dash.akamaized.net/envivio/EnvivioDash3/manifest.mpd',
            'description': 'DASH格式流媒体测试，展示自适应码率功能。',
            'date': '2024-01-20'
        }
    ]
    return jsonify(video_data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
