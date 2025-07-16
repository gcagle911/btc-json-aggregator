from flask import Flask, send_file
from flask_cors import CORS
from process_timeframes import process_timeframes
import os

app = Flask(__name__)
CORS(app)

try:
    print("🚀 Generating initial JSONs...")
    process_timeframes()
except Exception as e:
    print(f"⚠️ Error generating initial JSONs: {e}")

@app.route("/")
def home():
    return "✅ BTC JSON Aggregator is running."

@app.route("/<timeframe>.json")
def serve_json(timeframe):
    from process_timeframes import process_timeframes
    print(f"📦 Generating {timeframe}.json")
    process_timeframes()
    filename = f"{timeframe}.json"
    if os.path.exists(filename):
        return send_file(filename)
    return "❌ JSON not found", 404
