from __future__ import annotations

from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    BoxPlotSeries,
    ChartBase,
    ChartOptions,
    Heatmap,
    Histogram,
    HistogramBar,
    LineChart,
    LinePoint,
    ScatterPlot,
    ScatterPoint,
)


def test_line_chart_single_point_renders():
    chart = LineChart(
        points=[LinePoint(series="Solo", x=1, y=100)],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Solo" in result


def test_heatmap_single_cell_renders():
    chart = Heatmap(
        matrix=[[42]],
        row_labels=["Q1"],
        col_labels=["A"],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Q1" in result
    assert "42" in result


def test_box_plot_single_value_series_renders():
    chart = BoxPlot(
        series=[BoxPlotSeries(name="One", values=[42])],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "One" in result


def test_bar_chart_handles_nan_without_crash():
    chart = BarChart(
        data=[BarData(label="Normal", value=100), BarData(label="NaN", value=float("nan"))],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Normal" in result


def test_bar_chart_handles_infinity_without_crash():
    chart = BarChart(
        data=[BarData(label="Normal", value=100), BarData(label="Inf", value=float("inf"))],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Normal" in result


def test_histogram_handles_zero_latency_without_division_error():
    chart = Histogram(
        data=[HistogramBar(query_id="Q1", latency_ms=0), HistogramBar(query_id="Q2", latency_ms=0)],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Q1" in result


def test_heatmap_narrow_width_truncates_columns():
    matrix = [[i * 10 for i in range(10)]]
    col_labels = [f"Platform{i}" for i in range(10)]
    chart = Heatmap(
        matrix=matrix,
        row_labels=["Q1"],
        col_labels=col_labels,
        options=ChartOptions(width=40, use_color=False),
    )
    result = chart.render()
    assert "Q1" in result
    assert "..." in result


def test_heatmap_column_fitting_compresses_before_truncating():
    matrix = [[float(10 * (i + 1) + j) for j in range(6)] for i in range(3)]
    row_labels = [f"Q{i + 1}" for i in range(3)]
    col_labels = [f"Platform{j + 1}" for j in range(6)]
    chart = Heatmap(
        matrix=matrix,
        row_labels=row_labels,
        col_labels=col_labels,
        options=ChartOptions(width=120, use_color=False),
    )
    result = chart.render()
    for idx in range(1, 7):
        assert f"Platform{idx}" in result
    assert "..." not in result


def test_bar_chart_sanitizes_ansi_sequences_from_labels():
    chart = BarChart(
        data=[BarData(label="\033[31mInjected\033[0m", value=100)],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Injected" in result
    assert "\033[31m" not in result


def test_sanitize_text_strips_ansi_sequences():
    assert ChartBase._sanitize_text("\033[1;31mRED\033[0m") == "RED"


def test_scatter_plot_renders_at_minimum_width():
    chart = ScatterPlot(
        points=[ScatterPoint(name="A", x=10, y=20), ScatterPoint(name="B", x=30, y=40)],
        options=ChartOptions(width=40, use_color=False),
    )
    result = chart.render()
    assert "A" in result
