from flask import jsonify
import psutil, time

@app.route("/metrics/summary", methods=["GET"])
def metrics_summary():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "timestamp": time.time()
    })

@app.route("/ledger/tip", methods=["GET"])
def ledger_tip():
    return jsonify({
        "tip": "SIGMA Ledger Hash: 1ae3...42fd (mocked)",
        "timestamp": time.time()
    })

@app.route("/integrity/health", methods=["GET"])
def integrity_health():
    return jsonify({
        "relay": "operational",
        "nodes_online": 1,
        "flame_status": "green",
        "timestamp": time.time()
    })
