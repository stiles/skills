---
name: gis-datasets
description: >-
  Choose and load GIS files from stilesdata.com/gis (US national) and
  stilesdata.com/la-geography (Los Angeles). Use when picking states, counties,
  cities, hex grids, tracts, ZIPs, LA neighborhoods, LAPD/LAFD boundaries,
  Metro lines or Census-apportioned demographics; joining on FIPS or layer ids;
  or reading GeoJSON/Parquet from S3 / HTTPS.
metadata:
  short-description: National and LA GIS defaults on stilesdata.com
---

# GIS assets

Two public prefixes on the same bucket (`s3://stilesdata.com/`):

| Prefix | HTTPS base | Use for |
|--------|------------|---------|
| `gis/` | `https://stilesdata.com/gis/` | US states, counties, cities, outlines, hex grids, tracts, ZIPs |
| `la-geography/` | `https://stilesdata.com/la-geography/` | LA city/county boundaries, neighborhoods, police/fire, transit, demos |

Prefer **live HTTPS URLs**. Cache large files locally when needed. Prefer **HTTPS** over `http://`.

- National specialty / legacy inventory: [reference.md](reference.md)
- LA layer definitions and upstream sources live in `~/code/la-geography` (`config/layers.yml`, README)

## How to load

```python
import geopandas as gpd
import pandas as pd

states = gpd.read_file("https://stilesdata.com/gis/usa_states_esri_simple.json")

hoods = gpd.read_file(
    "https://stilesdata.com/la-geography/la_neighborhoods_comprehensive.geojson"
)
demos = pd.read_parquet(
    "https://stilesdata.com/la-geography/la_neighborhoods_comprehensive_demographics.parquet"
)
```

```bash
aws s3 ls s3://stilesdata.com/gis/
aws s3 ls s3://stilesdata.com/la-geography/
```

## National defaults (`gis/`)

| Need | File | Notes |
|------|------|-------|
| US states (50 + DC) | `usa_states_esri_simple.json` | Join on `STATE_FIPS` (2-digit). Also `STATE_NAME`, `STATE_ABBR`. |
| US counties (join geometries) | `usa_counties_esri_simple.json` | ~3143 counties. Join on `fips` (5-digit). ~37 MiB. |
| US counties + generation demos | `usa_counties_demos_generations.geojson` | Join on `ID` → rename to `fips`. ~18 MiB. |
| CONUS states only | `usa_states_conus.geojson` | Lower 48 + DC (49 features). |
| Light CONUS outline | `usa_boundaries_lakes_conus.geojson` | Single multipolygon w/ lakes; ~190 KiB. |
| Major cities (points) | `us_cities_major_pop_esri.geojson` | ~4k places; pop + FIPS fields. |
| Small curated places | `us_census_places_with_population.geojson` | ~870 points; `name`, `pop`, `st`. |
| Hex grid (50 mi) | `us_hexgrid_50_miles.geojson` | Geometry-only; prefer `us_hexgrid_*` over `usa_50-mile_grid`. |

URL: `https://stilesdata.com/gis/<filename>`.

### National join keys

| Layer | ID field | Format |
|-------|----------|--------|
| States | `STATE_FIPS` | 2-digit (`"06"`) |
| Counties simple | `fips` | 5-digit (`"06037"`) |
| Counties demos / generations | `ID` | 5-digit FIPS |
| Cities (Esri major) | `STATE_FIPS` + `PLACE_FIPS` | strings |

Zero-pad after CSV joins: `df["fips"] = df["fips"].astype(str).str.zfill(5)`.

For CONUS-only maps, drop state FIPS `02` / `15` / usually `72`, or start from `usa_states_conus.geojson`. Chorokit `conus()` helps.

## LA defaults (`la-geography/`)

Canonical LA layers are maintained by `~/code/la-geography` and published under `la-geography/`, not `gis/`. If the same basename appears under `gis/` (for example older `la_city_boundary.geojson`), **prefer `la-geography/`**.

| Need | File | Notes |
|------|------|-------|
| “Where do you live?” neighborhoods | `la_neighborhoods_comprehensive.geojson` | **Start here.** ~270 features: cities, unincorporated areas and LA City neighborhoods. `slug`, `name`, `type`, `region`. |
| Broad regions (Westside, SFV, …) | `la_regions.geojson` | 16 regions dissolved from comprehensive neighborhoods. |
| City limit | `la_city_boundary.geojson` | Official City of LA boundary. |
| LA City neighborhoods only | `la_city_neighborhoods.geojson` | ~114 Mapping LA neighborhoods inside the city. |
| Neighborhood councils | `la_city_neighborhood_councils.geojson` | Certified councils. |
| City council districts | `la_city_council_districts.geojson` | 15 districts. |
| County boundary | `la_county_boundary.geojson` | LA County outline. |
| County cities / communities | `la_county_cities.geojson` | Cities + unincorporated; larger file (~14 MB). |
| LAPD divisions | `lapd_divisions.geojson` | 21 divisions. |
| LAPD bureaus | `lapd_bureaus.geojson` | 4 bureaus. |
| LAPD reporting districts | `lapd_reporting_districts.geojson` | ~1,191 districts; heavier. |
| Freeways | `la_freeways.geojson` | Interstates / state highways in county. |
| Metro lines | `la_metro_lines.geojson` | Rail + BRT lines. |

URL: `https://stilesdata.com/la-geography/<filename>`.

### Demographics companions

Most polygon layers have apportioned 2020 Census stats:

`https://stilesdata.com/la-geography/{layer}_demographics.parquet`

Example: `lapd_divisions_demographics.parquet`. Join back to the GeoJSON on the layer’s id/slug field (see `config/layers.yml` in the repo). Catalog index: `https://stilesdata.com/la-geography/metadata.json`.

### Point-in-polygon API

`https://api.stilesdata.com/la-geography/lookup?lat=34.05&lon=-118.25` — returns matching LA geographies for a coordinate (used by whatsmyla.com).

### Other LA layers (same prefix)

Also published: city parks; county school districts; LACoFD / LAFD station boundaries and locations; LAPD station locations; county airports and noise contours; election precincts. Full list and upstream ArcGIS URLs: `~/code/la-geography/config/layers.yml` and [reference.md](reference.md#la-geography).

## Which national file when

**States** — default `usa_states_esri_simple.json`; CONUS `usa_states_conus.geojson`; generation demos `usa_states_demos_generations.geojson`.

**Counties** — join geometries `usa_counties_esri_simple.json`; generation/income demos `usa_counties_demos_generations.geojson`. Avoid `counties_lakes_cnn.geojson` for new work. `west_coast_counties_esri.geojson` is a 25-county subset.

**Outlines** — prefer `usa_boundaries_lakes_conus.geojson`. `usa_boundary.geojson` and `usboundaryconus.geojson` are byte-identical. `us_mainland_outline_500k.geojson` is linework, not a fill.

**Cities** — default `us_cities_major_pop_esri.geojson`; tiny set `us_census_places_with_population.geojson`. Other `usa_cities*` names are legacy overlaps.

**Hex** — `us_hexgrid_{20,25,50}_miles.geojson` (+ `*_with_states`). `usa_50-mile_grid.geojson` is a different denser grid.

### Heavy national files

| File | ~Size | Use when |
|------|-------|----------|
| `usa_counties_esri_simple.json` | 37 MiB | County polygons |
| `zips_poly.geojson` | 73 MiB | ZIP polygons |
| `usa_tracts_2020_simple.zip` | 116 MiB | 2020 tracts |
| `zip_code_demographics_esri.geojson` | 160 MiB | ZIP + economic demos |

Prefer aggregates before pulling ZIP/tract monsters into a notebook.

## Pair with other skills

- Map styling / chorokit: [graphics-style](../graphics-style/SKILL.md)
- Notebook fetch habits: [jupyter-notebook](../jupyter-notebook/SKILL.md)
