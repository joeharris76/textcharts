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
``ComparisonBar``      Showing side-by-side baseline vs contender values
``DivergingBar``       Highlighting regression vs improvement around a center
``StackedBar``         Showing composition of a total by segment
``NormalizedSpeedup``  Comparing speedup ratios relative to a baseline
=====================  ============================================

Distribution charts
-------------------

Use these when spread, skew, or percentile behavior matters.

=====================  ============================================
Chart                  Use when
=====================  ============================================
``Histogram``          Showing bucketed frequency counts
``BoxPlot``            Showing quartiles, whiskers, and outliers
``PercentileLadder``   Comparing percentile cut points directly
``CDFChart``           Showing the cumulative shape of a distribution
=====================  ============================================

Trend and relationship charts
-----------------------------

===================  =============================================
Chart                Use when
===================  =============================================
``LineChart``        Showing ordered values over time or sequence
``ScatterPlot``      Showing correlation or cost/performance tradeoffs
``SparklineTable``   Embedding tiny trends inside a textual table
===================  =============================================

Tabular and matrix output
-------------------------

================  ================================================
Chart             Use when
================  ================================================
``Heatmap``       Showing dense matrix intensity at a glance
``RankTable``     Showing rank-ordered matrix summaries
``SummaryBox``    Showing headline metrics and deltas compactly
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
