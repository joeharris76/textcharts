"""textcharts — Beautiful ASCII charts for your terminal.

Zero-dependency library providing 15 chart types for terminal visualization:
bar, histogram, heatmap, box plot, line, scatter, comparison bar, diverging bar,
summary box, percentile ladder, normalized speedup, stacked bar, sparkline table,
CDF chart, and rank table.

Preferred public API:
    - Clean chart names such as ``BarChart`` and ``Heatmap``
    - Data models such as ``BarData`` and ``LinePoint``
    - Shared configuration via ``ChartOptions`` and ``ColorMode``

Compatibility API:
    - ``ASCII*`` aliases are retained for BenchBox migrations
    - Domain-specific factory helpers remain available but are secondary to the
      chart classes and data models above

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
from textcharts.bar_chart import ASCIIBarChart, BarData
from textcharts.bar_chart import from_bar_data  # deprecated compat
from textcharts.bar_chart import from_data as bar_from_data
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
from textcharts.box_plot import ASCIIBoxPlot, BoxPlotSeries, BoxPlotStats
from textcharts.box_plot import from_distribution_series  # deprecated compat
from textcharts.box_plot import from_series as box_from_series
from textcharts.cdf_chart import ASCIICDFChart, CDFSeriesData
from textcharts.cdf_chart import from_query_results as cdf_from_query_results  # deprecated compat
from textcharts.cdf_chart import from_series as cdf_from_series
from textcharts.comparison_bar import ASCIIComparisonBar, ComparisonBarData
from textcharts.comparison_bar import from_comparison_data  # deprecated compat
from textcharts.comparison_bar import from_data as comparison_from_data
from textcharts.diverging_bar import ASCIIDivergingBar, DivergingBarData
from textcharts.diverging_bar import from_data as diverging_from_data
from textcharts.diverging_bar import from_regression_data  # deprecated compat
from textcharts.heatmap import ASCIIHeatmap, from_matrix
from textcharts.histogram import ASCIIHistogram, ASCIIQueryHistogram, HistogramBar
from textcharts.histogram import from_data as histogram_from_data
from textcharts.histogram import from_query_latency_data  # deprecated compat
from textcharts.line_chart import ASCIILineChart, LinePoint
from textcharts.line_chart import from_points as line_from_points
from textcharts.line_chart import from_time_series_points  # deprecated compat
from textcharts.normalized_speedup import ASCIINormalizedSpeedup, SpeedupData
from textcharts.normalized_speedup import from_normalized_results  # deprecated compat
from textcharts.normalized_speedup import from_ratios as speedup_from_ratios
from textcharts.percentile_ladder import ASCIIPercentileLadder, PercentileData
from textcharts.percentile_ladder import from_query_results as percentile_from_query_results  # deprecated compat
from textcharts.percentile_ladder import from_series as percentile_from_series
from textcharts.rank_table import ASCIIRankTable, RankTableData
from textcharts.rank_table import from_heatmap_data  # deprecated compat
from textcharts.rank_table import from_matrix as rank_from_matrix
from textcharts.scatter_plot import ASCIIScatterPlot, ScatterPoint
from textcharts.scatter_plot import from_cost_performance_points  # deprecated compat
from textcharts.scatter_plot import from_points as scatter_from_points
from textcharts.sparkline_table import ASCIISparklineTable, SparklineColumn, SparklineTableData
from textcharts.sparkline_table import from_data as sparkline_from_data
from textcharts.sparkline_table import from_metrics  # deprecated compat
from textcharts.stacked_bar import ASCIIStackedBar, StackedBarData, StackedBarSegment
from textcharts.stacked_bar import from_data as stacked_from_data
from textcharts.stacked_bar import from_phase_data  # deprecated compat
from textcharts.summary_box import ASCIISummaryBox, SummaryStats

# ---------------------------------------------------------------------------
# Clean standalone aliases (preferred public API)
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
    # BenchBox-compatible aliases retained for migration compatibility
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
    # Factory functions — new generic names (preferred)
    "bar_from_data",
    "box_from_series",
    "cdf_from_series",
    "comparison_from_data",
    "diverging_from_data",
    "from_matrix",
    "histogram_from_data",
    "line_from_points",
    "percentile_from_series",
    "rank_from_matrix",
    "scatter_from_points",
    "sparkline_from_data",
    "speedup_from_ratios",
    "stacked_from_data",
    # Factory functions — deprecated names (kept for backwards compatibility)
    "cdf_from_query_results",
    "from_bar_data",
    "from_comparison_data",
    "from_cost_performance_points",
    "from_distribution_series",
    "from_heatmap_data",
    "from_metrics",
    "from_normalized_results",
    "from_phase_data",
    "from_query_latency_data",
    "from_regression_data",
    "from_time_series_points",
    "percentile_from_query_results",
]
