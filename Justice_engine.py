# justice_engine.py
# Sigma Justice Engine — integrity watchdog + attestation
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import os, json, hmac, hashlib, base64

import requests
from flask import Blueprint, jsonify, current_app, request

UTC = timezone.utc
now = lambda: datetime.now(UTC)
iso = lambda dt: dt.replace(microsecond=0).isoformat().replace("+00:00","Z")

# ----- helpers --------------------------------------------------------------
def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _sign(payload: Dict[str, Any], secret: str) -> str:
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    sig = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    return _b64url(body) + "." + _b64url(sig)

def _get_env_json(name: str, default: Dict[str, Any]) -> Dict[str, Any]:
    try:
        raw = os.getenv(name, "")
        return json.loads(raw) if raw else default
    except Exception:
        return default

# ----- core --------------------------------------------------------------
@dataclass
class WatchdogConfig:
    node_id: str
    service_urls: Dict[str, str]
    tokens: Dict[str, str]
    pkas_verify_path: str = "/attestation/chain"
    cl_tip_path: str = "/ledger/tip"
    mos_metrics_path: str = "/metrics/summary"
    sync_publish_path: str = "/sync/publish"
    jet_recent_path: str = "/jet/recent"
    timeout_s: int = 4

class IntegrityWatchdog:
    def __init__(self, cfg: WatchdogConfig):
        self.cfg = cfg
        self.started_at = now()
        self.last_ok: Dict[str, Optional[datetime]] = {k: None for k in cfg.service_urls}

    def _hdr(self, svc: str) -> Dict[str, str]:
        tok = self.cfg.tokens.get(svc)
        return {"Authorization": f"Bearer {tok}"} if tok else {}

    def _ping_health(self, base: str, svc: str) -> Dict[str, Any]:
        try:
            r = requests.get(base.rstrip("/") + "/health", headers=self._hdr(svc), timeout=self.cfg.timeout_s)
            ok = r.ok
            if ok: self.last_ok[svc] = now()
            return {"ok": ok, "code": r.status_code, "body": (r.json() if r.headers.get("content-type","").startswith("application/json") else None)}
        except Exception as e:
            return {"ok": False, "err": str(e)}

    def _get_json(self, base: str, path: str, svc: str) -> Dict[str, Any]:
        try:
            r = requests.get(base.rstrip("/") + path, headers=self._hdr(svc), timeout=self.cfg.timeout_s)
            return r.json() if r.ok else {"_error": f"{r.status_code}"}
        except Exception as e:
            return {"_error": str(e)}

    def sample(self) -> Dict[str, Any]:
        urls = self.cfg.service_urls
        # 1) health checks
        health = {svc: self._ping_health(url, svc) for svc, url in urls.items()}
        up_count = sum(1 for v in health.values() if v.get("ok"))
        # 2) key subsystem snapshots (best-effort)
        pkas = self._get_json(urls.get("PKAS",""), self.cfg.pkas_verify_path, "PKAS") if urls.get("PKAS") else {}
        cl   = self._get_json(urls.get("CL",""),   self.cfg.cl_tip_path,   "CL")   if urls.get("CL") else {}
        mos  = self._get_json(urls.get("MOS",""),  self.cfg.mos_metrics_path,"MOS") if urls.get("MOS") else {}
        # 3) score (simple, transparent)
        score = round(min(1.0, 0.5*(up_count/max(1,len(urls))) + 0.5*(1.0 if (pkas.get("status")=="verified" or pkas.get("status")=="ok") else 0.0)), 3)
        # 4) attestation
        secret = os.getenv("JUSTICE_SECRET", "change-me")
        payload = {
            "node_id": self.cfg.node_id,
            "ts": int(now().timestamp()),
            "up": up_count,
            "n": len(urls),
            "score": score,
            "pkas_status": pkas.get("status","unknown"),
            "ledger_tip": cl.get("tip_hash") or cl.get("hash") or "—",
        }
        proof = _sign(payload, secret)

        return {
            "status": "ok",
            "node_id": self.cfg.node_id,
            "started_at": iso(self.started_at),
            "sampled_at": iso(now()),
            "integrity_score": score,
            "health": health,
            "pkas": pkas,
            "ledger": cl,
            "mos": mos,
            "attestation_proof": proof,
        }

# ----- Flask wiring ------------------------------------------------------
def create_blueprint(watchdog: IntegrityWatchdog) -> Blueprint:
    bp = Blueprint("justice_engine", __name__)

    @bp.get("/check")
    def check():
        snap = watchdog.sample()
        return jsonify(snap), 200

    @bp.post("/attest")
    def attest():
        note = (request.json or {}).get("note","")
        snap = watchdog.sample()
        snap["note"] = note
        return jsonify(snap), 200

    @bp.get("/health")
    def health():
        return jsonify({"status":"ok","component":"justice-engine","time": iso(now())}), 200

    return bp

def init_watchdog_from_env() -> IntegrityWatchdog:
    # URLs
    service_urls = {
        "MOS":  os.getenv("MOS_URL","").strip(),
        "JET":  os.getenv("JET_URL","").strip(),
        "PKAS": os.getenv("PKAS_URL","").strip(),
        "CL":   os.getenv("CL_URL","").strip(),
        "SYNC": os.getenv("SYNC_URL","").strip(),
    }
    service_urls = {k:v for k,v in service_urls.items() if v}  # drop empty
    tokens = _get_env_json("SERVICE_TOKENS_JSON", {})
    node_id = os.getenv("NODE_ID","SIGMA-GRD")
    return IntegrityWatchdog(WatchdogConfig(node_id=node_id, service_urls=service_urls, tokens=tokens))
