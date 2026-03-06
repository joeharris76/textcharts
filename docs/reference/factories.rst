Factory helpers
===============

The preferred API is class-based, but the package also exports convenience
helpers used during BenchBox migrations and for compact one-shot conversions.

Generic convenience helpers
---------------------------

These helpers stay close to the preferred public API and are useful outside any
performance-analysis workflow.

.. autofunction:: textcharts.bar_chart.from_bar_data
   :no-index:

.. autofunction:: textcharts.box_plot.from_distribution_series
   :no-index:

.. autofunction:: textcharts.comparison_bar.from_comparison_data
   :no-index:

.. autofunction:: textcharts.heatmap.from_matrix
   :no-index:

.. autofunction:: textcharts.line_chart.from_time_series_points
   :no-index:

.. autofunction:: textcharts.rank_table.from_heatmap_data
   :no-index:

.. autofunction:: textcharts.sparkline_table.from_metrics
   :no-index:

BenchBox-derived and performance-oriented helpers
-------------------------------------------------

These functions remain public for compatibility and migration scenarios. New
code should prefer constructing chart classes from their data models directly.

.. autofunction:: textcharts.cdf_chart.from_query_results
   :no-index:

.. autofunction:: textcharts.diverging_bar.from_regression_data
   :no-index:

.. autofunction:: textcharts.histogram.from_query_latency_data
   :no-index:

.. autofunction:: textcharts.normalized_speedup.from_normalized_results
   :no-index:

.. autofunction:: textcharts.percentile_ladder.from_query_results
   :no-index:

.. autofunction:: textcharts.scatter_plot.from_cost_performance_points
   :no-index:

.. autofunction:: textcharts.stacked_bar.from_phase_data
   :no-index:
