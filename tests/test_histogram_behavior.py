from __future__ import annotations

from textcharts import ChartOptions, Histogram, HistogramBar, histogram_from_data


def test_histogram_empty_and_basic_rendering():
    assert "No data" in Histogram(data=[]).render()
    result = Histogram(
        data=[HistogramBar(label="Q1", value=100)],
        title="Test Histogram",
        options=ChartOptions(use_color=False),
    ).render()
    assert "Q1" in result
    assert "Test Histogram" in result


def test_histogram_natural_sort_orders_q1_q2_q10():
    data = [
        HistogramBar(label="Q10", value=100),
        HistogramBar(label="Q2", value=200),
        HistogramBar(label="Q1", value=150),
    ]
    result = Histogram(data=data, sort_by="label", options=ChartOptions(use_color=False)).render()
    label_line = next(line for line in result.splitlines() if "Q1" in line and "Q2" in line and "Q10" in line)
    assert label_line.index("Q1") < label_line.index("Q2") < label_line.index("Q10")


def test_histogram_mean_line_can_be_shown_and_hidden():
    data = [HistogramBar(label="Q1", value=100), HistogramBar(label="Q2", value=200)]
    shown = Histogram(data=data, show_mean_line=True, options=ChartOptions(use_color=False)).render()
    hidden = Histogram(data=data, show_mean_line=False, options=ChartOptions(use_color=False)).render()
    assert "Mean" in shown
    assert "Mean" not in hidden


def test_histogram_splits_large_datasets_by_query_ranges():
    data = [HistogramBar(label=f"Q{i}", value=i * 10) for i in range(1, 41)]
    result = Histogram(data=data, max_per_chart=33, options=ChartOptions(use_color=False)).render()
    assert "Q1-Q33" in result
    assert "Q34-Q40" in result


def test_histogram_multiplatform_mode_renders_legend_and_chunks_by_unique_queries():
    data = []
    for i in range(1, 11):
        data.append(HistogramBar(label=f"Q{i}", value=i * 10, platform="DuckDB"))
        data.append(HistogramBar(label=f"Q{i}", value=i * 15, platform="Polars"))

    result = Histogram(data=data, max_per_chart=5, options=ChartOptions(use_color=False)).render()

    assert "DuckDB" in result
    assert "Polars" in result
    assert "Q1-Q5" in result
    assert "Q6-Q10" in result


def test_histogram_multiplatform_legend_replaces_best_worst_legend():
    data = [
        HistogramBar(label="Q1", value=50, platform="DuckDB", is_best=True),
        HistogramBar(label="Q1", value=60, platform="Polars", is_best=True),
        HistogramBar(label="Q2", value=300, platform="DuckDB", is_worst=True),
        HistogramBar(label="Q2", value=350, platform="Polars", is_worst=True),
    ]
    result = Histogram(data=data, options=ChartOptions(use_color=False)).render()
    assert "DuckDB" in result
    assert "Polars" in result
    assert "Best" not in result
    assert "Worst" not in result


def test_histogram_factory_and_compact_labels_behavior():
    data = [HistogramBar(label=f"Q{i}", value=float(i)) for i in range(10, 20)]
    chart = histogram_from_data(data, title="Factory Test", options=ChartOptions(width=46, use_color=False))
    result = chart.render()
    assert "Factory Test" in result
    assert "10" in result
    assert "11" in result
    assert "19" in result
    assert "Q1 Q1 Q1" not in result
