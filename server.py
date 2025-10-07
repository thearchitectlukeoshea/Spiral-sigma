
from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)
LOG_FILE = 'relay_log.json'

@app.route('/ping', methods=['POST'])
def ping():
    data = request.get_json()
    data['received_at'] = int(time.time())
    try:
        with open(LOG_FILE, 'a') as f:
            json.dump(data, f)
            f.write('\n')
        return jsonify({'status': 'success', 'logged': data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/log', methods=['GET'])
def log():
    try:
        with open(LOG_FILE, 'r') as f:
            entries = [json.loads(line) for line in f if line.strip()]
        return jsonify(entries), 200
    except FileNotFoundError:
        return jsonify([]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
