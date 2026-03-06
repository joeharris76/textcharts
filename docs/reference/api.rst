API reference
=============

Package overview
----------------

The top-level package re-exports the preferred public API:

=======================  ============================================
Category                 Symbols
=======================  ============================================
Chart classes            ``BarChart``, ``Heatmap``, ``LineChart``, ``SummaryBox``, ``Histogram``, ``BoxPlot``, ``ScatterPlot``, ``CDFChart``, ``ComparisonBar``, ``DivergingBar``, ``NormalizedSpeedup``, ``PercentileLadder``, ``RankTable``, ``SparklineTable``, ``StackedBar``
Shared configuration     ``ChartOptions``, ``ChartBase``, ``ColorMode``
Data models              ``BarData``, ``HistogramBar``, ``LinePoint``, ``ScatterPoint``, ``SpeedupData``, ``SummaryStats`` and chart-specific companions
Compatibility aliases    ``ASCII*`` chart names retained for BenchBox migrations
Factory helpers          ``from_*`` conversion helpers for compatibility and one-shot data shaping
=======================  ============================================

Use :doc:`charts` and :doc:`factories` for the canonical symbol-level
documentation.

Shared configuration and utilities
----------------------------------

.. automodule:: textcharts.base
   :members: ASCIIChartBase, ASCIIChartOptions, TerminalCapabilities, TerminalColors, ColorMode, detect_terminal_capabilities, compute_percentile_linear, robust_p95, outlier_severity_markers
   :undoc-members: False
