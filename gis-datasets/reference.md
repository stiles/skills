# GIS assets — full catalog

Companion to [SKILL.md](SKILL.md). Use the defaults tables there first.

- National: `https://stilesdata.com/gis/<filename>` ↔ `s3://stilesdata.com/gis/<filename>`
- Korea: `https://stilesdata.com/gis/korea/<filename>` ↔ `s3://stilesdata.com/gis/korea/<filename>`
- Los Angeles: `https://stilesdata.com/la-geography/<filename>` ↔ `s3://stilesdata.com/la-geography/<filename>`

Source of truth for LA layer names: `~/code/la-geography/config/layers.yml`.  
Korea processing / admin glossary: `~/code/korea-geography`.

## National defaults (repeat)

| Role | Filename |
|------|----------|
| States | `usa_states_esri_simple.json` |
| Counties (join geometries) | `usa_counties_esri_simple.json` |
| Counties (generation demos) | `usa_counties_demos_generations.geojson` |
| CONUS states | `usa_states_conus.geojson` |
| CONUS outline (light) | `usa_boundaries_lakes_conus.geojson` |
| Cities | `us_cities_major_pop_esri.geojson` |
| Hex 50 mi | `us_hexgrid_50_miles.geojson` |

## Boundaries and states

| File | ~Size | Geometry | What it is | Prefer? |
|------|-------|----------|------------|---------|
| `usa_states_esri_simple.json` | 284 KiB | MultiPolygon × 51 | Esri-style states; `STATE_FIPS`, `STATE_NAME`, `STATE_ABBR` + older pop attrs | **Default** |
| `usa_states_conus.geojson` | 565 KiB | MultiPolygon × 49 | Same attribute family; lower 48 + DC | When you want CONUS without filtering |
| `us_states.geojson` | 666 KiB | MultiPolygon × 51 | Near Esri states export (`OBJECTID`, …) | Only if you already depend on it |
| `usa_states_demos_generations.geojson` | 1.6 MiB | MultiPolygon × 51 | State polygons + generation / income-style fields; id in `ID` | State-level demos |
| `usa_boundaries_lakes_conus.geojson` | 190 KiB | 1× MultiPolygon | Light CONUS country outline w/ lakes | **Default outline** |
| `usa_boundary.geojson` | 1.5 MiB | 1× MultiPolygon | Heavier admin outline (`ADMIN`, `ISO_A3`) | Specialty |
| `usboundaryconus.geojson` | 1.5 MiB | 1× MultiPolygon | **Identical bytes** to `usa_boundary.geojson` | Do not treat as a second dataset |
| `us_mainland_outline_500k.geojson` | 578 KiB | LineString × 306 | Mainland outline **lines** (`TYPE`, `R_STATEFP`, `L_STATEFP`) | Line overlays only |
| `usboundaryconus` / lakes / 500k | — | — | — | See rows above |

## Counties

| File | ~Size | Geometry | What it is | Prefer? |
|------|-------|----------|------------|---------|
| `usa_counties_esri_simple.json` | 37 MiB | Polygon × ~3143 | `fips`, `name`, `state_name`, `state_fips`, `cnty_fips` + older demos/ag fields | **Default join layer** |
| `usa_counties_demos_generations.geojson` | 18 MiB | Polygon × ~3142 | Esri updated demos; FIPS in `ID`; generations, income, race | **Default for generation maps** |
| `counties_lakes_cnn.geojson` | 4.7 MiB | — | Legacy lakes-clipped counties; CNN-era filename | Avoid for new work |
| `west_coast_counties_esri.geojson` | 57 KiB | MultiPolygon × 25 | CA/OR/WA (and similar) subset only | Regional demos only |

## Cities and places

| File | ~Size | Geometry | What it is | Prefer? |
|------|-------|----------|------------|---------|
| `us_cities_major_pop_esri.geojson` | 1.3 MiB | Point × ~4186 | Esri major cities; pop + FIPS | **Default** |
| `us_census_places_with_population.geojson` | 194 KiB | Point × 871 | Compact `name`/`pop`/`st` | Small label sets |
| `usa_cities.geojson` | 1.0 MiB | — | Overlapping city dump | Legacy |
| `usa-cities.geojson` | 701 KiB | — | Hyphenated legacy name | Legacy |
| `usa_cities_conus.geojson` | 3.7 MiB | — | CONUS-oriented cities extract | Legacy / specialty |
| `USA_Major_Cities.geojson` | 3.7 MiB | — | Another major-cities export | Legacy |
| `US_place_2019.zip` | 19 MiB | ZIP | 2019 places package | When you need the full places shapefile set |

## Hex grids

| File | ~Size | Cells | Notes |
|------|-------|-------|-------|
| `us_hexgrid_20_miles.geojson` | 2.3 MiB | — | Prefer this naming family |
| `us_hexgrid_20_miles_with_states.geojson` | 2.5 MiB | — | Hexes tagged/associated with states |
| `us_hexgrid_25_miles.geojson` | 1.4 MiB | — | |
| `us_hexgrid_25_miles_with_states.geojson` | 1.6 MiB | — | |
| `us_hexgrid_50_miles.geojson` | 380 KiB | ~819 | Geometry-only props; **default 50 mi** |
| `us_hexgrid_50_miles_with_states.geojson` | 419 KiB | — | |
| `usa_50-mile_grid.geojson` | 2.4 MiB | ~4092 | Different grid (`id`, bbox cols) — not the same as `us_hexgrid_50_miles` |

## Tracts and ZIPs

| File | ~Size | Notes |
|------|-------|-------|
| `usa_tracts_2020_simple.zip` | 116 MiB | Simplified 2020 tracts (shapefile zip). Cache; do not re-download casually |
| `usa_tracts_demos_generations.geojson` | 13 MiB | Tracts + generation populations |
| `usa_zips_centroids.geojson` | 17 MiB | ZIP centroids |
| `zips_poly.geojson` | 73 MiB | ZIP polygons |
| `zip_code_demographics_esri.geojson` | 160 MiB | ZIP polygons + economic demos — last resort for national ZIP maps |

## Los Angeles

| File | Notes |
|------|-------|
| `la_city_boundary.geojson` | City limit polygon |
| `la_city_hoods_county_munis.geojson` | Neighborhoods + municipal layers (common in LA projects) |
| `la_city_neighborhoods.geojson` | Neighborhood polygons |

## Countries and oceans

| File | ~Size | Notes |
|------|-------|-------|
| `countries.geojson` | 24 MiB | Global countries — heavy; subset before plotting |
| `north_pacific_ocean_boundary.geojson` | 361 KiB | Ocean basin boundary specialty layer |

## Naming patterns

- `usa_*` / `us_*` / `USA_*` are not a reliable hierarchy — use the defaults table
- `*_conus*` usually excludes Alaska and Hawaii (and often PR)
- `*_esri_simple*` → good general-purpose geometries
- `*_demos_generations*` → Esri demographic / generation attributes; FIPS often in `ID`
- `*_cnn*` → legacy; prefer Esri simples for new maps

## Korea

Prefix: `https://stilesdata.com/gis/korea/`. Built in `~/code/korea-geography` from NGII (Korean Geographic Information Institute) bilingual layers, plus GADM/Esri-derived outlines. Filenames ending in `_combined` merge English and Korean attribute fields onto one GeoJSON.

### Korea defaults

| Role | File |
|------|------|
| Peninsula outline | `unified_korea_boundary.geojson` |
| Admin polygons | `administrative_boundaries_combined.geojson` |
| DMZ | `demilitarized_zone_combined.geojson` |
| Place labels | `place_names_combined.geojson` |

### Full Korea layer list

| File | ~Size | Geometry | Features | Key name fields |
|------|-------|----------|----------|-----------------|
| `unified_korea_boundary.geojson` | 0.6 MiB | MultiPolygon | 3 | `COUNTRY_1` / `COUNTRY_2` (GADM-style) |
| `administrative_boundaries_combined.geojson` | 67 MiB | Polygon | ~9933 | `MNG_NAM_eng`, `MNG_NAM_kor`, `MNG_ARA_*` |
| `national_boundaries_combined.geojson` | 7 MiB | Polygon | ~2933 | `NAT_NAM_eng`, `NAT_NAM_kor` |
| `demilitarized_zone_combined.geojson` | 47 KiB | LineString | 1 | `DMZ_LEN_eng` / `_kor` |
| `coastal_lines_combined.geojson` | 9 MiB | LineString | ~3081 | `COD_LEN_*` |
| `rivers_combined.geojson` | 14 MiB | LineString | ~1204 | `RIV_NAM_eng`, `RIV_NAM_kor` |
| `roads_combined.geojson` | 23 MiB | LineString | ~1302 | `ROD_NAM_eng`, `ROD_NAM_kor` |
| `railways_combined.geojson` | 21 MiB | LineString | ~729 | `RAL_NAM_eng`, `RAL_NAM_kor` |
| `place_names_combined.geojson` | 0.3 MiB | Point | ~1352 | `KOR_NAM_eng`, `KOR_NAM_kor` |
| `premier_points_combined.geojson` | 0.5 MiB | Point | ~2070 | `MNG_NAM_eng`, `MNG_NAM_kor` |
| `mountain_peaks_combined.geojson` | 55 KiB | Point | ~181 | `MOT_NAM_*`, `MOT_HIG_*` |
| `cultural_locations_combined.geojson` | 15 KiB | Point | ~57 | `CUL_NAM_eng`, `CUL_NAM_kor` |
| `ocean_points_combined.geojson` | 9 KiB | Point | ~31 | `OCN_NAM_eng`, `OCN_NAM_kor` |
| `latitude_longitude_lines_combined.geojson` | 95 KiB | LineString | ~22 | `LAT_NAM_*` |

Cache `administrative_boundaries_combined`, `roads_combined` and `railways_combined` before interactive notebook use.

South / North admin vocabulary (도, 시, 구, 군, 동, etc.) is summarized in `~/code/korea-geography/README.md`.

## LA geography

Prefix: `https://stilesdata.com/la-geography/`. Maintained by `~/code/la-geography`. Sync via `python scripts/s3_sync.py`. Index: `metadata.json`.

Demographics: `{layer}_demographics.parquet` beside each polygon GeoJSON when apportionment has been run.

Lookup API: `https://api.stilesdata.com/la-geography/lookup?lat=…&lon=…`.

Prefer this prefix over any same-named files under `gis/` (legacy copies such as `gis/la_city_boundary.geojson`).

### LA defaults

| Role | File | Id / notes |
|------|------|------------|
| County-wide neighborhoods | `la_neighborhoods_comprehensive.geojson` | `slug`; ~270; **default “where do you live?”** |
| Regions | `la_regions.geojson` | 16 regions; dissolved from comprehensive |
| City boundary | `la_city_boundary.geojson` | City of LA |
| City neighborhoods only | `la_city_neighborhoods.geojson` | ~114 inside city |
| Neighborhood councils | `la_city_neighborhood_councils.geojson` | ~99 |
| Council districts | `la_city_council_districts.geojson` | `district` / 15 |
| County boundary | `la_county_boundary.geojson` | Mainland + islands |
| County cities | `la_county_cities.geojson` | Cities + unincorporated; ~14 MB |
| LAPD divisions | `lapd_divisions.geojson` | `prec` / `aprec`; 21 |
| LAPD bureaus | `lapd_bureaus.geojson` | 4 |
| LAPD reporting districts | `lapd_reporting_districts.geojson` | `repdist`; ~1191; heavy |
| Freeways | `la_freeways.geojson` | lines |
| Metro lines | `la_metro_lines.geojson` | rail + BRT |

### Full LA layer list

| File | Kind | Approx count | Id field |
|------|------|--------------|----------|
| `la_neighborhoods_comprehensive.geojson` | polygon | ~270 | `slug` |
| `la_regions.geojson` | polygon | 16 | `slug` |
| `la_city_boundary.geojson` | polygon | 1 | — |
| `la_city_neighborhoods.geojson` | polygon | 114 | `objectid` |
| `la_city_neighborhood_councils.geojson` | polygon | ~99 | — |
| `la_city_council_districts.geojson` | polygon | 15 | `district` |
| `la_city_parks.geojson` | polygon | ~561 | `park_id` |
| `la_county_boundary.geojson` | polygon | 1 (dissolved) | — |
| `la_county_cities.geojson` | polygon | ~88+ | `city_name` |
| `la_county_school_districts.geojson` | polygon | 85 | `abbr` |
| `la_freeways.geojson` | line | clipped NHS | `routeid` |
| `la_metro_lines.geojson` | line | ~17 | `label` |
| `lapd_bureaus.geojson` | polygon | 4 | `bureau` |
| `lapd_divisions.geojson` | polygon | 21 | `prec` |
| `lapd_reporting_districts.geojson` | polygon | ~1191 | `repdist` |
| `lapd_station_locations.geojson` | point | 21 | `prec` |
| `lacofd_station_boundaries.geojson` | polygon | ~175 | `stanum` |
| `lacofd_station_locations.geojson` | point | ~176 | `stanum` |
| `lafd_station_boundaries.geojson` | polygon | ~102 | `precinctid` |
| `la_county_airports.geojson` | point | 16 | — |
| `la_county_airport_noise_contours.geojson` | polygon | ~35 | — |
| `la_county_election_precincts.geojson` | polygon | ~1502 | `precinct` |
| `metadata.json` | catalog | — | — |

Not every layer in `layers.yml` is guaranteed on S3 until `s3_sync.py upload` has been run for it. If a URL 404s, check the repo’s `data/standard/` or sync from that project.

### Legacy under `gis/` (avoid for LA work)

Older projects sometimes used:

- `https://stilesdata.com/gis/la_city_boundary.geojson`
- `https://stilesdata.com/gis/la_city_hoods_county_munis.geojson`
- `https://stilesdata.com/gis/la_city_neighborhoods.geojson`

For new work, switch to `la-geography/` equivalents (`la_neighborhoods_comprehensive` replaces the ad-hoc hoods/munis mashup in most cases).

## Maintenance tips

- National: put new canonical files in SKILL.md defaults; demote near-duplicates here.
- LA: add layers in `~/code/la-geography/config/layers.yml`, publish with `s3_sync.py`, then mirror the name here and in SKILL.md defaults when it becomes a common starting point.
- If two national files hash equal (as with `usa_boundary` / `usboundaryconus`), document once and stop listing them as alternatives.
- After schema changes, update join-key notes in SKILL.md first.
