# JSON Input Formats

Reference for the JSON data format expected by each of the 15 chart types.
These formats apply to both the CLI (`textcharts <type>`) and the MCP server
(`textcharts_<type>` tools).

All examples below can be piped directly to the CLI:

```bash
echo '<json>' | textcharts <type> --no-color
```

---

## bar

Horizontal bar chart for comparing values across categories.

**Format:** list of objects

| Field     | Type    | Required | Description              |
|-----------|---------|----------|--------------------------|
| label     | string  | yes      | Category label           |
| value     | number  | yes      | Numeric value            |
| group     | string  | no       | Optional grouping key    |
| error     | number  | no       | Optional error margin    |
| is_best   | boolean | no       | Mark as best performer   |
| is_worst  | boolean | no       | Mark as worst performer  |

```json
[
  {"label": "Fiction", "value": 18.4, "is_best": true},
  {"label": "Children", "value": 14.2},
  {"label": "Comics", "value": 9.8},
  {"label": "Stationery", "value": 6.1, "is_worst": true}
]
```

**Chart params:** `metric_label` (string), `sort_by` (value | label | none)

---

## histogram

Vertical bar histogram for frequency distribution.

**Format:** list of objects

| Field      | Type    | Required | Description                |
|------------|---------|----------|----------------------------|
| query_id   | string  | yes      | Query or item identifier   |
| latency_ms | number  | yes      | Latency value in ms        |
| platform   | string  | no       | Optional platform name     |
| error      | number  | no       | Optional error margin      |
| is_best    | boolean | no       | Mark as best performer     |
| is_worst   | boolean | no       | Mark as worst performer    |

```json
[
  {"query_id": "Q1", "latency_ms": 120.5},
  {"query_id": "Q2", "latency_ms": 85.3, "is_best": true},
  {"query_id": "Q3", "latency_ms": 210.7, "is_worst": true}
]
```

**Chart params:** `y_label` (string), `sort_by` (query_id | latency),
`max_per_chart` (integer), `show_mean_line` (boolean)

---

## heatmap

Matrix heatmap with color intensity showing value magnitude.

**Format:** single object

| Field      | Type  | Required | Description                              |
|------------|-------|----------|------------------------------------------|
| matrix     | array | yes      | 2D array of numbers (rows x cols); null for missing |
| row_labels | array | yes      | Labels for each row                      |
| col_labels | array | yes      | Labels for each column                   |

```json
{
  "matrix": [
    [1.2, 3.4, 2.1],
    [4.5, null, 1.8],
    [2.3, 3.1, 5.0]
  ],
  "row_labels": ["Row A", "Row B", "Row C"],
  "col_labels": ["Col 1", "Col 2", "Col 3"]
}
```

**Chart params:** `value_label` (string), `x_label` (string),
`show_values` (boolean), `color_scheme` (diverging | sequential)

---

## boxplot

Box plot showing distribution with quartiles, whiskers, and outliers.

**Format:** list of objects

| Field  | Type   | Required | Description              |
|--------|--------|----------|--------------------------|
| name   | string | yes      | Series name              |
| values | array  | yes      | Array of numeric values  |

```json
[
  {"name": "Server A", "values": [12, 15, 14, 18, 22, 13, 16, 45]},
  {"name": "Server B", "values": [8, 9, 11, 10, 12, 9, 10, 11]}
]
```

**Chart params:** `y_label` (string), `show_stats` (boolean),
`show_mean` (boolean)

---

## line

Line chart for time series or trend visualization.

**Format:** list of objects

| Field  | Type   | Required | Description                    |
|--------|--------|----------|--------------------------------|
| series | string | yes      | Series name for grouping       |
| x      | number | yes      | X-axis value (numeric or string) |
| y      | number | yes      | Y-axis value                   |
| label  | string | no       | Optional point label           |

```json
[
  {"series": "Sales", "x": 1, "y": 100},
  {"series": "Sales", "x": 2, "y": 140},
  {"series": "Sales", "x": 3, "y": 120},
  {"series": "Costs", "x": 1, "y": 80},
  {"series": "Costs", "x": 2, "y": 90},
  {"series": "Costs", "x": 3, "y": 85}
]
```

**Chart params:** `x_label` (string), `y_label` (string),
`show_trend` (boolean)

---

## scatter

Scatter plot for comparing two dimensions with optional Pareto frontier.

**Format:** list of objects

| Field     | Type    | Required | Description               |
|-----------|---------|----------|---------------------------|
| name      | string  | yes      | Point label               |
| x         | number  | yes      | X-axis value              |
| y         | number  | yes      | Y-axis value              |
| is_pareto | boolean | no       | Mark as Pareto-optimal    |

```json
[
  {"name": "Alpha", "x": 10, "y": 95, "is_pareto": true},
  {"name": "Beta", "x": 25, "y": 88},
  {"name": "Gamma", "x": 15, "y": 92, "is_pareto": true},
  {"name": "Delta", "x": 40, "y": 70}
]
```

**Chart params:** `x_label` (string), `y_label` (string),
`show_pareto` (boolean)

---

## comparison

Side-by-side paired bar chart comparing baseline vs. comparison values.

**Format:** list of objects

| Field            | Type   | Required | Description                |
|------------------|--------|----------|----------------------------|
| label            | string | yes      | Item label                 |
| baseline_value   | number | yes      | Baseline measurement       |
| comparison_value | number | yes      | Comparison measurement     |
| baseline_name    | string | no       | Name for baseline series   |
| comparison_name  | string | no       | Name for comparison series |

```json
[
  {"label": "Query 1", "baseline_value": 120, "comparison_value": 95},
  {"label": "Query 2", "baseline_value": 200, "comparison_value": 180},
  {"label": "Query 3", "baseline_value": 80, "comparison_value": 110}
]
```

**Chart params:** `metric_label` (string)

---

## diverging

Centered diverging bar chart showing percentage change.

**Format:** list of objects

| Field      | Type   | Required | Description                                       |
|------------|--------|----------|---------------------------------------------------|
| label      | string | yes      | Item label                                        |
| pct_change | number | yes      | Percentage change (negative = improvement)        |

```json
[
  {"label": "Query 1", "pct_change": -25.3},
  {"label": "Query 2", "pct_change": 12.8},
  {"label": "Query 3", "pct_change": -8.1},
  {"label": "Query 4", "pct_change": 45.0}
]
```

**Chart params:** `clip_pct` (number, default 200.0)

---

## summary

Bordered summary box with aggregate statistics.

**Format:** single object

| Field                    | Type    | Required | Description                        |
|--------------------------|---------|----------|------------------------------------|
| title                    | string  | no       | Summary box title                  |
| geo_mean_ms              | number  | no       | Geometric mean in ms               |
| median_ms                | number  | no       | Median in ms                       |
| total_time_ms            | number  | no       | Total time in ms                   |
| geo_mean_baseline_ms     | number  | no       | Baseline geometric mean            |
| geo_mean_comparison_ms   | number  | no       | Comparison geometric mean          |
| total_time_baseline_ms   | number  | no       | Baseline total time                |
| total_time_comparison_ms | number  | no       | Comparison total time              |
| baseline_name            | string  | no       | Baseline label                     |
| comparison_name          | string  | no       | Comparison label                   |
| num_queries              | integer | no       | Number of queries                  |
| num_improved             | integer | no       | Count of improved queries          |
| num_stable               | integer | no       | Count of stable queries            |
| num_regressed            | integer | no       | Count of regressed queries         |
| best_queries             | array   | no       | List of [name, value] pairs for best queries  |
| worst_queries            | array   | no       | List of [name, value] pairs for worst queries |
| environment              | object  | no       | Environment info dict              |
| platform_config          | object  | no       | Platform config dict               |
| metric_label             | string  | no       | Unit label for values (default: "ms") |

```json
{
  "title": "Performance Summary",
  "geo_mean_ms": 142.5,
  "median_ms": 128.0,
  "num_queries": 10,
  "num_improved": 6,
  "num_stable": 2,
  "num_regressed": 2,
  "best_queries": [["Q3", 45.2], ["Q7", 52.1]],
  "worst_queries": [["Q1", 312.5]]
}
```

---

## percentile

Layered percentile bands showing P50/P90/P95/P99 distribution.

**Format:** list of objects

| Field | Type   | Required | Description              |
|-------|--------|----------|--------------------------|
| name  | string | yes      | Series name              |
| p50   | number | yes      | 50th percentile value    |
| p90   | number | yes      | 90th percentile value    |
| p95   | number | yes      | 95th percentile value    |
| p99   | number | yes      | 99th percentile value    |

```json
[
  {"name": "API v1", "p50": 45, "p90": 120, "p95": 200, "p99": 450},
  {"name": "API v2", "p50": 30, "p90": 85, "p95": 140, "p99": 310}
]
```

**Chart params:** `metric_label` (string)

---

## speedup

Log-scale normalized speedup chart relative to a baseline.

**Format:** list of objects

| Field       | Type    | Required | Description                                    |
|-------------|---------|----------|------------------------------------------------|
| name        | string  | yes      | Platform or variant name                       |
| ratio       | number  | yes      | Speedup ratio (2.0 = 2x faster)               |
| is_baseline | boolean | no       | Mark as baseline (ratio=1.0)                   |

```json
[
  {"name": "Baseline", "ratio": 1.0, "is_baseline": true},
  {"name": "Optimized", "ratio": 2.4},
  {"name": "Experimental", "ratio": 0.8}
]
```

**Chart params:** `baseline_name` (string)

---

## stacked

Stacked horizontal bar chart showing component breakdown.

**Format:** list of objects

| Field    | Type   | Required | Description                                    |
|----------|--------|----------|------------------------------------------------|
| label    | string | yes      | Bar label                                      |
| segments | array  | yes      | List of `{phase_name, value, color?}` segments |
| total    | number | no       | Override total (auto-computed if omitted)       |

```json
[
  {
    "label": "Server A",
    "segments": [
      {"phase_name": "Parse", "value": 30},
      {"phase_name": "Execute", "value": 85},
      {"phase_name": "Serialize", "value": 15}
    ]
  },
  {
    "label": "Server B",
    "segments": [
      {"phase_name": "Parse", "value": 25},
      {"phase_name": "Execute", "value": 60},
      {"phase_name": "Serialize", "value": 20}
    ]
  }
]
```

**Chart params:** `metric_label` (string, default "ms")

---

## sparkline

Compact table with inline sparkline mini-charts.

**Format:** single object

| Field     | Type  | Required | Description                                             |
|-----------|-------|----------|---------------------------------------------------------|
| rows      | array | yes      | List of row names                                       |
| columns   | array | yes      | List of `{name, values: {row: number}, higher_is_better?}` |

```json
{
  "rows": ["PostgreSQL", "MySQL", "SQLite"],
  "columns": [
    {
      "name": "Throughput",
      "values": {"PostgreSQL": 1200, "MySQL": 950, "SQLite": 400},
      "higher_is_better": true
    },
    {
      "name": "Latency (ms)",
      "values": {"PostgreSQL": 12, "MySQL": 18, "SQLite": 5}
    }
  ]
}
```

---

## cdf

Cumulative distribution function chart for comparing distributions.

**Format:** list of objects

| Field  | Type   | Required | Description              |
|--------|--------|----------|--------------------------|
| name   | string | yes      | Series name              |
| values | array  | yes      | Array of numeric values  |

```json
[
  {"name": "Before", "values": [10, 15, 12, 18, 22, 30, 45, 50]},
  {"name": "After", "values": [8, 10, 11, 13, 14, 16, 20, 22]}
]
```

**Chart params:** `x_label` (string), `y_label` (string),
`height` (integer)

---

## rank

Competitive ranking table with win counts across queries.

**Format:** single object

| Field     | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| queries   | array  | yes      | List of query names                              |
| platforms | array  | yes      | List of platform names                           |
| times     | object | yes      | Mapping of `"platform,query"` keys to time values |

```json
{
  "queries": ["Q1", "Q2", "Q3"],
  "platforms": ["Postgres", "MySQL"],
  "times": {
    "Postgres,Q1": 120,
    "Postgres,Q2": 85,
    "Postgres,Q3": 200,
    "MySQL,Q1": 130,
    "MySQL,Q2": 90,
    "MySQL,Q3": 180
  }
}
```

---

## Common Options

These options apply to all chart types and can be passed as CLI flags or
top-level keys in MCP tool calls:

| Option      | Type    | Default | Description                          |
|-------------|---------|---------|--------------------------------------|
| title       | string  | —       | Chart title                          |
| subtitle    | string  | —       | Subtitle line displayed below title  |
| width       | integer | auto    | Chart width in characters            |
| height      | integer | auto    | Chart height in rows                 |
| use_color   | boolean | true    | Enable ANSI color output             |
| use_unicode | boolean | true    | Enable Unicode box-drawing           |
| theme       | string  | light   | Color theme (light or dark)          |
| show_legend | boolean | true    | Show chart legend                    |
| show_values | boolean | true    | Show numeric values on chart         |

CLI flags use `--no-color` / `--no-unicode` to disable.
