Chart classes and data models
=============================

This page documents the primary chart constructors and the structured data
models used by the clean API.

Bar and comparison charts
-------------------------

.. automodule:: textcharts.bar_chart
   :members: ASCIIBarChart, BarData

.. automodule:: textcharts.comparison_bar
   :members: ASCIIComparisonBar, ComparisonBarData

.. automodule:: textcharts.diverging_bar
   :members: ASCIIDivergingBar, DivergingBarData

.. automodule:: textcharts.stacked_bar
   :members: ASCIIStackedBar, StackedBarData, StackedBarSegment

Distribution charts
-------------------

.. automodule:: textcharts.histogram
   :members: ASCIIHistogram, ASCIIQueryHistogram, HistogramBar

.. automodule:: textcharts.box_plot
   :members: ASCIIBoxPlot, BoxPlotSeries, BoxPlotStats

.. automodule:: textcharts.percentile_ladder
   :members: ASCIIPercentileLadder, PercentileData

.. automodule:: textcharts.cdf_chart
   :members: ASCIICDFChart, CDFSeriesData

Trend and relationship charts
-----------------------------

.. automodule:: textcharts.line_chart
   :members: ASCIILineChart, LinePoint

.. automodule:: textcharts.scatter_plot
   :members: ASCIIScatterPlot, ScatterPoint

.. automodule:: textcharts.normalized_speedup
   :members: ASCIINormalizedSpeedup, SpeedupData

Tabular and matrix charts
-------------------------

.. automodule:: textcharts.heatmap
   :members: ASCIIHeatmap

.. automodule:: textcharts.rank_table
   :members: ASCIIRankTable, RankTableData

.. automodule:: textcharts.sparkline_table
   :members: ASCIISparklineTable, SparklineColumn, SparklineTableData

.. automodule:: textcharts.summary_box
   :members: ASCIISummaryBox, SummaryStats
