Releasing
=========

This documents the release process for textcharts maintainers.

Branching model
---------------

- ``main`` is the release branch — it contains only squash-merge commits, one per
  release. Every commit on main corresponds to a tagged release.
- Development happens on long-lived ``dev-X.Y.Z`` branches.
- When a release is ready, the dev branch is squash-merged to main via PR and
  the resulting commit is tagged ``vX.Y.Z``.

Version locations
-----------------

Version is maintained in two files (must stay in sync):

1. ``pyproject.toml`` — ``version = "X.Y.Z"``
2. ``src/textcharts/__init__.py`` — ``__version__ = "X.Y.Z"``

CI validates that the tag matches both files on release.

Release script
--------------

The release process is automated by ``scripts/release.sh``:

.. code-block:: bash

   ./scripts/release.sh           # auto-increment patch (0.1.0 -> next 0.1.1)
   ./scripts/release.sh 0.2.0     # specify next version explicitly

The script performs all steps below with confirmation prompts at each stage.
It requires the ``gh`` CLI to be authenticated.

Release checklist (manual reference)
-------------------------------------

1. Ensure CI is green on the ``dev-X.Y.Z`` branch.

2. Finalize ``CHANGELOG.md``: rename ``[Unreleased]`` to ``[X.Y.Z] - YYYY-MM-DD``
   and add the release link at the bottom of the file.

3. Open a PR from ``dev-X.Y.Z`` to ``main`` with the title ``release: vX.Y.Z``.

4. Squash-merge the PR.

5. Tag the merge commit and push the tag:

   .. code-block:: bash

      git switch main && git pull
      git tag vX.Y.Z
      git push origin vX.Y.Z

6. CI automatically:

   - Runs the full test suite
   - Publishes to PyPI (via trusted publisher)
   - Creates a GitHub Release with auto-generated notes
   - Builds and deploys versioned Sphinx docs to GitHub Pages

7. Start the next development cycle:

   .. code-block:: bash

      git switch -c dev-X.Y.Z+1 main
      # Bump version in pyproject.toml and __init__.py
      # Add [Unreleased] section to CHANGELOG.md
      git push -u origin dev-X.Y.Z+1

What CI does on tag push
------------------------

Two workflows trigger on ``v*`` tags:

**ci.yml** — test, publish, release:

- Runs lint, tests (Python 3.10–3.13), docs build, and package build
- Validates version consistency (tag = pyproject.toml = __init__.py)
- Publishes to PyPI via ``pypa/gh-action-pypi-publish``
- Creates a GitHub Release with auto-generated notes

**docs.yml** — versioned documentation:

- Builds Sphinx docs
- Deploys to ``gh-pages`` branch under ``vX.Y.Z/`` directory
- Updates ``latest/`` to point to the new release
- Maintains ``versions.json`` for version discovery

Documentation URLs
------------------

After release, docs are available at:

- ``https://joeharris76.github.io/textcharts/latest/`` — always the most recent release
- ``https://joeharris76.github.io/textcharts/vX.Y.Z/`` — specific version

Versioning policy
-----------------

textcharts follows `SemVer <https://semver.org/>`_ during the ``0.x`` series:

- ``0.x.0`` — may include breaking API changes
- ``0.x.y`` — features and bug fixes, backwards compatible

Once the API stabilizes with downstream users, the project will promote to ``1.0.0``.
