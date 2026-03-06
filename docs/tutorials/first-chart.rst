First chart
===========

This tutorial walks through the fastest path from install to useful output.

Install
-------

.. code-block:: bash

   pip install textcharts

Render a basic bar chart
------------------------

.. code-block:: python

   from textcharts import BarChart, BarData

   data = [
       BarData(label="DuckDB", value=1.0, is_best=True),
       BarData(label="SQLite", value=1.8),
       BarData(label="Postgres", value=2.4, is_worst=True),
   ]

   chart = BarChart(
       data=data,
       title="Median query latency",
       metric_label="seconds",
   )

   print(chart.render())

What to expect
--------------

- Labels are aligned and sorted for readability.
- Best and worst values can be highlighted through the data model.
- Unicode and color are enabled by default when the terminal supports them.

Use shared chart options
------------------------

All chart types accept :class:`textcharts.ChartOptions`.

.. code-block:: python

   from textcharts import BarChart, BarData, ChartOptions

   options = ChartOptions(
       width=72,
       use_color=False,
       use_unicode=False,
   )

   chart = BarChart(
       data=[BarData(label="Python", value=89.5)],
       title="Compatibility mode",
       options=options,
   )

   print(chart.render())

Build a chart from structured data
----------------------------------

Most charts have a dedicated data model:

- :class:`textcharts.BarData`
- :class:`textcharts.LinePoint`
- :class:`textcharts.ScatterPoint`
- :class:`textcharts.SpeedupData`
- :class:`textcharts.SummaryStats`

Use those models directly for new code. Compatibility factory helpers are still
available when migrating from BenchBox, but they are secondary to the clean
class-based API.

Next steps
----------

- Read :doc:`../guides/chart-selection` to choose the right visualization.
- Read :doc:`../guides/configuration` to control width, color, and Unicode.
- Use :doc:`../reference/charts` for chart-specific constructors and data
  models.
