from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App, ComposeResult

from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    BoxPlotSeries,
    CDFChart,
    CDFSeriesData,
    ChartOptions,
    ComparisonBar,
    ComparisonBarData,
    DivergingBar,
    DivergingBarData,
    Heatmap,
    Histogram,
    HistogramBar,
    LineChart,
    LinePoint,
    NormalizedSpeedup,
    PercentileData,
    PercentileLadder,
    RankTable,
    RankTableData,
    ScatterPlot,
    ScatterPoint,
    SparklineColumn,
    SparklineTable,
    SparklineTableData,
    SpeedupData,
    StackedBar,
    StackedBarData,
    StackedBarSegment,
    SummaryBox,
    SummaryStats,
)
from textcharts.base import ChartBase
from textcharts.textual import TextChart, text_bar, text_chart


class RecordingChart(ChartBase):
    def __init__(self, label: str, options: ChartOptions | None = None) -> None:
        super().__init__(options)
        self.label = label

    def render(self) -> str:
        return (
            f"{self.label} "
            f"width={self.options.width} "
            f"height={self.options.height} "
            f"theme={self.options.theme} "
            f"color={self.options.use_color} "
            f"unicode={self.options.use_unicode}"
        )


def test_textchart_renders_chart_content():
    class ChartApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(BarChart([BarData("Alpha", 10.0), BarData("Beta", 20.0)], title="Latency"))

    async def run() -> None:
        app = ChartApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            plain = widget.render().plain
            assert "Latency" in plain
            assert "Alpha" in plain
            assert "Beta" in plain

    asyncio.run(run())


def test_textchart_uses_widget_size_and_theme_bridge():
    class RecordingApp(App[None]):
        CSS = "TextChart { width: 70; height: 20; }"

        def compose(self) -> ComposeResult:
            yield TextChart(RecordingChart("probe"))

    async def run() -> None:
        app = RecordingApp()
        async with app.run_test(size=(100, 30)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            plain = widget.render().plain
            assert "probe" in plain
            assert "width=70" in plain
            assert "height=20" in plain
            assert "theme=dark" in plain
            assert "color=True" in plain
            assert "unicode=True" in plain

            app.theme = "textual-light"
            await pilot.pause()
            assert "theme=light" in widget.render().plain

    asyncio.run(run())


def test_textchart_chart_assignment_triggers_rerender():
    class ReassignApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(RecordingChart("first"))

    async def run() -> None:
        app = ReassignApp()
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            assert "first" in widget.render().plain
            widget.chart = RecordingChart("second")
            await pilot.pause()
            assert "second" in widget.render().plain

    asyncio.run(run())


def test_textual_factory_helpers_build_widgets():
    class FactoryApp(App[None]):
        def compose(self) -> ComposeResult:
            yield text_chart("bar", [{"label": "A", "value": 1.0}, {"label": "B", "value": 2.0}], title="Raw")
            yield text_bar([BarData("X", 3.0), BarData("Y", 4.0)], title="Typed", widget_kwargs={"id": "typed"})

    async def run() -> None:
        app = FactoryApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widgets = app.query(TextChart)
            plains = [widget.render().plain for widget in widgets]
            assert any("Raw" in plain and "A" in plain for plain in plains)
            assert any("Typed" in plain and "X" in plain for plain in plains)

    asyncio.run(run())


def test_all_chart_types_render_inside_textual():
    charts = [
        BarChart([BarData("Alpha", 10.0), BarData("Beta", 20.0)], title="Bar"),
        Histogram([HistogramBar("Q1", 10.0), HistogramBar("Q2", 14.0)], title="Histogram"),
        Heatmap([[1.0, 2.0], [3.0, 4.0]], ["Q1", "Q2"], ["A", "B"], title="Heatmap"),
        BoxPlot([BoxPlotSeries("North", [1, 2, 3, 4, 5])], title="Box"),
        LineChart([LinePoint("Series", 1, 10.0), LinePoint("Series", 2, 14.0)], title="Line"),
        ScatterPlot([ScatterPoint("A", 1.0, 2.0), ScatterPoint("B", 2.0, 1.0)], title="Scatter"),
        ComparisonBar([ComparisonBarData("Q1", 10.0, 8.0)], title="Comparison"),
        DivergingBar([DivergingBarData("Q1", -12.0), DivergingBarData("Q2", 7.5)], title="Diverging"),
        SummaryBox(SummaryStats(title="Summary", primary_value=12.0, num_items=2)),
        PercentileLadder([PercentileData("DuckDB", 10.0, 14.0, 15.0, 20.0)], title="Percentile"),
        NormalizedSpeedup([SpeedupData("DuckDB", 1.0, True), SpeedupData("Polars", 0.8, False)], title="Speedup"),
        StackedBar(
            [
                StackedBarData(
                    "DuckDB",
                    [StackedBarSegment("Scan", 10.0), StackedBarSegment("Join", 5.0)],
                )
            ],
            title="Stacked",
        ),
        SparklineTable(
            SparklineTableData(
                rows=["DuckDB", "Polars"],
                columns=[SparklineColumn("Latency", {"DuckDB": 10.0, "Polars": 13.0})],
            ),
            title="Sparkline",
        ),
        CDFChart([CDFSeriesData("DuckDB", [1.0, 2.0, 3.0, 4.0])], title="CDF"),
        RankTable(
            RankTableData(
                items=["Q1", "Q2"],
                groups=["DuckDB", "Polars"],
                values={
                    ("DuckDB", "Q1"): 10.0,
                    ("Polars", "Q1"): 12.0,
                    ("DuckDB", "Q2"): 11.0,
                    ("Polars", "Q2"): 9.0,
                },
            ),
            title="Rank",
        ),
    ]

    class GalleryApp(App[None]):
        CSS = "TextChart { height: 8; }"

        def compose(self) -> ComposeResult:
            for index, chart in enumerate(charts):
                yield TextChart(chart, id=f"chart-{index}")

    async def run() -> None:
        app = GalleryApp()
        async with app.run_test(size=(120, 60)) as pilot:
            await pilot.pause()
            widgets = list(app.query(TextChart))
            assert len(widgets) == 15
            assert all(widget.render().plain.strip() for widget in widgets)

    asyncio.run(run())
