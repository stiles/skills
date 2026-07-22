#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Fetch stock price history from CNN Business API.

Supports one or more tickers, date filtering and summary output.
"""

import argparse
import json
import sys
from datetime import datetime, date

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

VALID_RANGES = ["1Y", "3Y", "5Y"]


def auto_range(since_date_str):
    """Pick the smallest range that covers the --since date."""
    since = datetime.strptime(since_date_str, "%Y-%m-%d").date()
    today = date.today()
    days_back = (today - since).days
    if days_back <= 365:
        return "1Y"
    if days_back <= 365 * 3:
        return "3Y"
    return "5Y"


def fetch_stock(ticker, date_range):
    url = f"{API_BASE}/{ticker}/{date_range}/false"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list) or not data:
            return None
        return data
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching {ticker}: {e}", file=sys.stderr)
        return None


def process_stock(ticker, date_range, since_date=None):
    raw = fetch_stock(ticker, date_range)
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

    if since_date:
        records = [r for r in records if r["date"] >= since_date]

    if not records:
        print(f"No data for {ticker} in the requested range", file=sys.stderr)
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
        "ticker": ticker,
        "range": date_range,
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
    parser = argparse.ArgumentParser(description="Fetch stock prices from CNN Business API")
    parser.add_argument("tickers", nargs="+", help="One or more ticker symbols (e.g. INTC F NVDA)")
    parser.add_argument("--range", dest="date_range", default=None, choices=VALID_RANGES,
                        help="Date range: 1Y, 3Y, 5Y (auto-selected when --since is given)")
    parser.add_argument("--since", dest="since_date", default=None,
                        help="Filter data from this date forward (YYYY-MM-DD)")
    parser.add_argument("--summary", action="store_true",
                        help="Omit raw data array, output metrics only")
    args = parser.parse_args()

    if args.since_date:
        try:
            datetime.strptime(args.since_date, "%Y-%m-%d")
        except ValueError:
            print("Error: --since must be YYYY-MM-DD format", file=sys.stderr)
            sys.exit(1)

    date_range = args.date_range
    if date_range is None:
        date_range = auto_range(args.since_date) if args.since_date else "1Y"

    results = []
    for ticker in args.tickers:
        result = process_stock(ticker.upper(), date_range, args.since_date)
        if result:
            if args.summary:
                result.pop("data", None)
            results.append(result)

    if not results:
        print("No data returned for any ticker", file=sys.stderr)
        sys.exit(1)

    output = results[0] if len(results) == 1 else results
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
