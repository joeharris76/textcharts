Development
===========

See `CONTRIBUTING.md <https://github.com/joeharris76/textcharts/blob/dev-0.1.0/CONTRIBUTING.md>`_
at the repository root for the full contribution guide, including branching model,
PR workflow, and commit conventions.

Environment setup
-----------------

.. code-block:: bash

   uv sync --group dev

Core validation commands
------------------------

.. code-block:: bash

   uv run --group dev ruff check src/ tests/
   uv run --group dev python -m pytest -q
   uv run --group dev sphinx-build -W -b html docs docs/_build/html
   uv build

Golden snapshots
----------------

Golden renderer fixtures live in ``tests/fixtures/golden/ascii/``.

To intentionally update them after renderer changes:

.. code-block:: bash

   uv run --group dev python -m pytest tests/test_golden_output.py -q --update-golden

Documentation screenshots
-------------------------

The chart gallery screenshots are generated from the library itself:

.. code-block:: bash

   uv run --group dev python scripts/generate_doc_screenshots.py

Testing guidelines
------------------

When changing rendering behavior, update tests before changing documentation so
the documented contract stays anchored to executable behavior.

The project enforces 85% code coverage via pytest-cov. The test suite includes:

- terminal color contract behavior
- matrix validation behavior
- standalone renderer parity
- curated edge-case regression coverage
