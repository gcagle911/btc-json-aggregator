from flask import Flask, send_file
from process_timeframes import process_timeframes
import os

app = Flask(__name__)

@app.before_first_request
def initialize():
    print("🚀 Generating initial JSONs...")
    process_timeframes()

@app.route("/")
def home():
    return "✅ BTC JSON Aggregator is running."

@app.route("/<timeframe>.json")
def serve_json(timeframe):
    filename = f"{timeframe}.json"
    if os.path.exists(filename):
        return send_file(filename)
    else:
        return f"❌ {filename} not found", 404
