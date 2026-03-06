# textcharts

Beautiful text based charts for your terminal — zero dependencies.

15 chart types with Unicode box-drawing, ANSI colors, and automatic terminal
width detection. Pure Python, no external dependencies, Python 3.10+.

## Install

```bash
pip install textcharts
```

## Quick Start

```python
from textcharts import BarChart, BarData, ChartOptions

data = [
    BarData(label="Python", value=89.5, is_best=True),
    BarData(label="Rust", value=95.2),
    BarData(label="Go", value=78.0),
    BarData(label="Java", value=72.3, is_worst=True),
]
chart = BarChart(data=data, title="Language Benchmark", metric_label="score")
print(chart.render())
```

```
Language Benchmark (score)
────────────────────────────────────────────────────────────────────────────────
Rust   ████████████████████████████████████████████████████████████████████ 95.2
Python ██████████████████████████████████████████████████████████████████   89.5
Go     █████████████████████████████████████████████████████████             78
Java   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             72.3
```

## Chart Types

| Chart              | Class               | Data Model           |
| ------------------ | ------------------- | -------------------- |
| Bar chart          | `BarChart`          | `BarData`            |
| Histogram          | `Histogram`         | `HistogramBar`       |
| Heatmap            | `Heatmap`           | matrix + labels      |
| Box plot           | `BoxPlot`           | `BoxPlotSeries`      |
| Line chart         | `LineChart`         | `LinePoint`          |
| Scatter plot       | `ScatterPlot`       | `ScatterPoint`       |
| Comparison bar     | `ComparisonBar`     | `ComparisonBarData`  |
| Diverging bar      | `DivergingBar`      | `DivergingBarData`   |
| Summary box        | `SummaryBox`        | `SummaryStats`       |
| Percentile ladder  | `PercentileLadder`  | `PercentileData`     |
| Normalized speedup | `NormalizedSpeedup` | `SpeedupData`        |
| Stacked bar        | `StackedBar`        | `StackedBarData`     |
| Sparkline table    | `SparklineTable`    | `SparklineTableData` |
| CDF chart          | `CDFChart`          | `CDFSeriesData`      |
| Rank table         | `RankTable`         | `RankTableData`      |

## Configuration

```python
from textcharts import ChartOptions, ColorMode

opts = ChartOptions(
    use_color=True,       # Auto-detect ANSI color support; set False to force plain text
    use_unicode=True,     # Unicode box-drawing characters
    width=80,             # Chart width (None for auto-detect)
    theme="dark",         # "dark" or "light"
)
```

`use_color=True` respects terminal detection and `NO_COLOR`. In non-interactive
contexts, renders default to plain text without ANSI escapes.

Heatmaps support `color_scheme="diverging"` (default) or
`color_scheme="sequential"`.

Matrix-based APIs require exact dimensions:
- `len(row_labels) == len(matrix)`
- every matrix row length must equal `len(col_labels)`

## Features

- **Zero dependencies** — pure Python, stdlib only
- **15 chart types** — from simple bars to heatmaps and CDF curves
- **Terminal-aware** — auto-detects width, color support, and Unicode capability
- **Best/worst highlighting** — automatic annotation of extreme values
- **Typed** — full type hints with `py.typed` marker (PEP 561)

## License

MIT
