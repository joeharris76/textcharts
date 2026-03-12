# Textual integration

`textcharts` can render directly inside a [Textual](https://textual.textualize.io/) app without changing the core chart engine.

## Install

```bash
pip install "textcharts[textual]"
```

The base package stays zero-dependency. Importing `textcharts` does not pull in `textual`; the optional integration lives under `textcharts.textual`.

## Generic wrapper

Use `TextChart` when you already have a chart instance:

```python
from textual.app import App, ComposeResult

from textcharts import BarChart, BarData
from textcharts.textual import TextChart


class ChartApp(App[None]):
    def compose(self) -> ComposeResult:
        chart = BarChart([BarData("DuckDB", 128.0), BarData("Polars", 164.0)], title="Runtime")
        yield TextChart(chart)
```

The widget adapts the wrapped chart to the current Textual layout:

- Widget width and height are forwarded through `ChartOptions`
- Color and Unicode are forced on so Rich/Textual can render the ANSI output
- The chart theme follows the current Textual theme (`dark` / `light`)

## Factory helpers

If your data is still in command-layer form, use `text_chart()`:

```python
from textcharts.textual import text_chart

widget = text_chart(
    "bar",
    [{"label": "DuckDB", "value": 128.0}, {"label": "Polars", "value": 164.0}],
    title="Runtime",
)
```

There are also typed helpers such as `text_bar()`, `text_line()`, and `text_heatmap()` that return a `TextChart` directly.

## Typed widgets

Typed widgets wrap the adapter with reactive chart-specific attributes:

```python
from textcharts import BarData, LinePoint
from textcharts.textual import BarChartWidget, LineChartWidget

throughput = BarChartWidget(
    data=[BarData("DuckDB", 320.0), BarData("Polars", 280.0)],
    metric_label="ops/s",
    title="Throughput",
)

trend = LineChartWidget(
    data=[LinePoint("Latency", 1, 11.0), LinePoint("Latency", 2, 10.4)],
    x_label="Run",
    y_label="ms",
    show_trend=True,
    title="Latency Trend",
)

throughput.data = [BarData("DuckDB", 340.0), BarData("Polars", 287.0)]
trend.show_trend = False
```

Available typed widgets:

- `BarChartWidget`
- `HistogramWidget`
- `HeatmapWidget`
- `BoxPlotWidget`
- `LineChartWidget`
- `ScatterPlotWidget`
- `ComparisonBarWidget`
- `DivergingBarWidget`
- `SummaryBoxWidget`
- `PercentileWidget`
- `SpeedupWidget`
- `StackedBarWidget`
- `SparklineWidget`
- `CDFChartWidget`
- `RankTableWidget`

## Data binding

Typed widgets work with Textual `data_bind()`:

```python
from textual.app import App, ComposeResult
from textual.reactive import reactive

from textcharts import BarData
from textcharts.textual import BarChartWidget


class Dashboard(App[None]):
    chart_data = reactive([BarData("DuckDB", 320.0), BarData("Polars", 280.0)], init=False)

    def compose(self) -> ComposeResult:
        yield BarChartWidget(metric_label="ops/s").data_bind(data=Dashboard.chart_data)
```

Updating `self.chart_data` in the parent app automatically rebuilds the child chart widget.

## Compound widgets

`ChartSwitcher` composes a `Select` control with a `TextChart` display. Provide builders that accept a shared data object and return chart instances:

```python
from textcharts import BarChart, BarData, LineChart, LinePoint
from textcharts.textual import ChartSwitcher


def build_bar(data):
    return BarChart([BarData(label, value) for label, value in data], title="Bar View")


def build_line(data):
    return LineChart(
        [LinePoint("Series", index, value, label=label) for index, (label, value) in enumerate(data, start=1)],
        title="Line View",
    )


switcher = ChartSwitcher({"bar": build_bar, "line": build_line}, [("A", 1.0), ("B", 2.0)])
```

When the selection changes, the widget posts `ChartSwitcher.Changed`.

## Examples

- `examples/textual_gallery.py` shows all 15 chart types with a selector.
- `examples/textual_dashboard.py` shows reactive widgets bound to app-level state and updated on a timer.
