from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, add_playback_record, get_all_playback_records, delete_playback_record, clear_all_playback_records, update_playback_position

app = Flask(__name__)
CORS(app)

@app.before_request
def initialize():
    init_db()

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        limit = request.args.get('limit', 20, type=int)
        records = get_all_playback_records(limit)
        return jsonify({
            'success': True,
            'data': records
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['POST'])
def add_history():
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        video_name = data.get('video_name', '')
        video_format = data.get('video_format', 'mp4')
        last_position = data.get('last_position', 0)
        
        if not video_url:
            return jsonify({
                'success': False,
                'error': 'video_url is required'
            }), 400
        
        add_playback_record(video_url, video_name, video_format, last_position)
        
        return jsonify({
            'success': True,
            'message': 'Playback record added successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_history(record_id):
    try:
        delete_playback_record(record_id)
        return jsonify({
            'success': True,
            'message': 'Playback record deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    try:
        clear_all_playback_records()
        return jsonify({
            'success': True,
            'message': 'All playback records cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/position', methods=['PUT'])
def update_position():
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        last_position = data.get('last_position', 0)
        
        if not video_url:
            return jsonify({
                'success': False,
                'error': 'video_url is required'
            }), 400
        
        update_playback_position(video_url, last_position)
        
        return jsonify({
            'success': True,
            'message': 'Playback position updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
