from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ✅ Serve root URL for basic confirmation
@app.route("/")
def home():
    return "✅ BTC JSON Aggregator is running"

# ✅ Serve timeframe JSONs
@app.route("/<filename>")
def serve_json(filename):
    if filename in ["1min.json", "5min.json", "1h.json"]:
        return send_from_directory(".", filename)
    return "❌ File not found", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
