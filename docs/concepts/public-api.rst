Public API model
================

textcharts exports a single, clean API layer.

Chart classes and data models
-----------------------------

The public surface is:

- Clean chart class names such as ``BarChart`` and ``Heatmap``
- Data models such as ``BarData`` and ``LinePoint``
- Shared configuration and helpers such as ``ChartOptions`` and ``ColorMode``

This layer is concise, easy to document, and the right basis for external
examples.

Performance-oriented surfaces
-----------------------------

Most chart types are documented with general-purpose examples that transfer to
domains such as retail, operations, education, and product analytics.
``NormalizedSpeedup`` is the clearest exception: it is intentionally aimed at
benchmark and performance-analysis workflows.

``ComparisonBar``, ``DivergingBar``, ``PercentileLadder``, ``SummaryBox``, and
``RankTable`` remain broadly useful, but they also overlap naturally with
performance reporting.

Documentation strategy
----------------------

The docs emphasize the chart classes and data models first, then list
convenience factory helpers in reference sections.
