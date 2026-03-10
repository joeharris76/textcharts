CLI Usage
=========

textcharts provides a command-line interface for rendering charts from JSON data
piped via stdin or read from a file.

Quick start
-----------

.. code-block:: bash

   echo '[{"label": "A", "value": 10}, {"label": "B", "value": 25}]' | textcharts bar

   textcharts bar -f data.json --title "Revenue by Region"

Available commands
------------------

.. code-block:: bash

   textcharts list                # show all chart types
   textcharts <type> --help       # show usage for a specific chart type

All 15 chart types are available as subcommands:

.. code-block:: text

   bar         Horizontal bar chart
   histogram   Vertical bar histogram
   heatmap     Matrix heatmap
   boxplot     Box plot with quartiles
   line        Line chart for trends
   scatter     Scatter plot with Pareto frontier
   comparison  Side-by-side paired bar chart
   diverging   Centered diverging bar chart
   summary     Bordered summary statistics box
   percentile  Percentile band chart (P50/P90/P95/P99)
   speedup     Log-scale normalized speedup chart
   stacked     Stacked horizontal bar chart
   sparkline   Compact table with sparkline mini-charts
   cdf         Cumulative distribution function chart
   rank        Competitive ranking table

Input
-----

Data is read from **stdin** by default (pipe JSON in), or from a file with
``-f PATH``:

.. code-block:: bash

   # From stdin
   cat data.json | textcharts histogram --title "Latency Distribution"

   # From file
   textcharts histogram -f data.json --title "Latency Distribution"

See :doc:`/input-formats` for the JSON schema of each chart type.

Common options
--------------

All chart subcommands accept these flags:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``--title TEXT``
     - Chart title
   * - ``--subtitle TEXT``
     - Subtitle line below the title
   * - ``--width N``
     - Chart width in characters (default: auto-detect terminal)
   * - ``--height N``
     - Chart height in rows (default: auto)
   * - ``--no-color``
     - Disable ANSI color output
   * - ``--no-unicode``
     - Disable Unicode box-drawing (ASCII fallback)
   * - ``--theme light|dark``
     - Color theme

Chart-specific options (like ``--metric-label``, ``--sort-by``) are listed in
each subcommand's ``--help`` output.

Examples
--------

Bar chart with custom title and no color:

.. code-block:: bash

   echo '[
     {"label": "Fiction", "value": 18.4},
     {"label": "Children", "value": 14.2},
     {"label": "Comics", "value": 9.8}
   ]' | textcharts bar --title "Bookstore Revenue" --no-color

Box plot from file:

.. code-block:: bash

   textcharts boxplot -f latencies.json --title "Response Times"

Heatmap piped from a script:

.. code-block:: bash

   python generate_data.py | textcharts heatmap --no-unicode
