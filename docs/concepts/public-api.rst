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

Compatibility API
-----------------

The package also exports:

- ``ASCII*`` aliases for chart classes
- Factory helpers such as ``from_query_latency_data`` and ``from_phase_data``

These exist to preserve BenchBox migration paths. They are public and supported,
but they are not the recommended way to write new code against the library.

Documentation strategy
----------------------

The docs emphasize the preferred API first, then list compatibility helpers in
reference sections so existing adopters can still find them.
