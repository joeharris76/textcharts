"""Tests for the textcharts MCP server.

Tests tool registration, schema generation, tool execution for all 15 chart
types, meta-tools, and error handling. Uses create_server() for direct testing.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

# Skip entire module if mcp is not installed
mcp = pytest.importorskip("mcp")

from mcp.server.fastmcp.exceptions import ToolError  # noqa: E402

from textcharts.mcp_server import _HAS_MCP, create_server  # noqa: E402

# Sample data for each chart type (matches test_commands.py)
SAMPLE_DATA: dict[str, Any] = {
    "bar": [{"label": "A", "value": 10}, {"label": "B", "value": 20}, {"label": "C", "value": 15}],
    "histogram": [
        {"query_id": "Q1", "latency_ms": 100},
        {"query_id": "Q2", "latency_ms": 200},
        {"query_id": "Q3", "latency_ms": 150},
    ],
    "heatmap": {
        "matrix": [[10, 20], [30, 40]],
        "row_labels": ["Q1", "Q2"],
        "col_labels": ["DuckDB", "SQLite"],
    },
    "boxplot": [
        {"name": "A", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        {"name": "B", "values": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]},
    ],
    "line": [
        {"series": "S1", "x": 1, "y": 10},
        {"series": "S1", "x": 2, "y": 20},
        {"series": "S1", "x": 3, "y": 15},
    ],
    "scatter": [
        {"name": "P1", "x": 1, "y": 10},
        {"name": "P2", "x": 2, "y": 20},
        {"name": "P3", "x": 3, "y": 15},
    ],
    "comparison": [
        {"label": "Q1", "baseline_value": 100, "comparison_value": 80},
        {"label": "Q2", "baseline_value": 200, "comparison_value": 150},
    ],
    "diverging": [
        {"label": "Q1", "pct_change": -20},
        {"label": "Q2", "pct_change": 15},
        {"label": "Q3", "pct_change": -5},
    ],
    "summary": {"title": "Test Summary", "geo_mean_ms": 42.5, "median_ms": 40.0, "num_queries": 10},
    "percentile": [
        {"name": "Q1", "p50": 10, "p90": 20, "p95": 25, "p99": 30},
        {"name": "Q2", "p50": 15, "p90": 25, "p95": 30, "p99": 40},
    ],
    "speedup": [
        {"name": "DuckDB", "ratio": 2.5},
        {"name": "Postgres", "ratio": 1.5},
        {"name": "SQLite", "ratio": 1.0, "is_baseline": True},
    ],
    "stacked": [
        {"label": "Q1", "segments": [{"phase_name": "Parse", "value": 10}, {"phase_name": "Execute", "value": 90}]},
        {"label": "Q2", "segments": [{"phase_name": "Parse", "value": 20}, {"phase_name": "Execute", "value": 80}]},
    ],
    "sparkline": {
        "rows": ["DuckDB", "SQLite"],
        "columns": [
            {"name": "Latency (ms)", "values": {"DuckDB": 10, "SQLite": 20}},
            {"name": "Throughput", "values": {"DuckDB": 100, "SQLite": 50}, "higher_is_better": True},
        ],
    },
    "cdf": [
        {"name": "A", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        {"name": "B", "values": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]},
    ],
    "rank": {
        "queries": ["Q1", "Q2"],
        "platforms": ["DuckDB", "SQLite"],
        "times": {"DuckDB,Q1": 10, "DuckDB,Q2": 20, "SQLite,Q1": 15, "SQLite,Q2": 25},
    },
}


@pytest.fixture
def server():
    """Create a fresh MCP server for each test."""
    return create_server()


def _call_tool(server, name: str, args: dict) -> str:
    """Helper: call a tool synchronously and return the text content."""
    result = asyncio.run(server.call_tool(name, args))
    # result is a tuple of (content_list, result_dict)
    content_list = result[0]
    return content_list[0].text


# ---------------------------------------------------------------------------
# Tool registration tests
# ---------------------------------------------------------------------------


class TestToolRegistration:
    def test_mcp_available(self):
        assert _HAS_MCP is True

    def test_total_tool_count(self, server):
        tools = asyncio.run(server.list_tools())
        assert len(tools) == 17  # 15 charts + list + describe

    def test_chart_tools_registered(self, server):
        tools = asyncio.run(server.list_tools())
        tool_names = {t.name for t in tools}
        for chart_name in SAMPLE_DATA:
            assert f"textcharts_{chart_name}" in tool_names

    def test_meta_tools_registered(self, server):
        tools = asyncio.run(server.list_tools())
        tool_names = {t.name for t in tools}
        assert "textcharts_list" in tool_names
        assert "textcharts_describe" in tool_names

    def test_tools_have_descriptions(self, server):
        tools = asyncio.run(server.list_tools())
        for tool in tools:
            assert tool.description, f"{tool.name} has no description"
            assert len(tool.description) > 10

    def test_tools_have_input_schemas(self, server):
        tools = asyncio.run(server.list_tools())
        for tool in tools:
            assert tool.inputSchema is not None
            assert "properties" in tool.inputSchema


# ---------------------------------------------------------------------------
# Chart tool execution tests
# ---------------------------------------------------------------------------


class TestChartToolExecution:
    @pytest.mark.parametrize("chart_name", sorted(SAMPLE_DATA.keys()))
    def test_render_all_chart_types(self, server, chart_name):
        text = _call_tool(server, f"textcharts_{chart_name}", {
            "data": SAMPLE_DATA[chart_name],
            "use_color": False,
        })
        assert isinstance(text, str)
        assert len(text.strip()) > 0

    def test_render_with_title(self, server):
        text = _call_tool(server, "textcharts_bar", {
            "data": SAMPLE_DATA["bar"],
            "title": "My Title",
            "use_color": False,
        })
        assert "My Title" in text

    def test_render_with_subject(self, server):
        text = _call_tool(server, "textcharts_bar", {
            "data": SAMPLE_DATA["bar"],
            "subject": "Revenue",
            "use_color": False,
        })
        assert "Revenue Bar Chart" in text

    def test_render_with_chart_params(self, server):
        text = _call_tool(server, "textcharts_bar", {
            "data": SAMPLE_DATA["bar"],
            "use_color": False,
            "chart_params": {"sort_by": "label", "metric_label": "Score"},
        })
        assert "Score" in text

    def test_render_with_width(self, server):
        text = _call_tool(server, "textcharts_bar", {
            "data": SAMPLE_DATA["bar"],
            "use_color": False,
            "width": 60,
        })
        assert len(text.strip()) > 0

    def test_render_with_dark_theme(self, server):
        text = _call_tool(server, "textcharts_bar", {
            "data": SAMPLE_DATA["bar"],
            "use_color": False,
            "theme": "dark",
        })
        assert len(text.strip()) > 0

    def test_invalid_data_raises_tool_error(self, server):
        with pytest.raises(ToolError):
            asyncio.run(server.call_tool("textcharts_bar", {"data": "not_a_list"}))

    def test_parse_error_returns_error_message(self, server):
        # Empty list passes pydantic but fails our parser
        text = _call_tool(server, "textcharts_bar", {
            "data": [],
            "use_color": False,
        })
        assert "Error:" in text


# ---------------------------------------------------------------------------
# Meta-tool tests
# ---------------------------------------------------------------------------


class TestMetaTools:
    def test_list_tool(self, server):
        text = _call_tool(server, "textcharts_list", {})
        assert "Available chart types (15):" in text
        for chart_name in SAMPLE_DATA:
            assert f"textcharts_{chart_name}" in text

    def test_describe_tool(self, server):
        text = _call_tool(server, "textcharts_describe", {"chart_type": "bar"})
        assert '"name": "bar"' in text
        assert "data_fields" in text
        assert "chart_params" in text

    def test_describe_with_prefix(self, server):
        text = _call_tool(server, "textcharts_describe", {"chart_type": "textcharts_heatmap"})
        assert '"name": "heatmap"' in text

    def test_describe_unknown_type(self, server):
        text = _call_tool(server, "textcharts_describe", {"chart_type": "nonexistent"})
        assert "Unknown chart type" in text
