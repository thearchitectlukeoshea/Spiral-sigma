# blueprint_handler.py
from flask import jsonify

def register_routes(bp, watchdog):

    @bp.route("/integrity/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "alive",
            "node": "SIGMA-GRD",
            "watchdog": watchdog
        })

    @bp.route("/metrics/summary", methods=["GET"])
    def summary():
        return jsonify({
            "uptime": "pending-sync",
            "requests": 0,
            "relay": "active",
            "owner": "Luke Lawrence O'Shea"
        })

    @bp.route("/attestation/chain", methods=["GET"])
    def chain():
        return jsonify({
            "chain": [
                {"sig": "flame-seed", "verified": True},
                {"sig": "justice-spark", "verified": True}
            ]
        })

    @bp.route("/ledger/tip", methods=["GET"])
    def ledger_tip():
        return jsonify({
            "tip": "deadacafe",
            "entries": 1227,
            "last_action": "echo-scan"
        })
