from __future__ import annotations

from textcharts import (
    ASCIIChartOptions,
    ASCIINormalizedSpeedup,
    SpeedupData,
    from_normalized_results,
)


def test_normalized_speedup_renders_faster_and_slower_sides():
    data = [
        SpeedupData("SQLite", 1.0, True),
        SpeedupData("DuckDB", 8.2, False),
        SpeedupData("Pandas", 0.4, False),
    ]
    result = ASCIINormalizedSpeedup(data=data, options=ASCIIChartOptions(use_color=False)).render()
    assert "SQLite" in result
    assert "DuckDB" in result
    assert "Pandas" in result
    assert "Slower" in result
    assert "Faster" in result
    assert "8.20x" in result
    assert "0.40x" in result


def test_normalized_speedup_handles_empty_and_invalid_ratios():
    assert "No data" in ASCIINormalizedSpeedup(data=[]).render()
    assert ASCIINormalizedSpeedup._format_ratio(0.0) == "N/A"
    assert ASCIINormalizedSpeedup._format_ratio(float("inf")) == "N/A"
    assert ASCIINormalizedSpeedup._format_ratio(150.0) == "150x"
    assert ASCIINormalizedSpeedup._format_ratio(15.0) == "15.0x"


def test_from_normalized_results_selects_requested_baseline_modes():
    slowest = from_normalized_results(
        [("A", 100), ("B", 500), ("C", 200)],
        baseline="slowest",
        options=ASCIIChartOptions(use_color=False),
    ).render()
    fastest = from_normalized_results(
        [("A", 100), ("B", 500), ("C", 200)],
        baseline="fastest",
        options=ASCIIChartOptions(use_color=False),
    ).render()
    assert "1.00x" in slowest
    assert "1.00x" in fastest


def test_from_normalized_results_handles_empty_and_zero_baseline_inputs():
    empty = from_normalized_results([], options=ASCIIChartOptions(use_color=False)).render()
    zeroish = from_normalized_results(
        [("A", 0.0), ("B", 10.0)],
        baseline="A",
        options=ASCIIChartOptions(use_color=False),
    ).render()
    assert "No data" in empty
    assert "N/A" in zeroish
