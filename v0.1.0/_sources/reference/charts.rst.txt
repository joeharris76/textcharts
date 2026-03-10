Chart classes and data models
=============================

This page documents the primary chart constructors and the structured data
models used by the clean API.

Bar and comparison charts
-------------------------

.. automodule:: textcharts.bar_chart
   :members: BarChart, BarData

.. automodule:: textcharts.comparison_bar
   :members: ComparisonBar, ComparisonBarData

.. automodule:: textcharts.diverging_bar
   :members: DivergingBar, DivergingBarData

.. automodule:: textcharts.stacked_bar
   :members: StackedBar, StackedBarData, StackedBarSegment

Distribution charts
-------------------

.. automodule:: textcharts.histogram
   :members: Histogram, HistogramBar

.. automodule:: textcharts.box_plot
   :members: BoxPlot, BoxPlotSeries, BoxPlotStats

.. automodule:: textcharts.percentile_ladder
   :members: PercentileLadder, PercentileData

.. automodule:: textcharts.cdf_chart
   :members: CDFChart, CDFSeriesData

Trend and relationship charts
-----------------------------

.. automodule:: textcharts.line_chart
   :members: LineChart, LinePoint

.. automodule:: textcharts.scatter_plot
   :members: ScatterPlot, ScatterPoint

.. automodule:: textcharts.normalized_speedup
   :members: NormalizedSpeedup, SpeedupData

Tabular and matrix charts
-------------------------

.. automodule:: textcharts.heatmap
   :members: Heatmap

.. automodule:: textcharts.rank_table
   :members: RankTable, RankTableData

.. automodule:: textcharts.sparkline_table
   :members: SparklineTable, SparklineColumn, SparklineTableData

.. automodule:: textcharts.summary_box
   :members: SummaryBox, SummaryStats
