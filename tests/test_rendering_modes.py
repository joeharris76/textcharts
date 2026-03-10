"""Tests for color output and Unicode/ASCII fallback rendering paths."""

from __future__ import annotations

import re

import pytest

import textcharts.base as base
from textcharts import (
    ChartOptions,
    BarChart,
    BarData,
    Heatmap,
    Histogram,
    HistogramBar,
    ScatterPlot,
    ScatterPoint,
)
from textcharts.base import ColorMode, TerminalCapabilities

ANSI_RE = re.compile(r"\x1b\[[\d;]*m")
# Unicode block elements range U+2580-U+259F
UNICODE_BLOCKS_RE = re.compile(r"[\u2580-\u259f]")


def _caps(color_mode: ColorMode) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=80, height=24, color_mode=color_mode,
        unicode_support=True, interactive=color_mode != ColorMode.NONE,
    )


def _make_bar_data():
    return [BarData("A", 10.0), BarData("B", 20.0), BarData("C", 15.0)]


def _make_heatmap_args():
    return dict(matrix=[[10, 20], [30, 40]], row_labels=["Q1", "Q2"], col_labels=["X", "Y"])


def _make_histogram_data():
    return [HistogramBar(query_id=f"Q{i}", latency_ms=float(i * 10)) for i in range(1, 6)]


def _make_scatter_data():
    return [ScatterPoint("A", 10, 100), ScatterPoint("B", 20, 200), ScatterPoint("C", 15, 150)]


# ---------------------------------------------------------------------------
# w1: Color output tests
# ---------------------------------------------------------------------------


def test_bar_chart_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = BarChart(data=_make_bar_data(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_heatmap_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = Heatmap(**_make_heatmap_args(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_histogram_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = Histogram(data=_make_histogram_data(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_scatter_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = ScatterPlot(points=_make_scatter_data(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_no_color_mode_produces_no_ansi():
    result = BarChart(data=_make_bar_data(), options=ChartOptions(use_color=False, width=80)).render()
    assert not ANSI_RE.search(result), "Expected no ANSI escape sequences in no-color output"


# ---------------------------------------------------------------------------
# w2: ASCII fallback tests
# ---------------------------------------------------------------------------


def test_bar_chart_ascii_fallback():
    result = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(use_color=False, use_unicode=False, width=80),
    ).render()
    assert not UNICODE_BLOCKS_RE.search(result), "Expected no Unicode block chars in ASCII mode"


def test_heatmap_ascii_fallback():
    result = Heatmap(
        **_make_heatmap_args(),
        options=ChartOptions(use_color=False, use_unicode=False, width=80),
    ).render()
    assert not UNICODE_BLOCKS_RE.search(result), "Expected no Unicode block chars in ASCII mode"


def test_histogram_ascii_fallback():
    result = Histogram(
        data=_make_histogram_data(),
        options=ChartOptions(use_color=False, use_unicode=False, width=80),
    ).render()
    assert not UNICODE_BLOCKS_RE.search(result), "Expected no Unicode block chars in ASCII mode"


def test_unicode_mode_uses_block_or_box_chars():
    result = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(use_color=False, use_unicode=True, width=80),
    ).render()
    # Should use Unicode block elements (U+2580-U+259F) or box-drawing (U+2500-U+257F)
    has_blocks = UNICODE_BLOCKS_RE.search(result)
    has_box = re.search(r"[\u2500-\u257f]", result)
    assert has_blocks or has_box, "Expected Unicode chars in Unicode mode"


# ---------------------------------------------------------------------------
# w3: Theme tests
# ---------------------------------------------------------------------------


def test_dark_vs_light_theme_differ(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    dark = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(theme="dark", width=80),
    ).render()
    light = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(theme="light", width=80),
    ).render()
    assert ANSI_RE.search(dark)
    assert ANSI_RE.search(light)
    assert dark != light
    assert set(ANSI_RE.findall(dark)) != set(ANSI_RE.findall(light))
