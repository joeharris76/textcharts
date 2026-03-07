from __future__ import annotations

from textcharts import ASCIIChartOptions, ASCIISparklineTable, SparklineColumn, SparklineTableData
from textcharts.sparkline_table import from_metrics


def _opts(**kw):
    return ASCIIChartOptions(use_color=False, width=100, **kw)


def test_empty_data():
    data = SparklineTableData(platforms=[], columns=[])
    assert "No data" in ASCIISparklineTable(data=data).render()
    data2 = SparklineTableData(platforms=["A"], columns=[])
    assert "No data" in ASCIISparklineTable(data=data2).render()


def test_platforms_and_columns_rendered():
    data = SparklineTableData(
        platforms=["DuckDB", "SQLite"],
        columns=[
            SparklineColumn("Latency", {"DuckDB": 50, "SQLite": 200}, higher_is_better=False),
            SparklineColumn("Success", {"DuckDB": 100, "SQLite": 95}, higher_is_better=True),
        ],
    )
    result = ASCIISparklineTable(data=data, options=_opts()).render()
    assert "DuckDB" in result
    assert "SQLite" in result
    assert "Latency" in result
    assert "Success" in result


def test_best_worst_markers_no_color():
    data = SparklineTableData(
        platforms=["A", "B"],
        columns=[
            SparklineColumn("Speed", {"A": 10, "B": 100}, higher_is_better=False),
        ],
    )
    result = ASCIISparklineTable(data=data, options=_opts()).render()
    # In no-color mode, best gets "+" marker, worst gets "-" marker
    lines = result.splitlines()
    data_lines = [l for l in lines if "A" in l.split()[0:1] or "B" in l.split()[0:1]]
    # A (10) is best for lower-is-better
    a_line = next((l for l in lines if l.strip().startswith("A")), "")
    b_line = next((l for l in lines if l.strip().startswith("B")), "")
    assert "+" in a_line  # best marker
    assert "-" in b_line  # worst marker


def test_higher_is_better_inverts_best_worst():
    data = SparklineTableData(
        platforms=["A", "B"],
        columns=[
            SparklineColumn("Rate", {"A": 10, "B": 100}, higher_is_better=True),
        ],
    )
    result = ASCIISparklineTable(data=data, options=_opts()).render()
    # B (100) is best for higher-is-better
    lines = result.splitlines()
    a_line = next((l for l in lines if l.strip().startswith("A")), "")
    b_line = next((l for l in lines if l.strip().startswith("B")), "")
    assert "-" in a_line  # worst
    assert "+" in b_line  # best


def test_compact_value_formatting():
    assert ASCIISparklineTable._format_compact_value(0) == "0"
    assert ASCIISparklineTable._format_compact_value(0.005) == "0.005"
    assert ASCIISparklineTable._format_compact_value(5.5) == "5.50"
    assert ASCIISparklineTable._format_compact_value(55.5) == "55.5"
    assert ASCIISparklineTable._format_compact_value(555) == "555"
    assert ASCIISparklineTable._format_compact_value(5555) == "5,555"
    assert ASCIISparklineTable._format_compact_value(55555) == "56k"
    assert ASCIISparklineTable._format_compact_value(float("nan")) == "N/A"


def test_legend_line():
    data = SparklineTableData(
        platforms=["A"],
        columns=[SparklineColumn("M", {"A": 10}, higher_is_better=False)],
    )
    result = ASCIISparklineTable(data=data, options=_opts()).render()
    assert "best" in result
    assert "worst" in result


def test_from_metrics_factory():
    chart = from_metrics(
        platforms=["A", "B"],
        metrics=[("Latency", {"A": 50, "B": 200}, False)],
        title="Factory Test",
        options=_opts(),
    )
    result = chart.render()
    assert isinstance(chart, ASCIISparklineTable)
    assert "Factory Test" in result
    assert "A" in result


def test_column_width_fitting():
    # With narrow width, some columns should be dropped
    data = SparklineTableData(
        platforms=["Platform1"],
        columns=[
            SparklineColumn(f"Metric{i}", {"Platform1": float(i)}, higher_is_better=False)
            for i in range(20)
        ],
    )
    result = ASCIISparklineTable(data=data, options=ASCIIChartOptions(use_color=False, width=50)).render()
    # Not all 20 columns can fit in 50 chars; should render without error
    assert "Platform1" in result
