# textcharts

Beautiful text based charts for your terminal — zero dependencies.

15 chart types with Unicode box-drawing, ANSI colors, and automatic terminal
width detection. Pure Python, no external dependencies, Python 3.10+.

## Provenance

`textcharts` was extracted from the
[BenchBox](https://github.com/joeharris76/benchbox) project so the terminal
charting layer could be used as a standalone library.

BenchBox remains the source of the most complete end-to-end usage examples for
benchmarking and performance-analysis workflows. For canonical example-driven
documentation, see the
[BenchBox documentation](https://benchbox.dev/docs/index.html).

## Install

```bash
pip install textcharts
```

## Quick Start

```python
from textcharts import BarChart, BarData, ChartOptions

data = [
    BarData(label="Fiction", value=18.4, is_best=True),
    BarData(label="Children", value=14.2),
    BarData(label="Comics", value=9.8),
    BarData(label="Stationery", value=6.1, is_worst=True),
]
chart = BarChart(data=data, title="April Bookstore Revenue", metric_label="k USD")
print(chart.render())
```

```
April Bookstore Revenue (k USD)
────────────────────────────────────────────────────────────────────────────────
Fiction   ████████████████████████████████████████████████████████████████ 18.4
Children  ██████████████████████████████████████████████████               14.2
Comics    ██████████████████████████████                                    9.8
Stationery ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                               6.1
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

## Public API

- Chart classes: `BarChart`, `Heatmap`, `LineChart`, `SummaryBox`, etc.
- Data models: `BarData`, `HistogramBar`, `LinePoint`, `SummaryStats`, etc.
- Configuration: `ChartOptions` and `ColorMode`

## CLI

Generate charts from the command line with JSON input:

```bash
# Pipe JSON data to any chart type
echo '[{"label": "Fiction", "value": 18.4}, {"label": "Comics", "value": 9.8}]' \
  | textcharts bar --title "Revenue" --no-color

# Read from a file
textcharts heatmap -f matrix.json --color-scheme sequential

# List all 15 chart types
textcharts list

# See data format and options for any chart type
textcharts scatter --help
```

See [docs/input-formats.md](docs/input-formats.md) for the JSON schema of each
chart type.

## MCP Server

Use textcharts as an AI tool via the
[Model Context Protocol](https://modelcontextprotocol.io):

```bash
pip install textcharts[mcp]
```

Add to your MCP client config (Claude Desktop, Claude Code, etc.):

```json
{
  "mcpServers": {
    "textcharts": {
      "command": "textcharts-mcp"
    }
  }
}
```

This exposes 17 tools: `textcharts_bar`, `textcharts_heatmap`, ...,
`textcharts_list`, and `textcharts_describe`. See
[docs/mcp-setup.md](docs/mcp-setup.md) for full configuration options.

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

## Development

Install dev tools:

```bash
uv sync --group dev
```

Run the same checks used for release verification:

```bash
uv run --group dev ruff check src/ tests/
uv run --group dev python -m pytest -q
uv run --group dev sphinx-build -W -b html docs docs/_build/html
uv build
```

Project documentation lives under `docs/` and is built with Sphinx.

If you want richer real-world examples beyond the standalone library docs, use
the [BenchBox documentation](https://benchbox.dev/docs/index.html) as the
canonical reference for benchmark-oriented chart usage.

Golden regression snapshots live under `tests/fixtures/golden/ascii/`. To
intentionally update them after a renderer change:

```bash
uv run --group dev python -m pytest tests/test_golden_output.py -q --update-golden
```

## Features

- **Zero dependencies** — pure Python, stdlib only
- **15 chart types** — from simple bars to heatmaps and CDF curves
- **Terminal-aware** — auto-detects width, color support, and Unicode capability
- **Best/worst highlighting** — automatic annotation of extreme values
- **Typed** — full type hints with `py.typed` marker (PEP 561)

## License

MIT
