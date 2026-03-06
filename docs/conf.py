"""Sphinx configuration for textcharts."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, os.fspath(SRC))

project = "textcharts"
author = "Joe Harris"
copyright = "2026, Joe Harris"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_class_signature = "mixed"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "undoc-members": False,
}

html_theme = "alabaster"
html_static_path = ["_static"]
html_title = "textcharts documentation"
html_theme_options = {
    "description": "Zero-dependency terminal charts for Python",
    "fixed_sidebar": True,
    "page_width": "1200px",
    "sidebar_width": "260px",
    "body_max_width": "900px",
}

_MARKDOWN_CLASS_DOCS = {
    "textcharts.box_plot.ASCIIBoxPlot",
    "textcharts.cdf_chart.ASCIICDFChart",
    "textcharts.comparison_bar.ASCIIComparisonBar",
    "textcharts.diverging_bar.ASCIIDivergingBar",
    "textcharts.heatmap.ASCIIHeatmap",
    "textcharts.histogram.ASCIIQueryHistogram",
    "textcharts.line_chart.ASCIILineChart",
    "textcharts.normalized_speedup.ASCIINormalizedSpeedup",
    "textcharts.scatter_plot.ASCIIScatterPlot",
}


def _sanitize_docstring(_app, what, name, _obj, _options, lines):
    """Replace markdown-fenced class docstrings with a short plain summary."""
    if what != "class" or name not in _MARKDOWN_CLASS_DOCS:
        return
    summary = next((line.strip() for line in lines if line.strip()), "")
    lines[:] = [summary]


def setup(app):
    """Register Sphinx hooks."""
    app.connect("autodoc-process-docstring", _sanitize_docstring)
