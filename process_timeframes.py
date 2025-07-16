import requests
import pandas as pd
from io import StringIO
import os
from datetime import datetime

BASE_CSV_LIST = [
    # Manually selected CSVs you want to include
    "https://btc-spread-test-pipeline.onrender.com/csv/2025-07-14_16.csv",
    "https://btc-spread-test-pipeline.onrender.com/csv/2025-07-15_00.csv",
    "https://btc-spread-test-pipeline.onrender.com/csv/2025-07-15_08.csv",
    "https://btc-spread-test-pipeline.onrender.com/csv/2025-07-15_16.csv",
    "https://btc-spread-test-pipeline.onrender.com/csv/2025-07-16_00.csv",
]

LIST_ENDPOINT = "https://btc-spread-test-pipeline.onrender.com/list-csvs"
CSV_BASE_URL = "https://btc-spread-test-pipeline.onrender.com/csv/"

def get_latest_csv_url():
    try:
        res = requests.get(LIST_ENDPOINT)
        files = res.json().get("available_csvs", [])
        if not files:
            return None
        files.sort()
        return CSV_BASE_URL + files[-1]
    except Exception as e:
        print("Error getting latest CSV:", e)
        return None

def load_csv(url):
    try:
        print(f"Fetching: {url}")
        r = requests.get(url)
        df = pd.read_csv(StringIO(r.text))
        return df
    except Exception as e:
        print(f"Failed to load {url}:", e)
        return None

def process_timeframes():
    urls = BASE_CSV_LIST.copy()
    latest = get_latest_csv_url()
    if latest and latest not in urls:
        urls.append(latest)

    all_data = []
    for url in urls:
        df = load_csv(url)
        if df is not None:
            all_data.append(df)

    if not all_data:
        print("❌ No data loaded")
        return

    df = pd.concat(all_data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    df = df.sort_index()

    output_frames = {
        '1min': df.resample('1T').mean().dropna(),
        '5min': df.resample('5T').mean().dropna(),
        '1h': df.resample('1H').mean().dropna(),
    }

    for name, resampled in output_frames.items():
        out = resampled.reset_index()
        out['time'] = out['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        out.to_json(f"{name}.json", orient="records")
        print(f"✅ Saved {name}.json ({len(out)} points)")

if __name__ == "__main__":
    process_timeframes()
