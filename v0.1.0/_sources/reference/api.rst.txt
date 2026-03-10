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
Factory helpers          ``from_*`` convenience helpers for one-shot chart creation
=======================  ============================================

Use :doc:`charts` and :doc:`factories` for the canonical symbol-level
documentation.

Shared configuration and utilities
----------------------------------

.. automodule:: textcharts.base
   :members: ChartBase, ChartOptions, TerminalCapabilities, TerminalColors, ColorMode, detect_terminal_capabilities, compute_percentile_linear, robust_p95, outlier_severity_markers
   :undoc-members: False
