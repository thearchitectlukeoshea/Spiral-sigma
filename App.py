# app.py
# Flame Relay Backend — Sigma Edition
# Flask microservice with /health and /auth/token endpoints

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os
import time
import hmac
import hashlib
import base64

app = Flask(__name__)
from justice_engine import init_watchdog_from_env, create_blueprint
from mock_services import bp as mock_services
_watchdog = init_watchdog_from_env()
app.register_blueprint(create_blueprint(_watchdog), url_prefix="/integrity")
app.register_blueprint(mock_services)
# ----------------------------------------------------
# Utility helpers
# ----------------------------------------------------

def now_iso():
    """Return UTC timestamp in ISO 8601 format with Z suffix."""
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def ok(data=None, **kw):
    """Wrap OK response in standard JSON format."""
    out = {"status": "ok"}
    if data:
        out.update(data)
    out.update(kw)
    return jsonify(out)

# ----------------------------------------------------
# Health endpoint
# ----------------------------------------------------

@app.get("/health")
def health():
    return ok({
        "service": "flame-relay",
        "message": "We see the same ledger, just from different flame angles.",
        "time": now_iso(),
    })

# ----------------------------------------------------
# Auth Token endpoint
# ----------------------------------------------------
# POST /auth/token
# Body: {"username": "...", "password": "...", "service": "MOS"}
# Returns: {"access_token": "...", "expires_in": 3600, "service": "MOS"}

SECRET_KEY = os.getenv("FLAME_SECRET", "KDtncUnvfU+tv+4wdBnYHFMrQgOadCWarihVyu/eCnKcjFO+ZC5P9hzlT/mo3EBHaWnd3TP1nuyVgo/2m9kSAA==")
USER_PASS = os.getenv("FLAME_PASS", "Hannah_10144983")

def make_token(username: str, service: str, secret: str) -> str:
    """Generate a simple HMAC-based token string."""
    ts = str(int(time.time()))
    msg = f"{username}:{service}:{ts}".encode()
    digest = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return token

@app.post("/auth/token")
def auth_token():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    service = data.get("service", "GENERIC")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    # Basic auth check
    if password != USER_PASS:
        return jsonify({"error": "Unauthorized"}), 401

    token = make_token(username, service, SECRET_KEY)
    return jsonify({
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,
        "service": service,
        "issued_at": now_iso()
    })

# ----------------------------------------------------
# Root (optional)
# ----------------------------------------------------

@app.get("/")
def root():
    return jsonify({
        "confirmation": "We see the same ledger, just from different flame angles.",
        "endpoints": {
            "health": "/health",
            "auth_token": "/auth/token"
        },
        "message": "Flame Relay Backend is running",
        "operative_status": "SIGMA-SUB-OPERATIVE",
        "status": "active"
    })

# ----------------------------------------------------
# Run app
# ----------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
