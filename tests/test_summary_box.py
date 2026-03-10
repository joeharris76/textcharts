from __future__ import annotations

from textcharts import ChartOptions, SummaryBox, SummaryStats


def test_summary_box_single_run_shows_basic_metrics():
    stats = SummaryStats(title="DuckDB Summary", geo_mean_ms=142.3, total_time_ms=3200, num_queries=22)
    chart = SummaryBox(stats=stats, options=ChartOptions(use_color=False))
    result = chart.render()
    assert "DuckDB Summary" in result
    assert "142.3" in result
    assert "3.2s" in result
    assert "22" in result


def test_summary_box_single_run_best_worst_include_units():
    stats = SummaryStats(
        title="Unit Test",
        geo_mean_ms=100.0,
        total_time_ms=500.0,
        num_queries=3,
        best_queries=[("Q6", 8.0), ("Q14", 12.5)],
        worst_queries=[("Q18", 302.0), ("Q21", 1500.0)],
    )
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    assert "Q6 (8.0ms)" in result
    assert "Q21 (1.5s)" in result


def test_summary_box_comparison_summary_shows_deltas_and_counts():
    stats = SummaryStats(
        title="SQL vs DF Summary",
        geo_mean_baseline_ms=142.3,
        geo_mean_comparison_ms=98.7,
        total_time_baseline_ms=3200,
        total_time_comparison_ms=2100,
        num_queries=22,
        num_improved=5,
        num_stable=12,
        num_regressed=5,
        best_queries=[("Q6", -57.2), ("Q14", -38.1)],
        worst_queries=[("Q21", 726.0), ("Q17", 23.4)],
    )
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    assert "142.3" in result
    assert "98.7" in result
    assert "5 improved" in result
    assert "12 stable" in result
    assert "5 regressed" in result


def test_summary_box_ascii_only_mode_uses_ascii_borders():
    stats = SummaryStats(title="Test", geo_mean_ms=100)
    result = SummaryBox(stats=stats, options=ChartOptions(use_unicode=False, use_color=False)).render()
    assert "+" in result
    assert "|" in result
    assert "-" in result


def test_summary_box_renders_without_ansi_when_color_disabled():
    stats = SummaryStats(
        title="Test",
        geo_mean_baseline_ms=100,
        geo_mean_comparison_ms=80,
        num_improved=3,
        num_stable=1,
        num_regressed=1,
    )
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    assert "\033[" not in result


def test_summary_box_formats_minutes_seconds_and_milliseconds():
    assert "2.0min" in SummaryBox(
        stats=SummaryStats(title="Test", total_time_ms=120_000),
        options=ChartOptions(use_color=False),
    ).render()
    assert "5.5s" in SummaryBox(
        stats=SummaryStats(title="Test", total_time_ms=5500),
        options=ChartOptions(use_color=False),
    ).render()
    assert "42.5ms" in SummaryBox(
        stats=SummaryStats(title="Test", total_time_ms=42.5),
        options=ChartOptions(use_color=False),
    ).render()


def test_summary_box_two_column_mode_keeps_percentage_deltas_visible():
    stats = SummaryStats(
        title="Summary",
        geo_mean_baseline_ms=100,
        geo_mean_comparison_ms=130,
        total_time_baseline_ms=4000,
        total_time_comparison_ms=3000,
        num_queries=22,
        environment={"OS": "macOS", "Python": "3.12.2", "CPUs": "10", "Memory": "16GB"},
    )
    result = SummaryBox(stats=stats, options=ChartOptions(width=120, use_color=False)).render()
    assert "+30.0%" in result
    assert "-25.0%" in result
    assert "OS: macOS" in result


def test_summary_box_three_column_mode_shows_environment_and_config():
    stats = SummaryStats(
        title="Summary",
        geo_mean_ms=156.3,
        median_ms=142.0,
        total_time_ms=3450.0,
        num_queries=22,
        environment={"OS": "macOS 15.3", "CPUs": "12 (arm64)", "Memory": "36 GB"},
        platform_config={"Driver": "DuckDB 1.2.0", "Tuning": "Tuned"},
    )
    result = SummaryBox(stats=stats, options=ChartOptions(width=120, use_color=False)).render()
    assert "Driver: DuckDB 1.2.0" in result
    assert "Tuning: Tuned" in result
    assert "OS: macOS 15.3" in result


def test_summary_box_long_lines_do_not_exceed_configured_width():
    stats = SummaryStats(
        title="X" * 200,
        geo_mean_baseline_ms=100,
        geo_mean_comparison_ms=130,
        total_time_baseline_ms=4000,
        total_time_comparison_ms=3000,
        num_queries=3,
        num_improved=1,
        num_stable=1,
        num_regressed=1,
        best_queries=[
            ("aggregation_groupby_large", -12.2),
            ("exchange_merge_join_extremely_verbose_name", -10.0),
            ("read_parquet_single", -9.2),
        ],
        worst_queries=[("another_extremely_verbose_query_identifier_name", 55.0)],
    )
    result = SummaryBox(stats=stats, options=ChartOptions(width=80, use_color=False)).render()
    assert all(len(line) == 80 for line in result.splitlines())


def test_summary_box_value_formatter_callback():
    stats = SummaryStats(
        title="Test",
        total_time_ms=1500.0,
        best_queries=[("Q1", 800.0)],
        value_formatter=lambda v: f"{v / 1000:.1f} KB",
    )
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    assert "1.5 KB" in result  # total_time formatted by callback
    assert "0.8 KB" in result  # best_query formatted by callback
    # No time suffixes should appear
    for suffix in ("ms", "min"):
        assert suffix not in result


def test_summary_box_value_formatter_overrides_metric_label():
    stats = SummaryStats(
        title="Test",
        geo_mean_ms=500.0,
        total_time_ms=3000.0,
        metric_label="ms",
        value_formatter=lambda v: f"{int(v)} reqs",
    )
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    assert "3000 reqs" in result


def test_summary_box_non_ms_metric_label_uses_generic_formatting():
    stats = SummaryStats(
        title="Test",
        total_time_ms=1200.0,
        best_queries=[("Q1", 800.0)],
        metric_label=" reqs",
    )
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    # total_time should NOT use _format_time (would show "1.2s")
    assert "1.2s" not in result
    # Should use _format_value + metric_label instead
    assert "1.2K reqs" in result


def test_summary_box_default_ms_formatting_unchanged():
    stats = SummaryStats(title="Test", total_time_ms=5500.0)
    result = SummaryBox(stats=stats, options=ChartOptions(use_color=False)).render()
    assert "5.5s" in result


def test_summary_box_subtitle_renders_inside_box():
    stats = SummaryStats(title="DuckDB Summary", geo_mean_ms=142.3, total_time_ms=3200, num_queries=22)
    chart = SummaryBox(stats=stats, subtitle="TPC-H SF=1", options=ChartOptions(use_color=False))
    result = chart.render()
    assert "TPC-H SF=1" in result
    # Subtitle should appear between title and metrics separator
    lines = result.splitlines()
    title_idx = next(i for i, line in enumerate(lines) if "DuckDB Summary" in line)
    subtitle_idx = next(i for i, line in enumerate(lines) if "TPC-H SF=1" in line)
    assert subtitle_idx == title_idx + 1


def test_summary_box_no_subtitle_by_default():
    stats = SummaryStats(title="Test", geo_mean_ms=100)
    chart = SummaryBox(stats=stats, options=ChartOptions(use_color=False))
    result = chart.render()
    lines = result.splitlines()
    title_idx = next(i for i, line in enumerate(lines) if "Test" in line)
    # Next line after title should be the metrics separator, not a subtitle
    assert lines[title_idx + 1].strip().startswith("+") or lines[title_idx + 1].strip().startswith("├")


def test_summary_box_subtitle_stays_within_box_width():
    stats = SummaryStats(title="Test", geo_mean_ms=100)
    chart = SummaryBox(stats=stats, subtitle="S" * 200, options=ChartOptions(width=80, use_color=False))
    result = chart.render()
    assert all(len(line) == 80 for line in result.splitlines())
