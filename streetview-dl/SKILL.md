---
name: streetview-dl
description: Download high-resolution Google Street View panoramas from command line URLs. Use when working with Street View imagery, downloading panoramas, extracting Street View metadata, processing Google Maps URLs, batch downloading Street View images, discovering historical Street View captures, or building Street View datasets.
---

# streetview-dl

Download high-resolution Google Street View panoramas from Google Maps URLs using the Map Tiles API.

## Installation

```bash
pip install streetview-dl
```

## Authentication

Requires a Google Maps API key with Map Tiles API enabled:

```bash
# Set environment variable
export GOOGLE_MAPS_API_KEY="your_api_key_here"

# Or use --api-key flag
streetview-dl --api-key "your_key" "url"

# Or configure interactively
streetview-dl --configure
```

## Basic Usage

```bash
# Download panorama
streetview-dl "https://www.google.com/maps/@34.13,-118.47,3a,75y,32h,103t/data=..."

# Specify output
streetview-dl --output beach.jpg "url"

# Quality levels (default: medium)
streetview-dl --quality high "url"    # 16K resolution (~10MB, 512 tiles)
streetview-dl --quality medium "url"  # 8K resolution (~4MB, 128 tiles)
streetview-dl --quality low "url"     # 4K resolution (~1MB, 32 tiles)
```

## Metadata Extraction

```bash
# Get metadata without downloading image
streetview-dl --metadata-only "url"

# Download image + save metadata JSON
streetview-dl --metadata "url"

# Metadata includes:
# - pano_id, lat, lng, date (YYYY-MM format)
# - heading, tilt, roll, url_yaw, url_pitch, url_fov
# - image_width, image_height, imagery_type
# - copyright_info, address_components, links
```

## Image Processing

### Field of View Cropping

```bash
# Crop to specific FOV around URL viewing direction
streetview-dl --fov 180 "url"   # Half panorama
streetview-dl --fov 90 "url"    # Narrow architectural view
streetview-dl --fov 270 "url"   # Wide context view
```

### Directional Clipping

```bash
# Forward-facing 180° (from URL heading)
streetview-dl --clip right "url"

# Rear-facing 180° (opposite URL heading)
streetview-dl --clip left "url"

# Note: Clipping overrides --fov if < 180°
```

### Vertical Cropping

```bash
# Default: removes bottom 25% (car blur)
streetview-dl "url"

# Custom bottom crop (keep top 60%)
streetview-dl --crop-bottom 0.6 "url"

# Keep full height
streetview-dl --no-crop "url"
```

### Filters and Adjustments

```bash
# Filters
streetview-dl --filter bw "url"         # Black and white
streetview-dl --filter sepia "url"      # Sepia tone
streetview-dl --filter vintage "url"    # Sepia + desaturated

# Adjustments (range 0.1-3.0)
streetview-dl --brightness 1.2 "url"
streetview-dl --contrast 1.1 "url"
streetview-dl --saturation 0.8 "url"
```

## Historical Imagery

Discover and download historical Street View captures from different time periods:

```bash
# List available historical dates
streetview-dl --historical "url"

# Download all historical panoramas
streetview-dl --historical-download "url"

# More thorough search (slower, more API calls)
streetview-dl --historical --historical-max-depth 10 --historical-max-panoramas 500 "url"
```

**Limitations:**
- Typically finds 3-6 time periods (Google Maps shows more)
- Reliably finds 2015-present imagery
- Recent high-traffic locations yield better results
- Uses 15-100 API calls depending on depth settings

## Batch Processing

```bash
# Create urls.txt with one URL per line
streetview-dl --batch urls.txt --output-dir ./panoramas/
```

## Common Patterns

### Dataset Collection with Metadata

For collecting structured Street View datasets:

```python
import subprocess
import json
import pandas as pd

# Extract metadata for grid of points
rows = []
for lat, lng in grid_points:
    url = f"https://maps.google.com/?q={lat},{lng}"
    
    result = subprocess.run(
        ["streetview-dl", "--metadata-only", url],
        capture_output=True,
        text=True,
        timeout=20
    )
    
    data = json.loads(result.stdout)
    rows.append({
        "grid_lat": lat,
        "grid_lng": lng,
        "pano_id": data.get("pano_id"),
        "pano_lat": data.get("lat"),
        "pano_lng": data.get("lng"),
        "date": data.get("date")
    })

df = pd.DataFrame(rows)
df.to_csv("metadata.csv", index=False)
```

### Deduplicate Panos

Multiple grid points often map to the same panorama:

```python
df = pd.read_csv("metadata.csv")
unique_panos = df.drop_duplicates("pano_id")
```

### Download with Consistent Framing

For comparable imagery across locations:

```python
for _, r in df.iterrows():
    url = f"https://maps.google.com/?q={r.pano_lat},{r.pano_lng}"
    out = f"panos/{r.pano_id}.jpg"
    
    if os.path.exists(out):
        continue
    
    subprocess.run([
        "streetview-dl",
        "--fov", "100",
        "--crop-bottom", "0.7",
        "--output", out,
        url
    ])
```

## Output Formats

```bash
--format jpg|png|webp           # Default: jpg
--jpeg-quality 85               # 1-100, default: 92
--max-width 4096                # Resize if larger
```

## Advanced Options

```bash
--timeout 30                    # Request timeout seconds
--retries 3                     # HTTP retry attempts
--backoff 0.5                   # Retry backoff factor
--concurrency 0                 # Parallel workers (0=auto)
--no-xmp                        # Skip 360° metadata embedding
--verbose                       # Detailed output
--accent-color cyan|yellow      # Terminal color
```

## URL Parameters

Street View URLs contain these parameters:

```
https://www.google.com/maps/@LAT,LNG,3a,75y,32.27h,103.53t/data=...
                              │   │   │  │   │      └─ Pitch/tilt
                              │   │   │  │   └─ Heading (yaw) in degrees
                              │   │   │  └─ FOV in degrees
                              │   │   └─ Street View mode token
                              │   └─ Longitude
                              └─ Latitude
```

- Heading (h): 0°=North, 90°=East, 180°=South, 270°=West
- FOV and clip options use the heading to determine direction
- If URL lacks heading (h), horizontal cropping won't work

## API Costs

Uses Google's Map Tiles API:
- Free tier: 100k requests/month
- Quality impacts tile count: high=512, medium=128, low=32
- Metadata-only calls are cheap (1 request)
- High quality costs ~16x more than low quality

## Troubleshooting

**"--fov doesn't crop"**
- URL must include heading token (e.g., `32.27h`)
- Use Street View share link, not place URL

**"Invalid URL"**
- Ensure URL is a Street View URL with panorama ID
- Check URL isn't truncated

**"API key error"**
- Verify Map Tiles API is enabled
- Check billing is enabled in Google Cloud Console

## Common Use Cases

**Dataset collection**: Use `--metadata-only` first to collect pano_ids and dates, deduplicate, then download sampled images

**Consistent framing**: Use same `--fov` and `--crop-bottom` values across all downloads

**Historical analysis**: Use `--historical-download` to capture change over time

**Web optimization**: Combine `--quality medium`, `--max-width 2048`, `--format webp`

**Architectural documentation**: Use `--quality high`, `--fov 90` for detailed crops
