textcharts
==========

Beautiful text-based charts for your terminal — zero dependencies.

15 chart types with Unicode box-drawing, ANSI colors, and automatic terminal
width detection. Pure Python, no external dependencies, Python 3.10+.


.. image:: /_static/screenshots/box_plot/color.png
   :alt: Box plot chart rendered in the terminal
   :width: 100%

.. code-block:: python

   from textcharts import BoxPlot, BoxPlotSeries

   series = [
       BoxPlotSeries(name="Downtown", values=[1825, 1900, 1980, 2100, 2250, 2400, 2550, 2710, 2980]),
       BoxPlotSeries(name="Riverside", values=[1450, 1525, 1600, 1680, 1750, 1820, 1950, 2080, 2220]),
       BoxPlotSeries(name="Midtown", values=[1650, 1710, 1780, 1840, 1920, 2010, 2140, 2280, 2450]),
   ]
   chart = BoxPlot(
       series=series,
       title="Apartment Rents",
       subtitle="Monthly rent distribution by neighborhood",
   )
   print(chart.render())


Install
-------

.. code-block:: bash

   pip install textcharts


Features
--------

**Domain-neutral defaults** — generic labels and titles out of the box. Add
context with the ``subject`` parameter (e.g., ``subject="Query Latency"``
turns "Histogram" into "Query Latency Histogram").

**Adaptive rendering** — auto-detects terminal width, color support, and
Unicode capabilities. Falls back to ASCII-safe, plain-text output in
non-interactive contexts.

**Configurable at every level** — ``ChartOptions`` controls color, width,
theme, Unicode, and outlier capping. Per-chart parameters cover metric labels,
improvement direction (``lower_is_better``), and value formatting.

**Three interfaces** — Python API, CLI (``textcharts bar --title "Revenue"``),
and MCP server for AI tool use (``pip install textcharts[mcp]``).


Chart types
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25

   * - Chart
     - Class
     - Data model
   * - Bar chart
     - ``BarChart``
     - ``BarData``
   * - Histogram
     - ``Histogram``
     - ``HistogramBar``
   * - Heatmap
     - ``Heatmap``
     - matrix + labels
   * - Box plot
     - ``BoxPlot``
     - ``BoxPlotSeries``
   * - Line chart
     - ``LineChart``
     - ``LinePoint``
   * - Scatter plot
     - ``ScatterPlot``
     - ``ScatterPoint``
   * - Comparison bar
     - ``ComparisonBar``
     - ``ComparisonBarData``
   * - Diverging bar
     - ``DivergingBar``
     - ``DivergingBarData``
   * - Summary box
     - ``SummaryBox``
     - ``SummaryStats``
   * - Percentile ladder
     - ``PercentileLadder``
     - ``PercentileData``
   * - Normalized speedup
     - ``NormalizedSpeedup``
     - ``SpeedupData``
   * - Stacked bar
     - ``StackedBar``
     - ``StackedBarData``
   * - Sparkline table
     - ``SparklineTable``
     - ``SparklineTableData``
   * - CDF chart
     - ``CDFChart``
     - ``CDFSeriesData``
   * - Rank table
     - ``RankTable``
     - ``RankTableData``

See the :doc:`guides/chart-gallery` for rendered screenshots of every chart
type in color, greyscale, and monochrome modes.


.. toctree::
   :maxdepth: 2
   :caption: Start here
   :hidden:

   tutorials/first-chart
   guides/chart-selection
   guides/chart-gallery
   guides/configuration
   concepts/public-api
   concepts/rendering-behavior

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   reference/index
   reference/api
   reference/charts
   reference/factories

.. toctree::
   :maxdepth: 2
   :caption: Project
   :hidden:

   project/development
