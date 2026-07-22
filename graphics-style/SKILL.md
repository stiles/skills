---
name: graphics-style
description: >-
  Visual design principles for charts and maps in D3, Matplotlib, Seaborn,
  Altair, CSS or chorokit. Use when creating or styling charts, choropleths,
  legends, typography, color palettes, annotations or map projections to keep
  graphics consistent and readable.
metadata:
  short-description: Chart and map design standards
---

# Graphics style guide

Visual design principles for charts and maps in CSS, D3, Python charting libraries and [chorokit](https://github.com/mstiles/chorokit).

---

## Key principles

1. **Show the data**  
   Let the data speak. Avoid excessive decoration or "chartjunk." Clarity beats cleverness.

2. **Maximize data-ink ratio**  
   Use ink only if it communicates data. Gridlines, borders and shading should be minimal or purposeful.

3. **Avoid distortion**  
   Axes should be honest. Never manipulate scale to exaggerate trends — especially zero baselines on bar charts.

4. **Use color intentionally**  
   Color should signal meaning, not just decorate. Use it sparingly to highlight or group — not distract. Bar charts should not use multiple colors for a single series.

5. **Minimize cognitive load**  
   Make charts easy to scan. Avoid unnecessary legends, rotate labels only if needed and group related elements. Skip axis titles when context is clear (for example years without a "Year" label).

6. **Tell a story, not just a stat**  
   Every chart should answer: Why does this matter? A headline, dek or annotation often helps.

7. **Respect hierarchy**  
   Visual and typographic hierarchy should match informational hierarchy. What matters most should pop. Use sentence case for headlines — not title case.

8. **Use appropriate chart types**  
   Bar for comparisons, line for trends, scatter for correlations. Pie charts are almost never the answer.

9. **Label directly where possible**  
   Prefer labels next to the data over legends and tooltips.

10. **Be transparent about sources and uncertainty**  
    Cite data sources clearly. If data is incomplete or modeled, say so. On maps, show a No-data swatch when values are missing.

---

## Typography

Default chart font: **Roboto** (fallback: system sans-serif / DejaVu Sans in Matplotlib).

Choropleth maps via chorokit use **Barlow** (bundled with the package). Prefer Barlow for map figures so they match chorokit output; use Roboto for non-map charts unless the figure is part of a map package.

| Element                | Font           | Size | Weight | Color   |
|------------------------|----------------|------|--------|---------|
| Headline               | Roboto         | 18px | Bold   | #262626 |
| Dek (subhead)          | Roboto         | 15px | Light  | #262626 |
| Chart title (normal)   | Roboto         | 14px | Medium | #262626 |
| Chart title (headless) | Roboto         | 16px | Bold   | #262626 |
| Annotation text        | Roboto         | 12px | Light  | #262626 |
| Endpoint annotations   | Roboto         | 12px | Bold   | #262626 |
| Source / note          | Roboto         | 12px | Light  | #8e8e8e |
| Axis labels            | Roboto         | 12px | Light  | #A6A6A6 |
| Short label highlight  | Roboto         | 12px | Medium | #262626 |

### Map / chorokit type defaults

From chorokit `Theme` (Barlow):

| Element   | Size | Weight | Color |
|-----------|------|--------|-------|
| Title     | 18pt | Bold   | #333  |
| Subtitle  | 12pt | Regular| #333  |
| Source    | 9pt  | Regular| #666  |
| Legend title | 10pt | Bold | #333 |
| Legend ticks | 9pt | Regular | #333 |

---

## Color palette

### Core colors (charts)

- **Text / labels / body:** `#262626`
- **Source / note / byline:** `#8e8e8e`
- **Axis labels:** `#A6A6A6`
- **Gridlines:** `#B1B1B1`
- **Chart background:** `#FEFEFE`

### Category colors

Use for distinguishing a small number of categories:

- `#5194C3` – Blue
- `#F8C153` – Yellow
- `#C52622` – Red
- `#53A796` – Teal
- `#F18851` – Orange
- `#7C4EA5` – Purple

For sequential or diverging scales (especially maps), prefer ColorBrewer ramps (`Blues`, `YlOrRd`, `RdBu_r`, etc.) with a fixed class count.

---

## Spacing guidelines

| Measurement                 | Value      |
|-----------------------------|------------|
| Between headline and dek    | 30px       |
| Between dek and chart title | 25px       |
| Line height baseline gap    | 15–20px    |
| Source line spacing         | 8px below chart |

---

## Chart design rules

### Grid and axes

- **Gridlines:** `#B1B1B1`, 0.5px stroke
- **Axis tick labels:** 12px, `#A6A6A6`, Roboto Light
- **Axis tick count:** 3–4 on mobile, 4–5 on desktop (fewer is better)
- **Zero baseline (when needed):** 0.5px, `#6e6e6e`

### Annotations

- **Endpoint values:** 12px bold (`font-weight: 700`), `#262626`
- **Endpoint circles:** 4px radius, filled with line color, 1.5px white stroke
- **Direct labels** preferred over legends

---

## Map design (chorokit conventions)

When making choropleths, follow chorokit defaults. Prefer `chorokit.plot_choropleth` over hand-rolled Matplotlib maps when the project already uses chorokit.

### Layout

- Figure **width** is set; **height** comes from the projected map aspect plus fixed title, legend and source bands so spacing stays consistent across geographies.
- Typical width: `10`–`12` inches. Margins about `(0.5, 0.5, 0.4, 0.4)` inches (left, right, bottom, top).
- Vertical stack: title → subtitle → legend (top) → map → legend (bottom) → source / credit.
- Export at high DPI (for example `dpi=300`).

### Projection

- Geographic CRS should be projected before plotting.
- Large CONUS extents: **US Albers Equal Area (EPSG:5070)** / `Projection.us_albers()`.
- Local or regional extents: **UTM** zone from the data midpoint.
- Override with an EPSG code, EPSG string or `pyproj.CRS` when the default is wrong.

### Fills, edges and overlays

- Default choropleth edges: white (`#FFFFFF`), ~`0.5` linewidth.
- Missing values: `#E6E6E6` with an automatic **No data** swatch when the legend is shown.
- Boundary overlays (states on counties, etc.): `Overlay` with edge `#666666`, linewidth ~`0.4`, `facecolor="none"`. Election-style maps may use white state lines instead when fills are dark or diverging.

### Legend

- Horizontal only; place **top** (default) or bottom.
- Align **center** or **left** (left sits under the title block).
- Prefer **binned** legends with explicit breaks when the story needs readable classes; continuous when the scale is smooth.
- Classification: `quantiles`, `equal`, `natural` (and friends); optional `log=True` for skewed counts; `round_breaks=True` for nice edges.
- Labels: interval (`a–b`) or boundary ticks; optional compact `k`/`M` and `%` formatting.
- Legend bar outline: light gray (`#cccccc`), ~0.6pt; tick marks off.

### Palettes

- Sequential stories: ColorBrewer sequential (for example `YlOrRd`, `Blues`, `YlGnBu`).
- Diverging stories (margins, change around zero): ColorBrewer diverging with **symmetric breaks** around the midpoint (for example `RdBu_r`).
- Keep class counts modest (often 5–7).

### Hierarchy and basemap cues

- Title and subtitle carry the story; source line is quieter (`#666` / 9pt in chorokit).
- Primary place labels bold when labeling; roads, rivers and disputed areas stay subtle gray.
- Parks / forests: soft green only when those layers matter.
- Use hatch or a distinct missing fill for uncertainty or No-data — do not invent a value color for nulls.

### Minimal chorokit pattern

```python
from chorokit import plot_choropleth, LegendConfig, LayoutConfig, Projection, Overlay
from chorokit.style import Theme

legend = LegendConfig(
    kind="binned",
    title="value per 100k residents",
    location="top",
    scheme="quantiles",
    k=5,
)

layout = LayoutConfig(
    title="Headline in sentence case",
    subtitle="Where and when",
    source="Source: dataset",
    projection=Projection.us_albers(),
    width=12,
    theme=Theme(),  # Barlow
)

fig, ax = plot_choropleth(
    gdf,
    value="value_column",
    cmap="YlOrRd",
    legend=legend,
    layout=layout,
    overlays=[Overlay(gdf=states)],
    edgecolor="#FFFFFF",
    linewidth=0.5,
)
fig.savefig("out.png", dpi=300)
```

---

## Sample Python (Matplotlib) styles

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "Roboto",
    "font.size": 12,
    "axes.titlesize": 12,
    "axes.labelcolor": "#A6A6A6",
    "xtick.color": "#A6A6A6",
    "ytick.color": "#A6A6A6",
    "text.color": "#262626",
    "axes.edgecolor": "#B1B1B1",
    "axes.linewidth": 0.5,
    "figure.facecolor": "#FEFEFE",
    "axes.facecolor": "#FEFEFE",
    "grid.color": "#B1B1B1",
    "grid.linewidth": 0.25,
})
```

If Roboto is not installed, fall back to `"DejaVu Sans"` or the system sans-serif.

---

## CSS reference example

```css
.chart-title {
  font-family: "Roboto", sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #262626;
}

.annotation {
  font-size: 12px;
  font-weight: 300;
  color: #262626;
}

.source-line {
  font-size: 12px;
  font-weight: 300;
  color: #8e8e8e;
  margin-top: 8px;
}
```

---

## D3 style snippets

```js
svg.append("text")
  .attr("class", "chart-title")
  .attr("fill", "#262626")
  .style("font-size", "14px")
  .style("font-family", "Roboto, sans-serif")
  .text("Chart title");

axis.selectAll("text")
  .style("fill", "#A6A6A6")
  .style("font-size", "12px")
  .style("font-family", "Roboto, sans-serif")
  .style("font-weight", "300");

svg.selectAll(".grid line")
  .style("stroke", "#B1B1B1");

svg.append("circle")
  .attr("r", 4)
  .attr("fill", lineColor)
  .attr("stroke", "#fff")
  .attr("stroke-width", 1.5);

svg.append("text")
  .attr("class", "endpoint-label")
  .style("font-size", "12px")
  .style("font-weight", "700")
  .style("fill", "#262626");
```

---

## Seaborn styling example

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

plt.rcParams.update({
    "font.family": "Roboto",
    "font.size": 12,
    "axes.titlesize": 12,
    "axes.labelcolor": "#A6A6A6",
    "xtick.color": "#A6A6A6",
    "ytick.color": "#A6A6A6",
    "text.color": "#262626",
    "axes.edgecolor": "#B1B1B1",
    "axes.linewidth": 0.5,
    "figure.facecolor": "#FEFEFE",
    "axes.facecolor": "#FEFEFE",
    "grid.color": "#B1B1B1",
    "grid.linewidth": 0.25,
})

tips = sns.load_dataset("tips")
sns.barplot(data=tips, x="day", y="total_bill", color="#5194C3")

plt.title("Average total bill by day", loc="left", fontsize=12, fontweight="medium")
plt.xlabel("")
plt.ylabel("")
plt.figtext(0.01, -0.05, "Source: Seaborn tips dataset", fontsize=12, color="#8e8e8e")

plt.tight_layout()
plt.show()
```
