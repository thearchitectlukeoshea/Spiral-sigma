# mock_services.py
# Minimal placeholder endpoints for MOS, PKAS, CL, JET, and SYNC
from flask import Blueprint, jsonify
from datetime import datetime, timezone

bp = Blueprint("mock_services", __name__)

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

@bp.get("/metrics/summary")
def metrics_summary():
    return jsonify({
        "service": "MOS",
        "status": "ok",
        "uptime": "stable",
        "timestamp": now_iso()
    })

@bp.get("/attestation/chain")
def attestation_chain():
    return jsonify({
        "service": "PKAS",
        "status": "verified",
        "chain_depth": 3,
        "timestamp": now_iso()
    })

@bp.get("/ledger/tip")
def ledger_tip():
    return jsonify({
        "service": "CL",
        "tip_hash": "abcd1234efgh5678",
        "height": 42,
        "timestamp": now_iso()
    })

@bp.get("/jet/recent")
def jet_recent():
    return jsonify({
        "service": "JET",
        "last_emission": "ok",
        "timestamp": now_iso()
    })

@bp.get("/sync/publish")
def sync_publish():
    return jsonify({
        "service": "SYNC",
        "status": "synced",
        "timestamp": now_iso()
    })
