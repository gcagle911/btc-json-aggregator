import requests
import pandas as pd
from io import StringIO
import os
from datetime import datetime

# ✅ Your correct endpoints
LIST_ENDPOINT = "https://btc-spread-test-pipeline.onrender.com/csv-list"
CSV_BASE_URL  = "https://btc-spread-test-pipeline.onrender.com/csv/"

# ✅ 5 confirmed manually saved CSVs from your screenshot
BASE_CSV_LIST = [
    "2025-07-14_16.csv",
    "2025-07-15_00.csv",
    "2025-07-15_08.csv",
    "2025-07-15_16.csv",
    "2025-07-16_00.csv"
]

def get_latest_csv_url():
    try:
        res = requests.get(LIST_ENDPOINT)
        files = res.json().get("available_csvs", [])
        if not files:
            print("❌ No files found in /csv-list")
            return None
        files.sort()
        latest_file = files[-1]
        print(f"📁 Latest CSV: {latest_file}")
        return CSV_BASE_URL + latest_file
    except Exception as e:
        print("❌ Error fetching latest CSV:", e)
        return None

def load_csv(url):
    try:
        print(f"⬇️ Downloading: {url}")
        r = requests.get(url)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
        return df
    except Exception as e:
        print(f"❌ Failed to load {url}:", e)
        return None

def process_timeframes():
    # Start with your known saved files
    urls = [CSV_BASE_URL + filename for filename in BASE_CSV_LIST]

    # Add most recent CSV dynamically
    latest_url = get_latest_csv_url()
    if latest_url and latest_url not in urls:
        urls.append(latest_url)

    all_data = []
    for url in urls:
        df = load_csv(url)
        if df is not None:
            all_data.append(df)

    if not all_data:
        print("❌ No data could be loaded.")
        return

    # Combine and sort
    df = pd.concat(all_data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    df = df.sort_index()

    # Create multiple timeframes
    output_frames = {
        '1min': df.resample('1T').mean().dropna(),
        '5min': df.resample('5T').mean().dropna(),
        '1h':   df.resample('1H').mean().dropna(),
    }

    # Save each to JSON
    for name, resampled in output_frames.items():
        out = resampled.reset_index()
        out['time'] = out['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        out.to_json(f"{name}.json", orient="records")
        print(f"✅ Saved {name}.json with {len(out)} points")

if __name__ == "__main__":
    process_timeframes()
