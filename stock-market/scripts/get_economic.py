#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Fetch economic indicators from CNN data endpoints.

Supports consumer sentiment (U of Michigan), CPI inflation and gas prices (AAA).
"""

import argparse
import json
import re
import sys

import requests

ENDPOINTS = {
    "sentiment": "https://ix.cnn.io/data/consumer-sentiment/consumer_sentiment_summary.json",
    "cpi": "https://ix.cnn.io/data/consumer-price-index/cpi.json",
    "gas": "https://ix.cnn.io/data/gas-prices/aaa_gas_prices_avg_national_five_years.json",
}

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
}


def fetch(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


def summarize_sentiment(data):
    meta = data.get("metadata", {})
    return {
        "indicator": "consumer_sentiment",
        "source": "University of Michigan",
        "current_month": meta.get("current_month", ""),
        "current_value": meta.get("current_value"),
        "previous_value": meta.get("prev_value"),
        "previous_month": meta.get("prev_month", ""),
        "direction": meta.get("change_phrase", ""),
        "historical_mean": round(meta.get("historical_mean", 0), 1),
        "last_20yr_mean": round(meta.get("last_20_years_mean", 0), 1),
        "is_preliminary": meta.get("is_preliminary", False),
        "last_updated": meta.get("last_updated_str", ""),
        "summary": strip_html(meta.get("summary_sentence", "")),
    }


def summarize_cpi(data):
    return {
        "indicator": "cpi_inflation",
        "source": data.get("source", "US Bureau of Labor Statistics"),
        "latest_month": data.get("latestMonthStr", ""),
        "latest_value_pct": round(data.get("latestValue", 0), 1),
        "ten_year_mean_pct": data.get("mean10years"),
        "last_updated": data.get("lastUpdatedStr", ""),
        "summary": strip_html(data.get("summary", "")),
    }


def summarize_gas(data):
    meta = data.get("metadata", {})
    trends = meta.get("trends", {})
    return {
        "indicator": "gas_prices",
        "source": meta.get("source", "AAA"),
        "latest_date": meta.get("latestDateFormatted", ""),
        "national_avg": meta.get("latestValue"),
        "day_change": trends.get("dayChange"),
        "year_change": trends.get("yearChange"),
        "year_ago_price": trends.get("yearChangePrevPrice"),
        "last_updated": meta.get("lastUpdatedStr", ""),
        "summary": meta.get("summary", ""),
    }


def build_narrative_sentiment(data):
    meta = data.get("metadata", {})
    value = meta.get("current_value")
    month = meta.get("current_month", "").rstrip("*")
    prev = meta.get("prev_value")
    prev_month = meta.get("prev_month", "")
    mean_20 = meta.get("last_20_years_mean", 78)
    direction = meta.get("change_phrase", "")
    prelim = " (preliminary)" if meta.get("is_preliminary") else ""

    vs_avg = "below" if value < mean_20 else "above"
    pct_change = round(abs(value - prev) / prev * 100, 1) if prev else 0

    return (
        f"The University of Michigan Consumer Sentiment Index{prelim} is {value} "
        f"in {month}, {direction} about {pct_change}% from {prev} in {prev_month}. "
        f"That is {vs_avg} the 20-year average of {mean_20:.0f}."
    )


def build_narrative_cpi(data):
    value = round(data.get("latestValue", 0), 1)
    month = data.get("latestMonthStr", "")
    mean_10 = data.get("mean10years")

    parts = [strip_html(data.get("summary", ""))]
    if mean_10:
        comparison = "below" if value < mean_10 else "above"
        parts.append(f"That is {comparison} the 10-year average of {mean_10}%.")
    return " ".join(parts)


def build_narrative_gas(data):
    meta = data.get("metadata", {})
    trends = meta.get("trends", {})
    price = meta.get("latestValue")
    date_str = meta.get("latestDateFormatted", "")
    day_change = trends.get("dayChange", 0)
    year_change = trends.get("yearChange", 0)
    year_ago = trends.get("yearChangePrevPrice")

    day_dir = "up" if day_change > 0 else "down"
    year_dir = "up" if year_change > 0 else "down"

    return (
        f"The national average gas price is ${price:.2f} as of {date_str}, "
        f"{day_dir} ${abs(day_change):.2f} from the prior day. "
        f"Compared to a year ago (${year_ago:.2f}), prices are "
        f"{year_dir} ${abs(year_change):.2f}."
    )


SUMMARIZERS = {
    "sentiment": summarize_sentiment,
    "cpi": summarize_cpi,
    "gas": summarize_gas,
}

NARRATORS = {
    "sentiment": build_narrative_sentiment,
    "cpi": build_narrative_cpi,
    "gas": build_narrative_gas,
}


def main():
    parser = argparse.ArgumentParser(description="Fetch economic indicators")
    parser.add_argument(
        "indicators",
        nargs="+",
        choices=list(ENDPOINTS.keys()) + ["all"],
        help="Which indicator(s) to fetch: sentiment, cpi, gas, or all",
    )
    parser.add_argument("--narrative", action="store_true",
                        help="Output plain-English summaries")
    args = parser.parse_args()

    targets = list(ENDPOINTS.keys()) if "all" in args.indicators else args.indicators

    results = []
    narratives = []

    for key in targets:
        data = fetch(ENDPOINTS[key])
        if data is None:
            continue
        results.append(SUMMARIZERS[key](data))
        if args.narrative:
            narratives.append(NARRATORS[key](data))

    if not results:
        print("No data returned", file=sys.stderr)
        sys.exit(1)

    if args.narrative:
        print("\n\n".join(narratives))
    else:
        output = results[0] if len(results) == 1 else results
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
