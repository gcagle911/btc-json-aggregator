from flask import Flask, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ BTC JSON Aggregator is running."

@app.route("/<timeframe>.json")
def serve_json(timeframe):
    try:
        from process_timeframes import process_timeframes
        print(f"📦 Generating {timeframe}.json...")
        process_timeframes([timeframe])  # Only generate what's requested
        filename = f"{timeframe}.json"
        if os.path.exists(filename):
            return send_file(filename)
        return "❌ JSON not found", 404
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return "❌ Internal Server Error", 500
