from __future__ import annotations

import io

import pytest

import textcharts.base as base
from textcharts.base import (
    ChartBase,
    ChartOptions,
    ColorMode,
    TerminalCapabilities,
    TerminalColors,
    compute_percentile_linear,
    detect_terminal_capabilities,
    outlier_severity_markers,
    robust_p95,
)


class _DummyChart(ChartBase):
    def render(self) -> str:
        return ""


def test_detect_capabilities_returns_valid_object(monkeypatch: pytest.MonkeyPatch):
    stdout = io.StringIO()
    stdin = io.StringIO()
    monkeypatch.setattr(base.sys, "stdout", stdout)
    monkeypatch.setattr(base.sys, "stdin", stdin)
    monkeypatch.setattr(stdout, "isatty", lambda: False)
    monkeypatch.setattr(stdin, "isatty", lambda: False)

    caps = detect_terminal_capabilities()

    assert caps.width >= 40
    assert caps.height >= 10
    assert isinstance(caps.color_mode, ColorMode)
    assert isinstance(caps.unicode_support, bool)


def test_detect_capabilities_honors_truecolor_and_no_color(monkeypatch: pytest.MonkeyPatch):
    stdout = io.StringIO()
    stdin = io.StringIO()
    monkeypatch.setattr(base.sys, "stdout", stdout)
    monkeypatch.setattr(base.sys, "stdin", stdin)
    monkeypatch.setattr(stdout, "isatty", lambda: True)
    monkeypatch.setattr(stdin, "isatty", lambda: True)
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setenv("NO_COLOR", "1")

    caps = detect_terminal_capabilities()

    assert caps.color_mode == ColorMode.NONE
    assert caps.interactive is True


def test_terminal_colors_modes_and_colorize():
    none = TerminalColors(color_mode=ColorMode.NONE)
    assert none.fg("#ff0000") == ""
    assert none.bg("#ff0000") == ""
    assert none.colorize("x", fg_color="#ff0000") == "x"

    basic = TerminalColors(color_mode=ColorMode.BASIC)
    assert "\033[" in basic.fg(2)
    assert "\033[" in basic.bg(2)

    extended = TerminalColors(color_mode=ColorMode.EXTENDED)
    assert "\033[38;5;" in extended.fg("#1b9e77")
    assert "\033[48;5;" in extended.bg("#1b9e77")
    assert extended.colorize("test", fg_color="#ff0000", bg_color="#000000").endswith(extended.RESET)

    truecolor = TerminalColors(color_mode=ColorMode.TRUECOLOR)
    assert "\033[38;2;255;0;0m" == truecolor.fg("#ff0000")
    assert "\033[48;2;255;0;0m" == truecolor.bg("#ff0000")


def test_chart_options_width_and_character_selection():
    opts = ChartOptions(width=200)
    assert opts.get_effective_width() == 140

    opts = ChartOptions(width=20)
    assert opts.get_effective_width() == 40

    opts = ChartOptions(use_unicode=False, use_color=False)
    assert "#" in opts.get_horizontal_block_chars()
    assert "#" in opts.get_vertical_block_chars()
    assert opts.get_box_chars()["h"] == "-"
    assert opts.get_intensity_chars() == " .-=#"
    assert opts.get_series_fill(1) == "="
    assert opts.get_series_marker(1) == "*"


def test_chart_options_auto_width_uses_cached_capabilities():
    opts = ChartOptions()
    opts._capabilities = TerminalCapabilities(width=100, height=24, color_mode=ColorMode.BASIC)

    assert opts.get_effective_width() == 98
    assert opts.get_colors().color_mode == ColorMode.BASIC


def test_percentile_and_outlier_helpers_cover_edge_cases():
    assert compute_percentile_linear([], 95) == 0.0
    assert compute_percentile_linear([42], 95) == 42
    assert compute_percentile_linear([1, 2, 3, 4], 50) == 2.5
    assert robust_p95([0, 0, 0, 10, 20]) == 10
    assert robust_p95([0, 0, 0]) == 0
    assert outlier_severity_markers(21, 2) == "▸▸▸▸"
    assert outlier_severity_markers(3, 2) == "▸"


def test_base_render_helpers_and_subtitle_formatting():
    chart = _DummyChart(
        options=ChartOptions(use_color=False, use_unicode=True),
        subtitle="TPC-H | SF=1 | v1 | tuned",
    )

    rendered = chart._render_subtitle(80)

    assert rendered is not None
    assert "TPC-H" in rendered
    assert "SF=1" in rendered
    assert "v1" in rendered
    assert "tuned" in rendered
    assert "Injected" == chart._truncate_label("\033[31mInjected\033[0m", 20)
    assert chart._format_value(1500) == "1.5K"
    assert chart._format_value(0.001) == "1.00e-03"
    assert "Latency" in chart._render_axis_label("Latency", 40, axis="y")


def test_base_legend_wraps_and_respects_show_legend():
    chart = _DummyChart(options=ChartOptions(width=40, use_color=False))
    lines = chart._render_legend(
        [("DuckDB", "#1b9e77"), ("SQLite", "#d95f02"), ("Polars", "#7570b3"), ("Pandas", "#666666")],
        chart.options.get_colors(),
    )
    assert len(lines) >= 2

    no_legend = _DummyChart(options=ChartOptions(width=40, use_color=False, show_legend=False))
    assert no_legend._render_legend([("DuckDB", "#1b9e77")], no_legend.options.get_colors()) == []
