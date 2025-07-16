from flask import Flask, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ BTC JSON Aggregator is running"

@app.route("/<timeframe>.json")
def serve_json(timeframe):
    filename = f"{timeframe}.json"
    if os.path.exists(filename):
        return send_file(filename)
    return "❌ JSON not found", 404
