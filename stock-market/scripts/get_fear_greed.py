#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Fetch the CNN Fear & Greed Index and output JSON or a narrative summary.

The index ranges from 0 (maximum fear) to 100 (maximum greed).
"""

import argparse
import json
import sys
from datetime import datetime, timezone

import requests

API_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

HEADERS = {
    "accept": "*/*",
    "origin": "https://www.cnn.com",
    "referer": "https://www.cnn.com/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    ),
}


def fetch_index():
    try:
        resp = requests.get(API_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching Fear & Greed Index: {e}", file=sys.stderr)
        sys.exit(1)


def compute_trend(current, previous_week):
    diff = current - previous_week
    if abs(diff) < 2:
        return "flat"
    return "rising" if diff > 0 else "falling"


def rating_description(rating):
    labels = {
        "extreme fear": "deep in extreme fear territory",
        "fear": "in fear territory",
        "neutral": "in neutral territory",
        "greed": "in greed territory",
        "extreme greed": "deep in extreme greed territory",
    }
    return labels.get(rating, f"at {rating}")


def build_narrative(fg):
    score = fg["score"]
    rating = fg["rating"]
    prev_close = fg["previous_close"]
    prev_week = fg["previous_1_week"]
    prev_month = fg["previous_1_month"]
    prev_year = fg["previous_1_year"]

    trend = compute_trend(score, prev_week)
    ts = fg.get("timestamp", "")
    if ts:
        try:
            dt = datetime.fromisoformat(ts.replace("+00:00", "+00:00"))
            date_str = dt.strftime("%B %-d, %Y")
        except (ValueError, TypeError):
            date_str = "today"
    else:
        date_str = "today"

    trend_phrase = {
        "rising": f"up from {prev_week:.0f} a week ago",
        "falling": f"down from {prev_week:.0f} a week ago",
        "flat": f"roughly unchanged from {prev_week:.0f} a week ago",
    }[trend]

    month_direction = "up" if score > prev_month else "down"
    month_phrase = f"{month_direction} from {prev_month:.0f} a month ago"

    year_diff = abs(score - prev_year)
    if year_diff < 3:
        year_phrase = f"about the same as {prev_year:.0f} a year ago"
    else:
        year_direction = "up" if score > prev_year else "down"
        year_phrase = f"{year_direction} from {prev_year:.0f} a year ago"

    lines = [
        f"As of {date_str}, the CNN Fear & Greed Index sits at {score:.1f}, "
        f"{rating_description(rating)}.",
        f"The score is {trend_phrase} and {month_phrase}.",
        f"Compared to a year ago, the index is {year_phrase}.",
    ]

    if score <= 25:
        lines.append(
            "Markets appear to be driven by fear right now, which historically "
            "can mean stocks are trading below their fair value."
        )
    elif score >= 75:
        lines.append(
            "Markets appear to be driven by greed right now, which historically "
            "can signal stocks are getting overvalued."
        )

    return " ".join(lines)


def build_output(data, include_history=False):
    fg = data.get("fear_and_greed", {})
    result = {
        "score": round(fg.get("score", 0), 1),
        "rating": fg.get("rating", ""),
        "timestamp": fg.get("timestamp", ""),
        "previous_close": round(fg.get("previous_close", 0), 1),
        "previous_1_week": round(fg.get("previous_1_week", 0), 1),
        "previous_1_month": round(fg.get("previous_1_month", 0), 1),
        "previous_1_year": round(fg.get("previous_1_year", 0), 1),
        "trend_direction": compute_trend(
            fg.get("score", 0), fg.get("previous_1_week", 0)
        ),
    }

    if include_history:
        hist = data.get("fear_and_greed_historical", {})
        history_data = hist.get("data", [])
        result["history"] = [
            {
                "date": datetime.fromtimestamp(
                    point["x"] / 1000, tz=timezone.utc
                ).strftime("%Y-%m-%d"),
                "score": round(point["y"], 1),
                "rating": point.get("rating", ""),
            }
            for point in history_data
            if "x" in point and "y" in point
        ]

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch CNN Fear & Greed Index")
    parser.add_argument("--narrative", action="store_true",
                        help="Output a plain-English summary paragraph")
    parser.add_argument("--history", action="store_true",
                        help="Include daily historical data in JSON output")
    args = parser.parse_args()

    data = fetch_index()

    if args.narrative:
        fg = data.get("fear_and_greed", {})
        print(build_narrative(fg))
    else:
        output = build_output(data, include_history=args.history)
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
