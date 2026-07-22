---
name: stock-market
description: Fetch stock prices, indices, commodities, the CNN Fear & Greed Index and economic indicators. Use when asked about stock performance, company comparisons, market indices (Dow, S&P 500, Nasdaq), oil prices, market sentiment, the Fear & Greed Index, consumer sentiment, CPI inflation or gas prices.
---

# Stock market skill

Fetches stock price history from the CNN Business API, stock indices (Dow Jones, S&P 500, Nasdaq), commodities (crude oil, Brent crude), the CNN Fear & Greed Index and economic indicators (consumer sentiment, CPI, gas prices). Covers ~550 common tickers (S&P 500 + popular extras). Only individual stocks are supported -- ETFs (SPY, QQQ, etc.) and crypto are not available through this API.

## When to use this skill

Use this skill when:
- User asks about a company's stock price or performance
- User wants to compare stock performance across companies
- User asks about YTD or historical percentage change for a stock
- User asks about market indices (Dow Jones, S&P 500, Nasdaq)
- User asks about oil prices or crude oil
- User asks about market sentiment, fear and greed or "How are the markets doing?"
- User mentions the CNN Fear & Greed Index
- User asks about consumer sentiment or the University of Michigan sentiment index
- User asks about inflation or CPI
- User asks about gas prices

## Dependencies

Scripts use PEP 723 inline metadata. Dependencies install automatically via `uv run`.

**IMPORTANT**: Use `uv run script.py` NOT `uv run python script.py`.

## Standard workflow

### Looking up a ticker

If you have a company name but not the ticker symbol, resolve it first:

```bash
uv run skills/stock-market/scripts/lookup_ticker.py "Intel"
# Output: INTC     Intel Corp                                    (Technology)
```

Partial matches are supported. If multiple results appear, pick the correct one based on context.

If you already know the ticker (e.g. AAPL, TSLA, NVDA), skip this step.

### Fetching stock data

```bash
uv run skills/stock-market/scripts/get_stock.py TICKER [TICKER2 ...] [--range 1Y|3Y|5Y] [--since YYYY-MM-DD] [--summary]
```

**Arguments:**
- `TICKER`: One or more ticker symbols (required). Must be individual stocks -- ETFs (SPY, QQQ, DIA, etc.) are not supported by the CNN API.
- `--range`: How far back to fetch. Options: `1Y`, `3Y`, `5Y`. When omitted, the range is auto-selected based on `--since` (or defaults to `1Y`). You rarely need to set this manually.
- `--since`: Only include data from this date forward (YYYY-MM-DD). Recomputes all metrics based on the filtered window. The script automatically picks a range wide enough to cover the date.
- `--summary`: Omit the raw `data` array; output only summary metrics

**Output fields:**
- `ticker`, `range`, `data_points`
- `start_date`, `start_close` - first data point in the window
- `latest_date`, `latest_close` - most recent data point
- `pct_change` - percentage change from start to latest
- `high`, `high_date` - highest close in the window
- `low`, `low_date` - lowest close in the window
- `data` - array of `{"date", "close"}` records (omitted with `--summary`)

When given multiple tickers, the output is a JSON array.

### Fetching stock indices

```bash
uv run skills/stock-market/scripts/get_index.py SYMBOL [SYMBOL2 ...] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--frequency FREQ] [--summary]
```

**Arguments:**
- `SYMBOL`: One or more index symbols (required). Available: `DJII` (Dow Jones), `SP500` (S&P 500), `COMP` (Nasdaq)
- `--start`: Start date (YYYY-MM-DD). Defaults to 1 year ago
- `--end`: End date (YYYY-MM-DD). Defaults to today
- `--frequency`: Data frequency. Options: `DEFAULT`, `1MIN`, `3MIN`, `5MIN`, `10MIN`, `15MIN`, `30MIN`, `HOURLY`, `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`. Default: `DEFAULT`
- `--summary`: Omit the raw `data` array; output only summary metrics

**Output fields:**
- `symbol`, `name`, `frequency`, `data_points`
- `start_date`, `start_close` - first data point in the window
- `latest_date`, `latest_close` - most recent data point
- `pct_change` - percentage change from start to latest
- `high`, `high_date` - highest close in the window
- `low`, `low_date` - lowest close in the window
- `data` - array of `{"date", "close"}` records (omitted with `--summary`)

When given multiple symbols, the output is a JSON array.

### Fetching commodities

```bash
uv run skills/stock-market/scripts/get_commodity.py SYMBOL [SYMBOL2 ...] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--frequency FREQ] [--summary]
```

**Arguments:**
- `SYMBOL`: One or more commodity symbols (required). Available: `CL00` (Crude Oil), `BZC00` (Brent Crude)
- `--start`: Start date (YYYY-MM-DD). Defaults to 1 year ago
- `--end`: End date (YYYY-MM-DD). Defaults to today
- `--frequency`: Data frequency. Options: `DEFAULT`, `1MIN`, `3MIN`, `5MIN`, `10MIN`, `15MIN`, `30MIN`, `HOURLY`, `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`. Default: `DAILY`
- `--summary`: Omit the raw `data` array; output only summary metrics

**Output fields:**
- `symbol`, `name`, `frequency`, `data_points`
- `start_date`, `start_price` - first data point in the window
- `latest_date`, `latest_price` - most recent data point
- `pct_change` - percentage change from start to latest
- `high`, `high_date` - highest price in the window
- `low`, `low_date` - lowest price in the window
- `data` - array of `{"date", "price"}` records (omitted with `--summary`)

When given multiple symbols, the output is a JSON array.

### Fetching the Fear & Greed Index

```bash
uv run skills/stock-market/scripts/get_fear_greed.py [--narrative] [--history]
```

**Flags:**
- `--narrative`: Output a plain-English paragraph summarizing the current score, trend and context. Use this for conversational answers.
- `--history`: Include the daily historical data array in JSON output. Use this when charting or analyzing trends.
- Default (no flags): JSON with current score, rating, comparisons and trend direction.

### Fetching economic indicators

```bash
uv run skills/stock-market/scripts/get_economic.py INDICATOR [INDICATOR ...] [--narrative]
```

**Arguments:**
- `INDICATOR`: One or more of `sentiment`, `cpi`, `gas`, or `all`
- `--narrative`: Output plain-English summaries instead of JSON

**Available indicators:**
- `sentiment` -- University of Michigan Consumer Sentiment Index. Measures consumer confidence. Source: `ix.cnn.io/data/consumer-sentiment/consumer_sentiment_summary.json`
- `cpi` -- Consumer Price Index (12-month % change). Measures inflation. Source: `ix.cnn.io/data/consumer-price-index/cpi.json`
- `gas` -- National average gas price from AAA. Source: `ix.cnn.io/data/gas-prices/aaa_gas_prices_avg_national_five_years.json`

All three endpoints are static JSON files updated by bots. No authentication required.

## Example workflows

### "How has Intel done since the start of the year?"

```bash
uv run skills/stock-market/scripts/get_stock.py INTC --since 2026-01-01 --summary
```

Present the `pct_change` in context: "Intel (INTC) is up 11.4% year-to-date, trading at $43.87 as of March 20."

### "Compare Ford and Tesla over the last year"

```bash
uv run skills/stock-market/scripts/get_stock.py F TSLA --range 1Y --summary
```

Compare `pct_change` values side by side.

### "How are the markets doing today?"

```bash
uv run skills/stock-market/scripts/get_index.py DJII SP500 COMP --start 2026-01-01 --summary
```

Present the indices with their changes: "The Dow is up 3.2%, the S&P 500 is up 4.1%, and the Nasdaq is up 5.7% year-to-date."

You can also combine with the Fear & Greed Index:

```bash
uv run skills/stock-market/scripts/get_fear_greed.py --narrative
```

### "What's the price of oil right now?"

```bash
uv run skills/stock-market/scripts/get_commodity.py CL00 BZC00 --summary
```

Present the latest prices: "Crude oil (WTI) is trading at $68.45 per barrel, while Brent crude is at $72.10."

### "Show me oil prices over the last 6 months"

```bash
uv run skills/stock-market/scripts/get_commodity.py CL00 --start 2025-10-01 --end 2026-04-02
```

Use the full `data` array to chart the trend or analyze volatility.

### "What's the state of the markets right now?"

Combine indices with the Fear & Greed narrative:

```bash
uv run skills/stock-market/scripts/get_index.py DJII SP500 COMP --summary
uv run skills/stock-market/scripts/get_fear_greed.py --narrative
```

### "Show me the Fear & Greed trend for charting"

```bash
uv run skills/stock-market/scripts/get_fear_greed.py --history
```

The `history` array contains daily `{"date", "score", "rating"}` objects.

### "What's consumer sentiment right now?"

```bash
uv run skills/stock-market/scripts/get_economic.py sentiment --narrative
```

### "Give me a quick economic snapshot"

```bash
uv run skills/stock-market/scripts/get_economic.py all --narrative
```

Combine this with the Fear & Greed narrative and bellwether stocks for a full market picture.

### "How much is gas right now?"

```bash
uv run skills/stock-market/scripts/get_economic.py gas --narrative
```

### Looking up a company by name

```bash
uv run skills/stock-market/scripts/lookup_ticker.py "solar"
# FSLR     First Solar Inc                               (Technology)
# SEDG     SolarEdge Technologies Inc                    (Technology)
```

Multiple matches are printed. Pick the one that fits and pass it to `get_stock.py`.

## Important notes

- **CNN API**: No authentication required. Data source is CNN Business.
- **Individual stocks only**: The CNN API supports individual stock tickers. ETFs (SPY, QQQ, DIA, IWM, etc.) and crypto (BTC, ETH) return 404 errors. For broad market questions, use the index endpoints (DJII, SP500, COMP) or a handful of large-cap stocks (AAPL, MSFT, NVDA, AMZN, GOOG) as proxies alongside the Fear & Greed Index.
- **Stock indices**: Use `get_index.py` for Dow Jones (DJII), S&P 500 (SP500), and Nasdaq Composite (COMP). These provide direct market index data without needing ETFs.
- **Commodities**: Use `get_commodity.py` for crude oil (CL00) and Brent crude (BZC00). Prices are per barrel in USD.
- **Date ranges**: Stock data uses fixed ranges (1Y, 3Y, 5Y). Indices and commodities use flexible start/end dates.
- **Frequencies**: Indices and commodities support multiple frequencies from 1-minute to yearly data. Use `DAILY` for most queries. Intraday frequencies (1MIN, 5MIN, etc.) are useful for real-time analysis but return large datasets.
- **Range auto-selection**: When `--since` is provided without `--range` for stocks, the script picks the smallest range that covers the date (1Y, 3Y or 5Y). You can still override with `--range` if needed.
- **Ticker database**: The `data/tickers.json` file covers ~550 entries. If a ticker isn't in the database, you can still pass it directly to `get_stock.py` -- the lookup step is just a convenience.
- **Market hours**: Stock data updates at market close. Prices reflect the most recent trading day.
- **Fear & Greed Index**: Scored 0-100. Ratings: extreme fear (0-24), fear (25-44), neutral (45-55), greed (56-74), extreme greed (75-100).
- **Network required**: All scripts make HTTP requests to CNN endpoints.

## Output guidance

- Present percentage changes in plain language: "Intel is down 25% since January" not "pct_change: -25".
- For indices, use common names: "The Dow" or "Dow Jones" instead of "DJII". "The S&P 500" or just "S&P" instead of "SP500". "The Nasdaq" instead of "COMP".
- For commodities, say "crude oil" or "WTI crude" for CL00, and "Brent crude" for BZC00.
- For market sentiment, use `--narrative` and incorporate the output into a natural response.
- Use `--summary` unless the user specifically needs raw price data or you need to build a chart.
- When comparing stocks or indices, make sure to use the same date range for a fair comparison.
- For "how are markets doing" queries, show the three major indices (Dow, S&P, Nasdaq) together with YTD performance.
