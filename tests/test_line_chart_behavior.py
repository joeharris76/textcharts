from __future__ import annotations

from textcharts import ChartOptions, LineChart, LinePoint


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


def test_empty_data():
    assert "No data" in LineChart(points=[]).render()


def test_trend_line_renders_dots():
    # Simple ascending series — trend line should produce "." characters
    points = [LinePoint("S", i, float(i * 10)) for i in range(1, 8)]
    result = LineChart(
        points=points, show_trend=True, options=_opts()
    ).render()
    assert "." in result  # trend dots appear in grid


def test_trend_not_shown_when_disabled():
    points = [LinePoint("S", i, float(i * 10)) for i in range(1, 8)]
    no_trend = LineChart(points=points, show_trend=False, options=_opts()).render()
    with_trend = LineChart(points=points, show_trend=True, options=_opts()).render()
    # Trend version should have more dots
    assert with_trend.count(".") >= no_trend.count(".")


def test_compute_trend_linear():
    chart = LineChart(points=[LinePoint("S", 1, 1.0)], options=_opts())
    # Perfect linear: 0, 10, 20 → trend should be exactly [0, 10, 20]
    trend = chart._compute_trend([0.0, 10.0, 20.0])
    assert len(trend) == 3
    assert abs(trend[0] - 0.0) < 0.01
    assert abs(trend[1] - 10.0) < 0.01
    assert abs(trend[2] - 20.0) < 0.01


def test_compute_trend_single_value():
    chart = LineChart(points=[LinePoint("S", 1, 1.0)], options=_opts())
    assert chart._compute_trend([42.0]) == [42.0]


def test_compute_trend_constant():
    chart = LineChart(points=[LinePoint("S", 1, 1.0)], options=_opts())
    # All same values: denom == 0, returns original
    trend = chart._compute_trend([5.0, 5.0, 5.0])
    assert trend == [5.0, 5.0, 5.0]


def test_multi_series_renders_legend():
    points = [
        LinePoint("Alpha", 1, 10.0),
        LinePoint("Alpha", 2, 20.0),
        LinePoint("Beta", 1, 15.0),
        LinePoint("Beta", 2, 25.0),
    ]
    result = LineChart(points=points, options=_opts()).render()
    assert "Legend" in result
    assert "Alpha" in result
    assert "Beta" in result


def test_categorical_x_axis():
    points = [
        LinePoint("S", "Mon", 10.0),
        LinePoint("S", "Tue", 20.0),
        LinePoint("S", "Wed", 15.0),
    ]
    result = LineChart(points=points, options=_opts()).render()
    assert "Mon" in result
    assert "Tue" in result
    assert "Wed" in result


def test_axis_labels_rendered():
    points = [LinePoint("S", 1, 10.0), LinePoint("S", 2, 20.0)]
    result = LineChart(
        points=points, x_label="Time", y_label="Value", options=_opts()
    ).render()
    assert "Time" in result
    assert "Value" in result


def test_y_axis_capping_with_outlier():
    # One extreme outlier should trigger y-axis capping
    points = [LinePoint("S", i, 10.0) for i in range(1, 10)]
    points.append(LinePoint("S", 10, 10000.0))  # extreme outlier
    result = LineChart(points=points, options=_opts()).render()
    # Truncation marker should appear
    assert "capped" in result.lower() or "\u25b8" in result
