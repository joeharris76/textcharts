Configuration guide
===================

Shared rendering options
------------------------

All charts accept :class:`textcharts.ChartOptions`.

.. code-block:: python

   from textcharts import ChartOptions

   options = ChartOptions(
       width=100,
       use_color=True,
       use_unicode=True,
       show_legend=True,
       theme="dark",
   )

Width behavior
--------------

- ``width=None`` uses detected terminal width.
- Extremely small widths are clamped upward so charts remain legible.
- Very large widths are capped to avoid runaway output.

Color behavior
--------------

Color is capability-aware by default:

- ANSI color is emitted only when the terminal supports it.
- ``NO_COLOR`` disables color even if the terminal is interactive.
- Non-interactive output defaults to plain text without escape sequences.

You can still force plain output with ``use_color=False``.

Unicode behavior
----------------

Unicode box-drawing and block characters are enabled when the environment
appears UTF-8 capable. Set ``use_unicode=False`` to force ASCII-safe output.

Heatmap color schemes
---------------------

:class:`textcharts.Heatmap` supports two color schemes:

- ``diverging`` for values centered around a neutral midpoint
- ``sequential`` for monotonic low-to-high intensity

Matrix validation
-----------------

Matrix-based renderers fail fast on shape mismatches:

- ``len(row_labels)`` must equal ``len(matrix)``
- Every row in ``matrix`` must have the same length as ``col_labels``

This is deliberate. Silent truncation is convenient in an internal app, but it
is a poor contract for a public library.
