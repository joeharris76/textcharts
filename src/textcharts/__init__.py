"""textcharts — Beautiful ASCII charts for your terminal.

Zero-dependency library providing 15 chart types for terminal visualization:
bar, histogram, heatmap, box plot, line, scatter, comparison bar, diverging bar,
summary box, percentile ladder, normalized speedup, stacked bar, sparkline table,
CDF chart, and rank table.

Basic usage::

    from textcharts import BarChart, BarData, ChartOptions

    data = [
        BarData(label="Python", value=89.5),
        BarData(label="Rust", value=95.2),
        BarData(label="Go", value=78.0),
    ]
    chart = BarChart(data=data, title="Language Benchmark")
    print(chart.render())
"""

__version__ = "0.1.0"

# ---------------------------------------------------------------------------
# Base class and configuration
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Chart classes
# ---------------------------------------------------------------------------
from textcharts.bar_chart import ASCIIBarChart, BarData, from_bar_data
from textcharts.base import (
    ASCIIChartBase,
    ASCIIChartOptions,
    ColorMode,
    TerminalCapabilities,
    TerminalColors,
    compute_percentile_linear,
    detect_terminal_capabilities,
    outlier_severity_markers,
    robust_p95,
)
from textcharts.box_plot import ASCIIBoxPlot, BoxPlotSeries, BoxPlotStats, from_distribution_series
from textcharts.cdf_chart import ASCIICDFChart, CDFSeriesData
from textcharts.cdf_chart import from_query_results as cdf_from_query_results
from textcharts.comparison_bar import ASCIIComparisonBar, ComparisonBarData, from_comparison_data
from textcharts.diverging_bar import ASCIIDivergingBar, DivergingBarData, from_regression_data
from textcharts.heatmap import ASCIIHeatmap, from_matrix
from textcharts.histogram import ASCIIHistogram, ASCIIQueryHistogram, HistogramBar, from_query_latency_data
from textcharts.line_chart import ASCIILineChart, LinePoint, from_time_series_points
from textcharts.normalized_speedup import ASCIINormalizedSpeedup, SpeedupData, from_normalized_results
from textcharts.percentile_ladder import ASCIIPercentileLadder, PercentileData
from textcharts.percentile_ladder import from_query_results as percentile_from_query_results
from textcharts.rank_table import ASCIIRankTable, RankTableData, from_heatmap_data
from textcharts.scatter_plot import ASCIIScatterPlot, ScatterPoint, from_cost_performance_points
from textcharts.sparkline_table import ASCIISparklineTable, SparklineColumn, SparklineTableData, from_metrics
from textcharts.stacked_bar import ASCIIStackedBar, StackedBarData, StackedBarSegment, from_phase_data
from textcharts.summary_box import ASCIISummaryBox, SummaryStats

# ---------------------------------------------------------------------------
# Clean standalone aliases (drop ASCII prefix)
# ---------------------------------------------------------------------------
ChartBase = ASCIIChartBase
ChartOptions = ASCIIChartOptions
BarChart = ASCIIBarChart
BoxPlot = ASCIIBoxPlot
CDFChart = ASCIICDFChart
ComparisonBar = ASCIIComparisonBar
DivergingBar = ASCIIDivergingBar
Heatmap = ASCIIHeatmap
Histogram = ASCIIHistogram
LineChart = ASCIILineChart
NormalizedSpeedup = ASCIINormalizedSpeedup
PercentileLadder = ASCIIPercentileLadder
RankTable = ASCIIRankTable
ScatterPlot = ASCIIScatterPlot
SparklineTable = ASCIISparklineTable
StackedBar = ASCIIStackedBar
SummaryBox = ASCIISummaryBox

__all__ = [
    "__version__",
    # Clean standalone names (preferred)
    "BarChart",
    "BoxPlot",
    "CDFChart",
    "ChartBase",
    "ChartOptions",
    "ComparisonBar",
    "DivergingBar",
    "Heatmap",
    "Histogram",
    "LineChart",
    "NormalizedSpeedup",
    "PercentileLadder",
    "RankTable",
    "ScatterPlot",
    "SparklineTable",
    "StackedBar",
    "SummaryBox",
    # BenchBox-compatible names (aliases)
    "ASCIIBarChart",
    "ASCIIBoxPlot",
    "ASCIICDFChart",
    "ASCIIChartBase",
    "ASCIIChartOptions",
    "ASCIIComparisonBar",
    "ASCIIDivergingBar",
    "ASCIIHeatmap",
    "ASCIIHistogram",
    "ASCIILineChart",
    "ASCIINormalizedSpeedup",
    "ASCIIPercentileLadder",
    "ASCIIQueryHistogram",
    "ASCIIRankTable",
    "ASCIIScatterPlot",
    "ASCIISparklineTable",
    "ASCIIStackedBar",
    "ASCIISummaryBox",
    # Configuration and utilities
    "ColorMode",
    "TerminalCapabilities",
    "TerminalColors",
    "compute_percentile_linear",
    "detect_terminal_capabilities",
    "outlier_severity_markers",
    "robust_p95",
    # Data models
    "BarData",
    "BoxPlotSeries",
    "BoxPlotStats",
    "CDFSeriesData",
    "ComparisonBarData",
    "DivergingBarData",
    "HistogramBar",
    "LinePoint",
    "PercentileData",
    "RankTableData",
    "ScatterPoint",
    "SparklineColumn",
    "SparklineTableData",
    "SpeedupData",
    "StackedBarData",
    "StackedBarSegment",
    "SummaryStats",
    # Factory functions
    "cdf_from_query_results",
    "from_bar_data",
    "from_comparison_data",
    "from_cost_performance_points",
    "from_distribution_series",
    "from_heatmap_data",
    "from_matrix",
    "from_metrics",
    "from_normalized_results",
    "from_phase_data",
    "from_query_latency_data",
    "from_regression_data",
    "from_time_series_points",
    "percentile_from_query_results",
]
