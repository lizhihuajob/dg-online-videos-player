from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

DATABASE = 'playback_history.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    max_retries = 5
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playback_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    name TEXT,
                    format TEXT DEFAULT 'mp4',
                    is_local BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            print("数据库初始化完成")
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                print(f"数据库被锁定，等待重试... ({attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise


@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, url, name, format, is_local, created_at
            FROM playback_history
            ORDER BY created_at DESC
            LIMIT 50
        ''')
        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'url': row['url'],
                'name': row['name'],
                'format': row['format'],
                'isLocal': bool(row['is_local']),
                'timestamp': row['created_at']
            })

        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/history', methods=['POST'])
def add_history():
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'message': '缺少必需的 url 字段'
            }), 400

        url = data['url']
        name = data.get('name', '')
        format_type = data.get('format', 'mp4')
        is_local = data.get('isLocal', False)

        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查是否已存在相同的 URL
        cursor.execute('SELECT id FROM playback_history WHERE url = ?', (url,))
        existing = cursor.fetchone()

        if existing:
            # 更新现有记录的时间戳
            cursor.execute('''
                UPDATE playback_history
                SET created_at = CURRENT_TIMESTAMP, name = ?, format = ?
                WHERE url = ?
            ''', (name, format_type, url))
        else:
            # 插入新记录
            cursor.execute('''
                INSERT INTO playback_history (url, name, format, is_local)
                VALUES (?, ?, ?, ?)
            ''', (url, name, format_type, 1 if is_local else 0))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': '播放记录已保存'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/history/<int:history_id>', methods=['DELETE'])
def delete_history_item(history_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM playback_history WHERE id = ?', (history_id,))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': '播放记录已删除'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/history/clear', methods=['DELETE'])
def clear_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM playback_history')
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': '所有播放记录已清除'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': '服务运行正常'
    })


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
