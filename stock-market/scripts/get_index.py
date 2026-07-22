#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Fetch stock index history from CNN charting API.

Supports Dow Jones (DJII), S&P 500 (SP500), and Nasdaq (COMP).
"""

import argparse
import json
import sys
from datetime import datetime, date, timedelta

import requests

API_BASE = "https://production.dataviz.cnn.io/charting/instruments"

HEADERS = {
    "authority": "production.dataviz.cnn.io",
    "accept": "*/*",
    "origin": "https://www.cnn.com",
    "referer": "https://www.cnn.com/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
}

VALID_FREQUENCIES = [
    "DEFAULT", "1MIN", "3MIN", "5MIN", "10MIN", "15MIN", "30MIN",
    "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"
]

INDICES = {
    "DJII": "Dow Jones Industrial Average",
    "SP500": "S&P 500",
    "COMP": "Nasdaq Composite"
}


def fetch_index(symbol, start_date, end_date, frequency):
    url = f"{API_BASE}/{symbol}/Index/{start_date}/{end_date}/{frequency}/false"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list) or not data:
            return None
        return data
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching {symbol}: {e}", file=sys.stderr)
        return None


def process_index(symbol, start_date, end_date, frequency):
    raw = fetch_index(symbol, start_date, end_date, frequency)
    if raw is None:
        return None

    records = []
    for row in raw:
        if "event_date" not in row or "current_price" not in row:
            continue
        records.append({
            "date": row["event_date"],
            "close": round(row["current_price"], 2),
        })

    records.sort(key=lambda r: r["date"])

    if not records:
        print(f"No data for {symbol} in the requested range", file=sys.stderr)
        return None

    closes = [r["close"] for r in records]
    max_close = max(closes)
    min_close = min(closes)
    max_idx = closes.index(max_close)
    min_idx = closes.index(min_close)

    start_close = records[0]["close"]
    latest_close = records[-1]["close"]
    pct_change = round(((latest_close - start_close) / start_close) * 100, 2)

    return {
        "symbol": symbol,
        "name": INDICES.get(symbol, symbol),
        "frequency": frequency,
        "latest_date": records[-1]["date"],
        "latest_close": latest_close,
        "start_date": records[0]["date"],
        "start_close": start_close,
        "pct_change": pct_change,
        "high": max_close,
        "high_date": records[max_idx]["date"],
        "low": min_close,
        "low_date": records[min_idx]["date"],
        "data_points": len(records),
        "data": records,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch stock index data from CNN charting API")
    parser.add_argument("symbols", nargs="+", choices=list(INDICES.keys()),
                        help="One or more index symbols: DJII (Dow), SP500 (S&P 500), COMP (Nasdaq)")
    parser.add_argument("--start", dest="start_date", default=None,
                        help="Start date (YYYY-MM-DD). Defaults to 1 year ago")
    parser.add_argument("--end", dest="end_date", default=None,
                        help="End date (YYYY-MM-DD). Defaults to today")
    parser.add_argument("--frequency", default="DEFAULT", choices=VALID_FREQUENCIES,
                        help="Data frequency (default: DEFAULT)")
    parser.add_argument("--summary", action="store_true",
                        help="Omit raw data array, output metrics only")
    args = parser.parse_args()

    today = date.today()
    one_year_ago = today - timedelta(days=365)

    start_date = args.start_date or one_year_ago.strftime("%Y-%m-%d")
    end_date = args.end_date or today.strftime("%Y-%m-%d")

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: dates must be YYYY-MM-DD format", file=sys.stderr)
        sys.exit(1)

    results = []
    for symbol in args.symbols:
        result = process_index(symbol.upper(), start_date, end_date, args.frequency)
        if result:
            if args.summary:
                result.pop("data", None)
            results.append(result)

    if not results:
        print("No data returned for any index", file=sys.stderr)
        sys.exit(1)

    output = results[0] if len(results) == 1 else results
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
