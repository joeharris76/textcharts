Choosing a chart
================

The library exposes 15 chart types. The right one depends on the question you
want the terminal output to answer.

Comparison charts
-----------------

Use these when the reader needs to compare magnitudes or relative change.

=====================  ============================================
Chart                  Use when
=====================  ============================================
``BarChart``           Comparing independent values across categories
``ComparisonBar``      Showing planned vs actual or before vs after values
``DivergingBar``       Highlighting positive and negative change around a center
``StackedBar``         Showing composition of a total by segment
``NormalizedSpeedup``  Comparing speedup ratios in performance analysis
=====================  ============================================

Distribution charts
-------------------

Use these when spread, skew, or percentile behavior matters.

=====================  ============================================
Chart                  Use when
=====================  ============================================
``Histogram``          Showing bucketed frequency counts
``BoxPlot``            Showing quartiles, whiskers, and outliers
``PercentileLadder``   Comparing percentile cut points across groups
``CDFChart``           Showing the cumulative shape of a distribution
=====================  ============================================

Trend and relationship charts
-----------------------------

===================  =============================================
Chart                Use when
===================  =============================================
``LineChart``        Showing ordered values over time or sequence
``ScatterPlot``      Showing correlation such as ad spend vs conversions
``SparklineTable``   Embedding tiny trends inside a textual table
===================  =============================================

Tabular and matrix output
-------------------------

================  ================================================
Chart             Use when
================  ================================================
``Heatmap``       Showing dense matrix intensity at a glance
``RankTable``     Showing rank-ordered summaries across criteria
``SummaryBox``    Showing headline metrics and deltas in one panel
================  ================================================

Preferred API
-------------

For new code, use the clean exported names and their data models:

- ``BarChart`` with ``BarData``
- ``Heatmap`` with matrix and labels
- ``LineChart`` with ``LinePoint``
- ``SummaryBox`` with ``SummaryStats``

The ``ASCII*`` aliases are retained for BenchBox migration compatibility, but
they are not the preferred surface for new integrations.

Performance-specific note
-------------------------

``NormalizedSpeedup`` is the chart type most closely tied to benchmark and
performance-analysis workflows. ``ComparisonBar``, ``DivergingBar``,
``PercentileLadder``, ``RankTable``, and ``SummaryBox`` are still general
purpose charts, but they also map naturally to performance reporting and
compatibility helpers inherited from BenchBox.
