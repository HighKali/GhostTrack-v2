import json
import pathlib
from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "webapp" / "static"
CONFIG_PATH = STATIC_DIR / "config.json"

app = Flask(
    __name__,
    static_folder=str(STATIC_DIR),
    static_url_path=""
)

CORS(app)


def load_config():
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/api/status")
def status():
    cfg = load_config()
    return jsonify({
        "status": "ok",
        "service": "GhostTrack WebApp",
        "version": cfg.get("version", "3.0"),
        "environment": cfg.get("environment", "production"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.route("/api/starlink/status")
def starlink_status():
    # Qui aggancerai la telemetria reale Starlink
    # Valori placeholder COERENTI e stabili, pronti da sostituire con dati veri
    data = {
        "latency_ms": 45,
        "download_mbps": 120,
        "upload_mbps": 20,
        "uptime_h": 5.5,
        "credits": 320,
        "mode": "normal"
    }
    return jsonify(data)


@app.route("/api/economist/summary")
def economist_summary():
    # Qui potrai calcolare i crediti da DB / serie storiche
    data = {
        "total_credits": 12450,
        "today_credits": 180,
        "starlink_bonus": 22
    }
    return jsonify(data)


@app.route("/api/wallet/summary")
def wallet_summary():
    # Qui potrai collegare un wallet reale o un ledger di crediti
    data = {
        "balance": 9400,
        "last_tx": {
            "type": "earn",
            "amount": 45,
            "source": "starlink_hybrid",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }
    return jsonify(data)


@app.route("/api/podcast/list")
def podcast_list():
    cfg = load_config()
    streams = cfg.get("podcast", {}).get("default_streams", [])
    return jsonify({
        "streams": streams
    })


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    target = STATIC_DIR / path
    if path and target.exists():
        return app.send_static_file(path)
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
