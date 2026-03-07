from __future__ import annotations

from textcharts import ASCIIChartOptions, ASCIIStackedBar, StackedBarData, StackedBarSegment
from textcharts.stacked_bar import from_phase_data


def _opts(**kw):
    return ASCIIChartOptions(use_color=False, width=80, **kw)


def test_empty_data():
    assert "No data" in ASCIIStackedBar(data=[]).render()


def test_segments_and_total_rendered():
    data = [
        StackedBarData("Platform1", [
            StackedBarSegment("Load", 100.0),
            StackedBarSegment("Run", 500.0),
            StackedBarSegment("Cleanup", 50.0),
        ]),
    ]
    result = ASCIIStackedBar(data=data, options=_opts()).render()
    assert "Platform1" in result
    assert "Load" in result
    assert "Run" in result
    assert "Cleanup" in result


def test_auto_total_computation():
    segs = [StackedBarSegment("A", 100.0), StackedBarSegment("B", 200.0)]
    d = StackedBarData("P1", segs)
    assert d.total == 300.0


def test_format_time_units():
    assert ASCIIStackedBar._format_time(500.0) == "500ms"
    assert ASCIIStackedBar._format_time(1500.0) == "1.5s"
    assert ASCIIStackedBar._format_time(90_000.0) == "1.5min"


def test_multi_platform_rendering():
    data = [
        StackedBarData("Fast", [StackedBarSegment("Load", 100), StackedBarSegment("Run", 200)]),
        StackedBarData("Slow", [StackedBarSegment("Load", 300), StackedBarSegment("Run", 1200)]),
    ]
    result = ASCIIStackedBar(data=data, options=_opts()).render()
    assert "Fast" in result
    assert "Slow" in result


def test_legend_shows_phase_names():
    data = [
        StackedBarData("P1", [
            StackedBarSegment("DataGen", 10),
            StackedBarSegment("Query", 90),
        ]),
    ]
    result = ASCIIStackedBar(data=data, options=_opts()).render()
    # Legend line should list phase names
    assert "DataGen" in result
    assert "Query" in result


def test_zero_segment_skipped():
    data = [
        StackedBarData("P1", [
            StackedBarSegment("A", 0.0),
            StackedBarSegment("B", 100.0),
        ]),
    ]
    result = ASCIIStackedBar(data=data, options=_opts()).render()
    assert "P1" in result  # renders without error


def test_from_phase_data_factory():
    data = [StackedBarData("P1", [StackedBarSegment("Load", 100)])]
    chart = from_phase_data(data, title="Factory Test", options=_opts())
    result = chart.render()
    assert isinstance(chart, ASCIIStackedBar)
    assert "Factory Test" in result
