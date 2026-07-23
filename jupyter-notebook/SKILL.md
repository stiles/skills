---
name: jupyter-notebook
description: >-
  Create or extend JupyterLab notebooks using uv, the _template layout and
  reproducible data workflows. Use when starting a new notebook, scaffolding a
  topic folder, fetching or analyzing data in .ipynb files, adding charts or
  exports, or when the user mentions Jupyter, JupyterLab, uv sync, live data
  vs local downloads, or the notebooks collection template.
---

# Create Jupyter notebooks

Follow the structure and habits in `~/code/notebooks/_template/template.ipynb` and `~/code/notebooks/README.md`. Prefer live, reproducible fetches over checked-in raw dumps.

## Environment (uv)

This collection uses [uv](https://github.com/astral-sh/uv) with Python 3.13. Dependencies live in `pyproject.toml` and `uv.lock`.

```bash
brew install uv          # once
uv sync                  # create .venv from the lockfile
uv run jupyter lab       # start JupyterLab
uv add some-package      # add a dependency when needed
```

- Run package installs through `uv add`, not pip into a random env.
- Prefer libraries already in the project (`pandas`, `requests`, `altair`, `geopandas`, `jupyter-black`, etc.) before adding new ones.
- Do not commit `.venv/` or `.ipynb_checkpoints/`.

## Topic folder layout

Put each project in its own directory under the notebooks repo:

```
topic-name/
├── 00-fetch-something.ipynb
├── 01-analyze.ipynb          # optional multi-step series
├── data/
│   ├── raw/                  # only if a local snapshot is unavoidable
│   └── processed/            # dated exports from the notebook
└── visuals/                  # chart PNGs for GitHub rendering
```

Number notebooks when there is a sequence (`00-`, `01-`, …). Copy from `_template/template.ipynb` rather than inventing a new outline.

## Notebook outline (match the template)

Use markdown section cells with horizontal rules (`---`) between major parts.

1. **Title** — `# Project name` plus a one-line blockquote: what the notebook does and a link to the data source.
2. **Import Python tools and Jupyter config** — imports, then `jupyter_black.load()`, pandas display options, Altair max-rows disable, `today = pd.Timestamp("today").strftime("%Y-%m-%d")`.
3. **Fetch** — read from the live source when possible.
4. **Process** — clean dates, standardize categories, rename columns.
5. **Aggregate** — groupbys and summary tables.
6. **Charts** — Altair (or similar); save PNG under `visuals/` and display with `Image` so charts show on GitHub.
7. **Exports** — write dated files under `data/processed/`.
8. **Metadata** — provenance, column descriptions, caveats.

Default import / config pattern:

```python
import json

import altair as alt
import geopandas as gpd
import jupyter_black
import pandas as pd
import requests
from IPython.display import Image

jupyter_black.load()

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
pd.options.display.max_colwidth = None

alt.data_transformers.disable_max_rows()

today = pd.Timestamp("today").strftime("%Y-%m-%d")
```

Include only imports the notebook uses. Keep a browser-like `headers` dict in Fetch when calling public HTTP APIs.

## Data: live first, reproducible always

- Prefer API, CSV/JSON over HTTP, or other remote sources over files in `data/raw/`.
- Hard-code the source URL (or clearly documented API endpoint) in the Fetch section so anyone can re-run.
- When credentials are required, load them from an ignored local file (for example `creds.py` / `credentials.json`); never commit secrets.
- If a local download is unavoidable, document why, keep the fetch cell that produced it and treat `data/raw/` as a cache—not the source of truth.
- Export a copy with the run date (if needed): `data/processed/NAME_{today}.csv` (same pattern for `.json` / `.geojson`).

```python
# df.to_json(f"data/processed/NAME.json", indent=4, orient="records")
# df.to_json(f"data/processed/NAME_{today}.json", indent=4, orient="records")
```

## Charts

Build charts in code (Altair preferred in this collection). For anything that should render on GitHub:

```python
chart.save("visuals/chart.png")
Image(filename="visuals/chart.png")
```

Keep chart titles factual. Avoid decorative styling that needs a manual screenshot.

## Comments and markdown

- Markdown cells state purpose; code comments explain non-obvious choices (API quirks, join keys, filters).
- Prefer short factual notes over tutorial filler.
- Section headers in the template style: `#### Read data from the source...` under `## Fetch`, etc.
- Apply [ai-writing](../ai-writing/SKILL.md) habits in prose cells: no legacy/significance padding or chatbot closers.

## Outputs: do not commit notebook noise

Before committing:

- Clear execution outputs that dump large DataFrames, long `print` traces or interactive widgets.
- Do not leave `df.head()`, `df.tail()`, `df` or `print(df)` outputs saved in the `.ipynb` unless the user explicitly wants a small illustrative preview kept.
- Prefer empty `outputs: []` on data-inspection cells; charts may keep a small PNG reference via `Image` only when intentional.
- Restart/run all should work from a clean slate given network access and any local creds.

When editing notebooks with tools, strip bulky dataframe outputs rather than writing them into the file.

## Reproducibility checklist

- [ ] Title cell links the data source
- [ ] `uv sync` + `uv run jupyter lab` is enough to run (plus any documented creds)
- [ ] Fetch uses a live URL/API when possible
- [ ] Transforms are in code, not manual spreadsheet edits
- [ ] `today` stamps processed exports
- [ ] Charts save under `visuals/` when they matter for GitHub
- [ ] No secrets in the notebook
- [ ] No committed DataFrame printouts or giant HTML table outputs
- [ ] Comments explain non-obvious steps

## Workflow for new notebooks

1. Create `topic-name/` (and `data/processed/`, `visuals/` as needed).
2. Copy `_template/template.ipynb` and rename (`00-short-purpose.ipynb`).
3. Fill title, source link and Fetch first; prove the data loads.
4. Process → Aggregate → Charts → Exports → Metadata.
5. Clear dataframe/print outputs; run once to verify.
6. Commit notebook structure, processed outputs only if they are meant to be shared and are reasonably sized; keep raw caches out of git when they are regenerable.
