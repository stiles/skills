#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Look up stock ticker symbols by company name.

Searches an embedded database of ~570 common tickers (S&P 500 + extras).
Supports partial, case-insensitive matching.
"""

import json
import os
import sys


def load_tickers():
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "tickers.json",
    )
    with open(data_path) as f:
        return json.load(f)


def search(query, tickers):
    query_lower = query.lower().strip()

    exact_ticker = [t for t in tickers if t["ticker"].lower() == query_lower]
    if exact_ticker:
        return exact_ticker

    exact_name = [t for t in tickers if t["name"].lower() == query_lower]
    if exact_name:
        return exact_name

    partial = [
        t
        for t in tickers
        if query_lower in t["name"].lower() or query_lower in t["ticker"].lower()
    ]
    return partial


def format_result(t):
    return f'{t["ticker"]:8s} {t["name"]:45s} ({t["sector"]})'


def main():
    if len(sys.argv) < 2:
        print("Usage: lookup_ticker.py <company name or ticker>", file=sys.stderr)
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    tickers = load_tickers()
    results = search(query, tickers)

    if not results:
        print(f"No match found for '{query}'", file=sys.stderr)
        sys.exit(1)

    for r in results:
        print(format_result(r))


if __name__ == "__main__":
    main()
