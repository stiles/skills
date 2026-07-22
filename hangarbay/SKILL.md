---
name: hangarbay
description: Query FAA aircraft registry data for aircraft lookups, fleet analysis, and ownership research. Use when working with N-numbers, tail numbers, aircraft registration, owner searches, or aviation data analysis.
compatibility: Requires Python 3.9+ and hangarbay package
license: MIT
metadata:
  author: Matt Stiles
  version: "1.0.0"
---

# Hangarbay - FAA Aircraft Registry Tool

This skill enables fast queries of FAA aircraft registration data. Hangarbay provides clean, queryable access to 307,000+ aircraft registrations with owner, make/model, and specification data.

## Requirements

- Python 3.9+
- `hangarbay` package (installed via pip)

## Installation

```bash
pip install hangarbay
```

Or for local development:
```bash
cd ~/github/hangarbay
pip install -e ".[dev]"
```

## Data Setup

Hangarbay stores data in `~/.hangarbay/data/`. The first time you use it, download FAA data:

### Python API (for notebooks/scripts)
```python
import hangarbay as hb
hb.load_data()  # One-time download (~400MB, takes 1-2 minutes)
```

### Command-line Interface
```bash
hangar update   # Download, normalize and publish in one step
```

Data is stored globally at `~/.hangarbay/data/` so it's accessible from any project or notebook.

## Usage Modes

### Python API (Recommended for Analysis)

Best for notebooks and scripts where you need to manipulate data with pandas.

```python
import hangarbay as hb

# Look up a single aircraft
df = hb.search("N221LA")

# Find all aircraft owned by an entity
fleet = hb.fleet("United Airlines")
fleet = hb.fleet("LAPD|Los Angeles Police", state="CA")

# Custom SQL queries
df = hb.query("""
    SELECT maker, COUNT(*) as count
    FROM aircraft_decoded
    WHERE year_mfr > 2020
    GROUP BY maker
    ORDER BY count DESC
""")

# Check data age
info = hb.status()
print(f"Data is {info['age_days']} days old")
```

### CLI (Quick Lookups)

Best for quick terminal lookups and shell scripts.

```bash
# Look up an aircraft
hangar search N221LA

# Find a fleet
hangar fleet "LAPD|Los Angeles Police" --state CA --export lapd.csv

# Run SQL queries
hangar sql "SELECT COUNT(*) FROM aircraft"
hangar sql "SELECT * FROM aircraft_decoded WHERE year_mfr > 2020 LIMIT 10"

# Check data status
hangar status
```

## Key Functions

### `hb.search(n_number)` - Aircraft Lookup

Look up a single aircraft by N-number (tail number).

**Arguments:**
- `n_number` (str): N-number with or without "N" prefix (e.g., "N221LA" or "221LA")
- `skip_age_check` (bool): Skip data staleness warning

**Returns:** pandas DataFrame with aircraft details, make/model, and owner information

**Example:**
```python
# Both work the same
df = hb.search("N221LA")
df = hb.search("221LA")

# Access fields
print(df['maker'].iloc[0])      # "AIRBUS HELICOPTERS INC"
print(df['model'].iloc[0])      # "AS350B3"
print(df['year_mfr'].iloc[0])   # 2014
print(df['owner_name'].iloc[0]) # "LAPD AIR SUPPORT DIVISION"
```

### `hb.fleet(owner, state=None, limit=0)` - Fleet Search

Find all aircraft owned by a person or organization.

**Arguments:**
- `owner` (str): Owner name to search (case-insensitive, supports OR logic with `|`)
- `state` (str, optional): Filter by state (e.g., "CA", "TX")
- `limit` (int): Maximum results to return (0 = unlimited)
- `skip_age_check` (bool): Skip data staleness warning

**Returns:** pandas DataFrame with fleet information

**OR Logic:**
Use `|` (pipe) to search multiple patterns. Any match returns the record.

**Examples:**
```python
# Single owner search
fleet = hb.fleet("United Airlines")

# Multiple patterns (OR logic) - useful for name variations
fleet = hb.fleet("LAPD|Los Angeles Police")
fleet = hb.fleet("Delta|American|United")

# Filter by state
fleet = hb.fleet("LAPD", state="CA")

# Limit results
fleet = hb.fleet("Cessna", limit=100)

# Combine filters
fleet = hb.fleet("Delta|United", state="GA", limit=50)
```

**Common Use Cases:**
- Municipal fleets: `hb.fleet("LAPD|Los Angeles Police", state="CA")`
- Airlines: `hb.fleet("United Airlines|United Air Lines")`
- Government: `hb.fleet("US Air Force|USAF", state="CA")`
- Corporate: `hb.fleet("Boeing", state="WA")`

### `hb.query(sql)` - Custom SQL

Execute custom SQL queries against the DuckDB database.

**Arguments:**
- `sql` (str): SQL query string
- `skip_age_check` (bool): Skip data staleness warning

**Returns:** pandas DataFrame with query results

**Example:**
```python
# Top manufacturers by count
df = hb.query("""
    SELECT maker, COUNT(*) as count
    FROM aircraft_decoded
    WHERE year_mfr > 2020
    GROUP BY maker
    ORDER BY count DESC
    LIMIT 10
""")

# Aircraft by state
df = hb.query("""
    SELECT o.state, COUNT(*) as count
    FROM aircraft_decoded a
    JOIN owners_clean o ON a.n_number = o.n_number
    WHERE o.state = 'CA'
    GROUP BY o.state
""")

# Find specific models
df = hb.query("""
    SELECT a.n_number, a.maker, a.model, o.owner_name
    FROM aircraft_decoded a
    JOIN owners_clean o ON a.n_number = o.n_number
    WHERE a.model LIKE '%737%'
    ORDER BY a.year_mfr DESC
    LIMIT 20
""")
```

### `hb.status()` - Data Information

Get information about the current data snapshot.

**Returns:** Dictionary with metadata

**Example:**
```python
info = hb.status()
print(f"Data is {info['age_days']} days old")
print(f"Total aircraft: {info['aircraft_count']:,}")
print(f"Data snapshot: {info['snapshot_date']}")
print(f"Stale: {info['is_stale']}")  # True if 30+ days old
```

### `hb.list_tables()` - Available Tables

List all database tables.

**Returns:** List of table names

```python
tables = hb.list_tables()
# ['aircraft', 'aircraft_decoded', 'owners', 'owners_clean', ...]
```

### `hb.schema(table_name)` - Table Schema

Get column names and types for a table.

**Example:**
```python
schema = hb.schema('aircraft_decoded')
print(schema)
```

## Database Schema

### Recommended Tables (Decoded Views)

Use these for most queries - they have human-readable values and joined data.

**`aircraft_decoded`**
- All aircraft with decoded status codes and joined make/model
- Key fields: `n_number`, `maker`, `model`, `year_mfr`, `reg_status`, `serial_no`

**`owners_clean`**
- Simplified owner information with standardized addresses
- Key fields: `n_number`, `owner_name`, `city`, `state`, `zip`, `address`

### Core Tables

**`aircraft`**
- Raw aircraft registration data
- Fields: `n_number`, `serial_no`, `mfr_mdl_code`, `year_mfr`, `reg_status`, `mode_s_code`

**`owners`**
- Owner records with raw and standardized addresses
- Fields: `n_number`, `owner_name`, `owner_name_std`, `city_std`, `state_std`, `zip5`

**`registrations`**
- Registration certificates and dates
- Fields: `n_number`, `reg_type`, `cert_issue_date`, `reg_expiration`

**`aircraft_make_model`**
- Make and model reference table
- Fields: `mfr_mdl_code`, `maker`, `model`, `type_aircraft`

**`engines`**
- Engine specifications
- Fields: `eng_code`, `eng_mfr`, `eng_model`, `eng_type`, `horsepower`, `thrust`

### Reference Tables

- `status_codes` - Registration status code lookups
- `airworthiness_classes` - Airworthiness certificate class lookups
- `owner_types` - Owner type code lookups

## Common Query Patterns

### Fleet Analysis

```python
import hangarbay as hb
import pandas as pd

# Get LAPD fleet
lapd = hb.fleet("LAPD|Los Angeles Police", state="CA")

print(f"Total aircraft: {len(lapd)}")
print(f"Valid registrations: {(lapd['reg_status'] == 'Valid').sum()}")

# Breakdown by manufacturer
print(lapd['maker'].value_counts())

# Average age
avg_age = 2026 - lapd['year_mfr'].mean()
print(f"Average age: {avg_age:.1f} years")
```

### Geographic Analysis

```python
# Aircraft by state
df = hb.query("""
    SELECT state, COUNT(*) as count
    FROM owners_clean
    WHERE state != ''
    GROUP BY state
    ORDER BY count DESC
    LIMIT 10
""")

# California helicopters
df = hb.query("""
    SELECT a.maker, COUNT(*) as count
    FROM aircraft_decoded a
    JOIN owners_clean o ON a.n_number = o.n_number
    WHERE o.state = 'CA'
    AND a.type_aircraft LIKE '%ROTORCRAFT%'
    GROUP BY a.maker
    ORDER BY count DESC
""")
```

### Manufacturer Analysis

```python
# Top manufacturers by count
df = hb.query("""
    SELECT maker, COUNT(*) as count
    FROM aircraft_decoded
    WHERE maker != ''
    GROUP BY maker
    ORDER BY count DESC
    LIMIT 20
""")

# All Boeing aircraft
df = hb.query("""
    SELECT n_number, model, year_mfr
    FROM aircraft_decoded
    WHERE maker LIKE '%BOEING%'
    ORDER BY year_mfr DESC
""")
```

### Age and Status Analysis

```python
# Aircraft manufactured after 2020
df = hb.query("""
    SELECT maker, COUNT(*) as count
    FROM aircraft_decoded
    WHERE year_mfr > 2020
    GROUP BY maker
    ORDER BY count DESC
""")

# Registration status breakdown
df = hb.query("""
    SELECT reg_status, COUNT(*) as count
    FROM aircraft_decoded
    GROUP BY reg_status
    ORDER BY count DESC
""")
```

## CLI Reference

### Search Commands

```bash
# Look up an aircraft
hangar search N221LA

# Fleet search
hangar fleet "United Airlines"
hangar fleet "LAPD|Los Angeles Police" --state CA
hangar fleet "Boeing" --export boeing.csv --limit 100
```

### SQL Queries

```bash
# Basic queries
hangar sql "SELECT COUNT(*) FROM aircraft"
hangar sql "SELECT * FROM aircraft_decoded LIMIT 10"

# Case-insensitive search (use -i flag)
hangar sql "SELECT * FROM owners_clean WHERE owner_name LIKE '%boeing%'" -i

# Output formats
hangar sql "SELECT * FROM status_codes" --output-format json
hangar sql "SELECT * FROM status_codes" --output-format csv
```

### Data Management

```bash
# Update data
hangar update       # Full pipeline: fetch → normalize → publish

# Individual steps
hangar fetch        # Download FAA data
hangar normalize    # Parse to Parquet
hangar publish      # Build DuckDB indexes

# Check status
hangar status
```

## Data Freshness

FAA releases updated data weekly. Hangarbay warns when data is 30+ days old.

**Check age:**
```python
info = hb.status()
if info['age_days'] > 30:
    print(f"Data is {info['age_days']} days old - consider updating")
    hb.load_data(force=True)
```

**Force update:**
```python
hb.load_data(force=True)  # Re-download even if data exists
```

## Examples from LAPD Fleet Analysis

### Basic Fleet Lookup

```python
import hangarbay as hb

# Load data (one-time setup)
hb.load_data(quiet=True)

# Find LAPD aircraft
lapd = hb.fleet("LAPD|Los Angeles Police")
print(f"Found {len(lapd)} aircraft")

# Display key fields
display_cols = ['n_number', 'maker', 'model', 'year_mfr', 'reg_status']
print(lapd[display_cols])
```

### Fleet Summary Statistics

```python
# Owner name variations
print("Owner variations:")
print(lapd['owner_name'].unique())

# Manufacturer breakdown
print("\nManufacturers:")
print(lapd['maker'].value_counts())

# Valid registrations
valid_count = (lapd['reg_status'] == 'Valid').sum()
print(f"\nValid registrations: {valid_count}/{len(lapd)}")
```

### Combined Municipal Analysis

```python
# LAPD + other city departments
la_city = hb.fleet("City of Los Angeles", state="CA")
all_city = pd.concat([lapd, la_city]).drop_duplicates(subset=['n_number'])

print(f"Total LA municipal aircraft: {len(all_city)}")

# By department
print("\nFleet by Agency:")
agency_counts = all_city.groupby('owner_name').size().sort_values(ascending=False)
for owner, count in agency_counts.items():
    print(f"  {owner}: {count}")

# Average age
valid_years = all_city[all_city['year_mfr'].notna()]
avg_age = 2026 - valid_years['year_mfr'].mean()
print(f"\nAverage age: {avg_age:.1f} years")
```

### Individual Aircraft Details

```python
# Look up specific aircraft
aircraft = hb.search("N221LA")

# Display key information
if len(aircraft) > 0:
    a = aircraft.iloc[0]
    print(f"N-Number: N{a['n_number']}")
    print(f"Make/Model: {a['maker']} {a['model']}")
    print(f"Year: {int(a['year_mfr'])}")
    print(f"Owner: {a['owner_name']}")
    print(f"Location: {a['city']}, {a['state']}")
```

### Export for Further Analysis

```python
# Save to CSV
lapd.to_csv('lapd_fleet.csv', index=False)
print(f"Exported {len(lapd)} aircraft to lapd_fleet.csv")
```

## Workflow Tips

1. **Start with load_data()**: Always ensure data is available before querying
2. **Use decoded views**: `aircraft_decoded` and `owners_clean` are easier to work with
3. **OR logic for names**: Use `|` in fleet searches to catch name variations
4. **Check data age**: FAA data updates weekly - refresh periodically
5. **Filter by state**: Helps narrow large fleet searches
6. **Export for sharing**: Save DataFrames to CSV for reports or further analysis

## Data Quality Notes

- N-numbers stored without "N" prefix in database (e.g., "221LA" not "N221LA")
- Owner names vary (e.g., "LAPD" vs "Los Angeles Police Department")
- Some records have missing or null values for certain fields
- Registration status codes are decoded in `aircraft_decoded` view
- Addresses are standardized in `owners_clean` view

## Troubleshooting

**"No data found" error:**
```python
hb.load_data()  # Download data first
```

**Stale data warning:**
```python
hb.load_data(force=True)  # Force re-download
```

**Empty results from fleet search:**
- Try broader search terms with OR logic: `hb.fleet("LAPD|Los Angeles Police|LA Police")`
- Check state filter is correct
- Verify owner name spelling with exploratory queries

**CLI command not found:**
```bash
pip install hangarbay
which hangar  # Should show path to hangar command
```

## Repository

Source code and examples: `~/github/hangarbay`

- Python API: `hangarbay/api.py`
- CLI implementation: `hangarbay/cli.py`
- Example notebook: `examples/lapd_fleet_analysis.ipynb`
- Documentation: `README.md`
