#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort
import io, json, os, datetime

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA_FILE = os.path.join(ROOT, "docs", "data", "energy_wallets.json")

app = Flask("ghosttrack_wallet_api")

def load_data():
    with io.open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with io.open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/wallets", methods=["GET"])
def list_wallets():
    data = load_data()
    return jsonify(data)

@app.route("/wallets/<wallet_id>", methods=["GET"])
def get_wallet(wallet_id):
    data = load_data()
    for w in data.get("wallets", []):
        if w["id"] == wallet_id:
            return jsonify(w)
    abort(404)

@app.route("/wallets/<wallet_id>/transact", methods=["POST"])
def transact(wallet_id):
    payload = request.get_json(force=True)
    if not payload or "amount" not in payload or "type" not in payload:
        abort(400)
    data = load_data()
    for w in data.get("wallets", []):
        if w["id"] == wallet_id:
            w["impulsi"] = max(0, w.get("impulsi", 0) + int(payload["amount"]))
            entry = {
                "ts": datetime.datetime.utcnow().isoformat() + "Z",
                "type": payload["type"],
                "amount": int(payload["amount"]),
                "meta": payload.get("meta", {})
            }
            w.setdefault("history", []).append(entry)
            save_data(data)
            return jsonify({"status": "ok", "wallet": w})
    abort(404)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
