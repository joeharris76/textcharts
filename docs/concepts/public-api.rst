Public API model
================

textcharts exports two API layers.

Preferred public API
--------------------

The stable surface for new code is:

- Clean chart class names such as ``BarChart`` and ``Heatmap``
- Data models such as ``BarData`` and ``LinePoint``
- Shared configuration and helpers such as ``ChartOptions`` and ``ColorMode``

This layer is concise, easy to document, and the right basis for external
examples.

For fuller workflow examples built around these APIs, especially benchmark
reporting flows, use the `BenchBox documentation
<https://benchbox.dev/docs/index.html>`_ as the canonical example set.

Compatibility API
-----------------

The package also exports:

- ``ASCII*`` aliases for chart classes
- Factory helpers such as ``from_query_latency_data``,
  ``from_query_results``, ``from_regression_data``,
  ``from_normalized_results``, and ``from_phase_data``

These exist to preserve BenchBox migration paths. They are public and supported,
but they are not the recommended way to write new code against the library.

Performance-oriented surfaces
-----------------------------

Most chart types are documented with general-purpose examples that transfer to
domains such as retail, operations, education, and product analytics.
``NormalizedSpeedup`` is the clearest exception: it is intentionally aimed at
benchmark and performance-analysis workflows.

``ComparisonBar``, ``DivergingBar``, ``PercentileLadder``, ``SummaryBox``, and
``RankTable`` remain broadly useful, but they also overlap naturally with
performance reporting. The docs therefore show generic examples first and then
point to compatibility helpers only where that history matters.

Documentation strategy
----------------------

The docs emphasize the preferred API first, then list compatibility helpers in
reference sections so existing adopters can still find them.
