#!/usr/bin/env python3
"""Generate terminal screenshot assets for the Sphinx chart gallery."""

from __future__ import annotations

import html
import os
import subprocess
import tempfile
from pathlib import Path

from ansi2html import Ansi2HTMLConverter
from PIL import Image

from textcharts import (
    ASCIIBarChart,
    ASCIIBoxPlot,
    ASCIICDFChart,
    ASCIIChartOptions,
    ASCIIComparisonBar,
    ASCIIDivergingBar,
    ASCIIHeatmap,
    ASCIIHistogram,
    ASCIILineChart,
    ASCIINormalizedSpeedup,
    ASCIIPercentileLadder,
    ASCIIRankTable,
    ASCIIScatterPlot,
    ASCIISparklineTable,
    ASCIIStackedBar,
    ASCIISummaryBox,
    BarData,
    BoxPlotSeries,
    CDFSeriesData,
    ColorMode,
    ComparisonBarData,
    DivergingBarData,
    HistogramBar,
    LinePoint,
    PercentileData,
    RankTableData,
    ScatterPoint,
    SparklineColumn,
    SparklineTableData,
    SpeedupData,
    StackedBarData,
    StackedBarSegment,
    SummaryStats,
    TerminalCapabilities,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "_static" / "screenshots"
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html {{ background: #15181c; }}
  body {{
    margin: 0;
    background: #15181c;
    padding: 28px 30px;
    display: inline-block;
    min-width: 980px;
  }}
  pre {{
    margin: 0;
    font-family: "Fira Code", "JetBrains Mono", "SF Mono", "Menlo", "Consolas", monospace;
    font-size: 13.5px;
    line-height: 1.08;
    color: #d8dee9;
    white-space: pre;
  }}
  .ansi1 {{ font-weight: bold; }}
</style>
</head>
<body>
<pre>{content}</pre>
</body>
</html>
"""


def _chrome_binary() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("Chrome or Chromium not found in expected macOS application paths")


def _caps(color_mode: ColorMode, *, unicode_support: bool, interactive: bool) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=96,
        height=40,
        color_mode=color_mode,
        unicode_support=unicode_support,
        interactive=interactive,
    )


def _options(mode: str) -> ASCIIChartOptions:
    if mode == "color":
        opts = ASCIIChartOptions(width=96, use_color=True, use_unicode=True)
        opts._capabilities = _caps(ColorMode.EXTENDED, unicode_support=True, interactive=True)
        return opts
    if mode == "monochrome":
        opts = ASCIIChartOptions(width=96, use_color=False, use_unicode=False)
        opts._capabilities = _caps(ColorMode.NONE, unicode_support=False, interactive=False)
        return opts
    raise ValueError(f"unsupported mode: {mode}")


def _bar_chart(mode: str) -> str:
    data = [
        BarData(label="DuckDB", value=1234.5, is_best=True),
        BarData(label="SQLite", value=3456.7, is_worst=True),
        BarData(label="Polars", value=2100.0),
    ]
    return ASCIIBarChart(data=data, title="Total Runtime", metric_label="ms", options=_options(mode)).render()


def _histogram(mode: str) -> str:
    bars = [
        HistogramBar(query_id="Q1", latency_ms=120.5, is_best=True),
        HistogramBar(query_id="Q2", latency_ms=340.2),
        HistogramBar(query_id="Q3", latency_ms=89.1),
        HistogramBar(query_id="Q4", latency_ms=567.8, is_worst=True),
        HistogramBar(query_id="Q5", latency_ms=210.0),
        HistogramBar(query_id="Q6", latency_ms=150.3),
    ]
    return ASCIIHistogram(data=bars, title="Query Latency", options=_options(mode)).render()


def _heatmap(mode: str) -> str:
    matrix = [
        [120.0, 150.0, 200.0],
        [340.0, 280.0, 310.0],
        [89.0, 95.0, 110.0],
        [560.0, 480.0, 520.0],
    ]
    chart = ASCIIHeatmap(
        matrix=matrix,
        row_labels=["Q1", "Q2", "Q3", "Q4"],
        col_labels=["DuckDB", "SQLite", "Polars"],
        title="Query Heatmap",
        options=_options(mode),
    )
    return chart.render()


def _box_plot(mode: str) -> str:
    series = [
        BoxPlotSeries(name="DuckDB", values=[80, 95, 110, 130, 150, 200, 250, 300, 500]),
        BoxPlotSeries(name="SQLite", values=[200, 250, 300, 350, 400, 450, 500, 600, 800]),
        BoxPlotSeries(name="Polars", values=[100, 120, 140, 160, 180, 200, 220, 280, 350]),
    ]
    return ASCIIBoxPlot(series=series, title="Query Time Distribution", options=_options(mode)).render()


def _line_chart(mode: str) -> str:
    points = [
        LinePoint(series="DuckDB", x=1, y=120.0, label="Run 1"),
        LinePoint(series="DuckDB", x=2, y=115.0, label="Run 2"),
        LinePoint(series="DuckDB", x=3, y=110.0, label="Run 3"),
        LinePoint(series="SQLite", x=1, y=340.0, label="Run 1"),
        LinePoint(series="SQLite", x=2, y=320.0, label="Run 2"),
        LinePoint(series="SQLite", x=3, y=310.0, label="Run 3"),
    ]
    return ASCIILineChart(points=points, title="Performance Trend", options=_options(mode)).render()


def _scatter_plot(mode: str) -> str:
    points = [
        ScatterPoint(name="DuckDB", x=0.05, y=1234.5),
        ScatterPoint(name="SQLite", x=0.0, y=3456.7),
        ScatterPoint(name="Snowflake", x=2.5, y=890.0),
        ScatterPoint(name="Databricks", x=5.0, y=650.0),
    ]
    return ASCIIScatterPlot(points=points, title="Cost vs Performance", options=_options(mode)).render()


def _comparison_bar(mode: str) -> str:
    data = [
        ComparisonBarData(
            label="Q1", baseline_value=120.0, comparison_value=95.0, baseline_name="v1.0", comparison_name="v1.1"
        ),
        ComparisonBarData(
            label="Q2", baseline_value=340.0, comparison_value=380.0, baseline_name="v1.0", comparison_name="v1.1"
        ),
        ComparisonBarData(
            label="Q3", baseline_value=89.0, comparison_value=72.0, baseline_name="v1.0", comparison_name="v1.1"
        ),
        ComparisonBarData(
            label="Q4", baseline_value=560.0, comparison_value=540.0, baseline_name="v1.0", comparison_name="v1.1"
        ),
    ]
    return ASCIIComparisonBar(data=data, title="Version Comparison", options=_options(mode)).render()


def _diverging_bar(mode: str) -> str:
    data = [
        DivergingBarData(label="Q1", pct_change=-20.8),
        DivergingBarData(label="Q2", pct_change=11.8),
        DivergingBarData(label="Q3", pct_change=-19.1),
        DivergingBarData(label="Q4", pct_change=-3.6),
        DivergingBarData(label="Q5", pct_change=45.2),
    ]
    return ASCIIDivergingBar(data=data, title="Regression Analysis", options=_options(mode)).render()


def _summary_box(mode: str) -> str:
    stats = SummaryStats(
        title="TPC-H on DuckDB (SF 1)",
        geo_mean_ms=156.3,
        median_ms=142.0,
        total_time_ms=3450.0,
        num_queries=22,
        best_queries=[("Q6", 12.5), ("Q1", 45.2), ("Q3", 67.8)],
        worst_queries=[("Q21", 890.0), ("Q18", 670.0), ("Q9", 450.0)],
        environment={"OS": "macOS 15.3", "CPUs": "12 (arm64)", "Memory": "36 GB"},
        platform_config={"Driver": "DuckDB 1.2.0", "Tuning": "Tuned"},
    )
    return ASCIISummaryBox(stats=stats, options=_options(mode)).render()


def _percentile_ladder(mode: str) -> str:
    data = [
        PercentileData(name="DuckDB", p50=120.0, p90=350.0, p95=480.0, p99=890.0),
        PercentileData(name="SQLite", p50=280.0, p90=520.0, p95=650.0, p99=1200.0),
        PercentileData(name="Polars", p50=150.0, p90=310.0, p95=420.0, p99=700.0),
    ]
    return ASCIIPercentileLadder(data=data, title="Tail Latency", options=_options(mode)).render()


def _normalized_speedup(mode: str) -> str:
    data = [
        SpeedupData(name="DuckDB", ratio=1.0, is_baseline=True),
        SpeedupData(name="SQLite", ratio=0.36),
        SpeedupData(name="Polars", ratio=0.85),
        SpeedupData(name="Snowflake", ratio=1.42),
    ]
    return ASCIINormalizedSpeedup(data=data, title="Relative Speedup", options=_options(mode)).render()


def _stacked_bar(mode: str) -> str:
    data = [
        StackedBarData(
            label="DuckDB",
            segments=[
                StackedBarSegment(phase_name="Generate", value=5.0),
                StackedBarSegment(phase_name="Load", value=12.0),
                StackedBarSegment(phase_name="Query", value=1234.5),
            ],
        ),
        StackedBarData(
            label="SQLite",
            segments=[
                StackedBarSegment(phase_name="Generate", value=5.0),
                StackedBarSegment(phase_name="Load", value=45.0),
                StackedBarSegment(phase_name="Query", value=3456.7),
            ],
        ),
    ]
    return ASCIIStackedBar(data=data, title="Phase Breakdown", options=_options(mode)).render()


def _sparkline_table(mode: str) -> str:
    data = SparklineTableData(
        platforms=["DuckDB", "SQLite", "Polars"],
        columns=[
            SparklineColumn(name="Total (ms)", values={"DuckDB": 1234.5, "SQLite": 3456.7, "Polars": 2100.0}),
            SparklineColumn(name="Geo Mean", values={"DuckDB": 156.3, "SQLite": 420.1, "Polars": 210.5}),
            SparklineColumn(name="P99 (ms)", values={"DuckDB": 890.0, "SQLite": 1200.0, "Polars": 700.0}),
        ],
    )
    return ASCIISparklineTable(data=data, title="Platform Overview", options=_options(mode)).render()


def _cdf_chart(mode: str) -> str:
    data = [
        CDFSeriesData(name="DuckDB", values=[80, 95, 110, 130, 150, 200, 250, 300, 500]),
        CDFSeriesData(name="SQLite", values=[200, 250, 300, 350, 400, 450, 500, 600, 800]),
    ]
    return ASCIICDFChart(data=data, title="Cumulative Distribution", options=_options(mode)).render()


def _rank_table(mode: str) -> str:
    data = RankTableData(
        queries=["Q1", "Q2", "Q3", "Q4"],
        platforms=["DuckDB", "SQLite", "Polars"],
        times={
            ("DuckDB", "Q1"): 120.0,
            ("SQLite", "Q1"): 150.0,
            ("Polars", "Q1"): 135.0,
            ("DuckDB", "Q2"): 340.0,
            ("SQLite", "Q2"): 280.0,
            ("Polars", "Q2"): 310.0,
            ("DuckDB", "Q3"): 89.0,
            ("SQLite", "Q3"): 110.0,
            ("Polars", "Q3"): 95.0,
            ("DuckDB", "Q4"): 560.0,
            ("SQLite", "Q4"): 480.0,
            ("Polars", "Q4"): 520.0,
        },
    )
    return ASCIIRankTable(data=data, title="Platform Rankings", options=_options(mode)).render()


CHARTS = {
    "bar_chart": _bar_chart,
    "histogram": _histogram,
    "heatmap": _heatmap,
    "box_plot": _box_plot,
    "line_chart": _line_chart,
    "scatter_plot": _scatter_plot,
    "comparison_bar": _comparison_bar,
    "diverging_bar": _diverging_bar,
    "summary_box": _summary_box,
    "percentile_ladder": _percentile_ladder,
    "normalized_speedup": _normalized_speedup,
    "stacked_bar": _stacked_bar,
    "sparkline_table": _sparkline_table,
    "cdf_chart": _cdf_chart,
    "rank_table": _rank_table,
}


def _ansi_to_html(text: str) -> str:
    converter = Ansi2HTMLConverter(inline=True, scheme="ansi2html", dark_bg=True)
    return converter.convert(text, full=False)


def _estimate_height(text: str, pad: int = 72) -> int:
    lines = text.count("\n") + 1
    return min(max(lines * 24 + pad * 2, 200), 2600)


def _save_png(html_content: str, out_path: Path, text: str, *, width: int = 1100) -> None:
    chrome = _chrome_binary()
    height = _estimate_height(text)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as handle:
        handle.write(html_content)
        tmp_html = handle.name
    try:
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                f"--window-size={width},{height}",
                "--screenshot=" + str(out_path),
                "file://" + tmp_html,
            ],
            check=True,
            capture_output=True,
            env={**os.environ, "TERM": "xterm-256color", "FORCE_COLOR": "1"},
        )
    finally:
        Path(tmp_html).unlink(missing_ok=True)


def _crop_png(path: Path) -> None:
    image = Image.open(path).convert("RGB")
    pixels = image.load()
    width, height = image.size
    bg = (21, 24, 28)

    def is_bg(x: int, y: int) -> bool:
        pixel = pixels[x, y]
        return all(abs(pixel[idx] - bg[idx]) <= 4 for idx in range(3))

    last_row = height - 1
    for y in range(height - 1, 0, -1):
        if not all(is_bg(x, y) for x in range(0, width, 4)):
            last_row = min(y + 36, height)
            break
    image.crop((0, 0, width, last_row)).save(path)


def _render_mode(chart_name: str, mode: str) -> Path:
    text = CHARTS[chart_name](mode)
    out_dir = OUT / chart_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{mode}.png"
    if mode == "color":
        html_body = _ansi_to_html(text)
    else:
        html_body = html.escape(text)
    _save_png(HTML_TEMPLATE.format(content=html_body), out_path, text)
    _crop_png(out_path)
    return out_path


def _make_greyscale(chart_name: str) -> Path:
    color_path = OUT / chart_name / "color.png"
    greyscale_path = OUT / chart_name / "greyscale.png"
    image = Image.open(color_path).convert("L").convert("RGB")
    image.save(greyscale_path)
    return greyscale_path


def main() -> None:
    for chart_name in CHARTS:
        print(f"Generating {chart_name}")
        _render_mode(chart_name, "color")
        _make_greyscale(chart_name)
        _render_mode(chart_name, "monochrome")
    print(f"Generated screenshots in {OUT}")


if __name__ == "__main__":
    main()
