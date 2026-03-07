"""Direct tests for all public factory functions.

Tests happy path (return type, data passthrough, options forwarding)
and edge cases (empty data, single item).
"""

from __future__ import annotations

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
    BarData,
    BoxPlotSeries,
    CDFSeriesData,
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
    cdf_from_query_results,
    from_bar_data,
    from_comparison_data,
    from_cost_performance_points,
    from_distribution_series,
    from_heatmap_data,
    from_matrix,
    from_metrics,
    from_normalized_results,
    from_phase_data,
    from_query_latency_data,
    from_regression_data,
    from_time_series_points,
    percentile_from_query_results,
)


def _opts(**kw):
    return ASCIIChartOptions(use_color=False, width=80, **kw)


# ---------------------------------------------------------------------------
# w1: Happy-path tests for all 14 factory functions
# ---------------------------------------------------------------------------


def test_from_bar_data():
    data = [BarData("A", 10.0), BarData("B", 20.0)]
    chart = from_bar_data(data, title="Bar Test", options=_opts())
    assert isinstance(chart, ASCIIBarChart)
    result = chart.render()
    assert "Bar Test" in result
    assert "A" in result


def test_from_query_latency_data():
    data = [HistogramBar(query_id="Q1", latency_ms=100)]
    chart = from_query_latency_data(data, title="Hist Test", options=_opts())
    assert isinstance(chart, ASCIIHistogram)
    assert "Q1" in chart.render()


def test_from_matrix():
    chart = from_matrix(
        matrix=[[10, 20], [30, 40]],
        queries=["Q1", "Q2"],
        platforms=["A", "B"],
        title="Heat Test",
        options=_opts(),
    )
    assert isinstance(chart, ASCIIHeatmap)
    result = chart.render()
    assert "Heat Test" in result
    assert "Q1" in result


def test_from_distribution_series():
    series = [BoxPlotSeries("S1", [10, 20, 30, 40, 50])]
    chart = from_distribution_series(series, title="Box Test", options=_opts())
    assert isinstance(chart, ASCIIBoxPlot)
    assert "Box Test" in chart.render()


def test_from_time_series_points():
    points = [LinePoint("S", 1, 10.0), LinePoint("S", 2, 20.0), LinePoint("S", 3, 15.0)]
    chart = from_time_series_points(points, title="Line Test", options=_opts())
    assert isinstance(chart, ASCIILineChart)
    assert "Line Test" in chart.render()


def test_from_cost_performance_points():
    points = [ScatterPoint("A", 10, 100), ScatterPoint("B", 20, 200)]
    chart = from_cost_performance_points(points, title="Scatter Test", options=_opts())
    assert isinstance(chart, ASCIIScatterPlot)
    assert "Scatter Test" in chart.render()


def test_from_comparison_data():
    data = [ComparisonBarData("Q1", 100, 80)]
    chart = from_comparison_data(data, title="Comp Test", options=_opts())
    assert isinstance(chart, ASCIIComparisonBar)
    assert "Comp Test" in chart.render()


def test_from_regression_data():
    data = [DivergingBarData("Q1", -10.0)]
    chart = from_regression_data(data, title="Div Test", options=_opts())
    assert isinstance(chart, ASCIIDivergingBar)
    assert "Div Test" in chart.render()


def test_from_normalized_results():
    chart = from_normalized_results(
        [("A", 100), ("B", 200)], title="Speed Test", options=_opts()
    )
    assert isinstance(chart, ASCIINormalizedSpeedup)
    assert "Speed Test" in chart.render()


def test_from_phase_data():
    data = [StackedBarData("P1", [StackedBarSegment("Load", 100)])]
    chart = from_phase_data(data, title="Stack Test", options=_opts())
    assert isinstance(chart, ASCIIStackedBar)
    assert "Stack Test" in chart.render()


def test_from_metrics():
    chart = from_metrics(
        platforms=["A", "B"],
        metrics=[("Latency", {"A": 50, "B": 100}, False)],
        title="Spark Test",
        options=_opts(),
    )
    assert isinstance(chart, ASCIISparklineTable)
    assert "Spark Test" in chart.render()


def test_cdf_from_query_results():
    chart = cdf_from_query_results(
        [("A", [10, 20, 30, 40, 50])], title="CDF Test", options=_opts()
    )
    assert isinstance(chart, ASCIICDFChart)
    assert "CDF Test" in chart.render()


def test_percentile_from_query_results():
    chart = percentile_from_query_results(
        [("A", [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])],
        title="Pct Test",
        options=_opts(),
    )
    assert isinstance(chart, ASCIIPercentileLadder)
    assert "Pct Test" in chart.render()


def test_from_heatmap_data():
    chart = from_heatmap_data(
        matrix=[[10, 20], [30, 40]],
        queries=["Q1", "Q2"],
        platforms=["A", "B"],
        title="Rank Test",
        options=_opts(),
    )
    assert isinstance(chart, ASCIIRankTable)
    assert "Rank Test" in chart.render()


# ---------------------------------------------------------------------------
# w2: Edge-case factory tests
# ---------------------------------------------------------------------------


def test_from_bar_data_empty():
    chart = from_bar_data([], options=_opts())
    assert "No data" in chart.render()


def test_from_distribution_series_single_value():
    series = [BoxPlotSeries("S1", [42.0])]
    chart = from_distribution_series(series, options=_opts())
    result = chart.render()
    assert "S1" in result


def test_from_matrix_1x1():
    chart = from_matrix([[99.0]], ["Q1"], ["A"], options=_opts())
    result = chart.render()
    assert "Q1" in result
    assert "99" in result


def test_cdf_from_query_results_empty_values():
    chart = cdf_from_query_results([("Empty", [])], options=_opts())
    result = chart.render()
    # CDF with no values renders "No data"
    assert "No data" in result


def test_from_time_series_points_single_point():
    points = [LinePoint("S", 1, 42.0)]
    chart = from_time_series_points(points, options=_opts())
    result = chart.render()
    assert "42" in result


def test_from_cost_performance_points_single():
    points = [ScatterPoint("Solo", 10, 100)]
    chart = from_cost_performance_points(points, options=_opts())
    result = chart.render()
    assert "Solo" in result
