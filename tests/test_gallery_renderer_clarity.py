from __future__ import annotations

import pytest

import textcharts.base as base
from textcharts import (
    ASCIIBarChart,
    ASCIIChartOptions,
    ASCIIHeatmap,
    ASCIILineChart,
    ASCIIScatterPlot,
    ASCIISparklineTable,
    BarData,
    LinePoint,
    ScatterPoint,
    SparklineColumn,
    SparklineTableData,
)
from textcharts.base import ColorMode, TerminalCapabilities


def _capabilities(color_mode: ColorMode) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=96,
        height=30,
        color_mode=color_mode,
        unicode_support=True,
        interactive=color_mode != ColorMode.NONE,
    )


def test_heatmap_uses_configured_x_axis_label():
    chart = ASCIIHeatmap(
        matrix=[[88.0, 91.0]],
        row_labels=["Class A"],
        col_labels=["Math", "Science"],
        x_label="Subjects",
        options=ASCIIChartOptions(width=80, use_color=False),
    )

    result = chart.render()

    assert "Subjects →" in result
    assert "Platform →" not in result


def test_line_chart_renders_both_axis_labels():
    chart = ASCIILineChart(
        points=[LinePoint(series="Organic", x=1, y=320.0), LinePoint(series="Organic", x=2, y=355.0)],
        x_label="Week",
        y_label="Signups",
        options=ASCIIChartOptions(width=80, use_color=False),
    )

    result = chart.render()

    assert "↑ Signups" in result
    assert "Week →" in result


def test_scatter_plot_compacts_axis_labels_onto_one_line():
    chart = ASCIIScatterPlot(
        points=[ScatterPoint(name="Launch", x=8.0, y=410.0), ScatterPoint(name="Newsletter", x=2.0, y=220.0)],
        x_label="Cost (USD)",
        y_label="Performance",
        options=ASCIIChartOptions(width=96, use_color=False),
    )

    result = chart.render()

    assert "↑ Performance / Cost (USD) →" in result
    assert result.count("↑ Performance") == 1
    assert result.count("Cost (USD) →") == 1


def test_bar_chart_renders_legend_for_multi_bar_output():
    chart = ASCIIBarChart(
        data=[BarData(label="Fiction", value=18.4), BarData(label="Children", value=14.2), BarData(label="Comics", value=9.3)],
        options=ASCIIChartOptions(width=96, use_color=False),
    )

    result = chart.render()

    assert "■ Fiction" in result
    assert "◆ Children" in result
    assert "▲ Comics" in result


def test_sparkline_table_colorizes_best_and_worst_legend(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.TRUECOLOR))
    data = SparklineTableData(
        platforms=["North Store", "South Store"],
        columns=[SparklineColumn(name="Revenue", values={"North Store": 82.0, "South Store": 95.0})],
    )
    chart = ASCIISparklineTable(data=data, options=ASCIIChartOptions(width=96, use_color=True))

    result = chart.render()

    assert "\033[" in result
    assert "=best" in result
    assert "=worst" in result
