# Contributing to textcharts

## Branching model

- **`main`** is the release branch. It contains only release commits (one squash-merge per release). Do not commit directly to main.
- All development happens on **pre-release branches** named `dev-X.Y.Z` (e.g. `dev-0.1.1`, `dev-0.2.0`).
- When a release is ready, the dev branch is squash-merged to main and tagged.

```
main:       ● ─────────── R1 (squash) ── v0.1.0 ─────────── R2 (squash) ── v0.1.1
             \           /                \                  /
dev-0.1.0:    A ── B ──┘        dev-0.1.1: C ── D ── E ──┘
```

## Making changes

1. Find the current active `dev-*` branch.
2. Create a feature branch from it:
   ```bash
   git switch dev-0.1.1
   git switch -c feat/my-change
   ```
3. Make your changes, commit with [conventional commit](https://www.conventionalcommits.org/) messages:
   ```
   feat: add sparkline color options
   fix: handle empty data in bar chart
   docs: add box plot tutorial
   ```
4. Open a PR targeting the active `dev-*` branch (not `main`).

## Development setup

```bash
git clone https://github.com/joeharris76/textcharts.git
cd textcharts
uv sync --group dev
```

## Validation

Run all checks before submitting a PR:

```bash
uv run --group dev ruff check src/ tests/          # lint
uv run --group dev python -m pytest -q              # test (85% coverage required)
uv run --group dev sphinx-build -W -b html docs docs/_build/html  # docs
uv build                                            # package build
```

## Golden snapshots

Golden renderer fixtures live in `tests/fixtures/golden/ascii/`. To update them after intentional renderer changes:

```bash
uv run --group dev python -m pytest tests/test_golden_output.py -q --update-golden
```

## Documentation screenshots

The chart gallery screenshots are generated from the library itself:

```bash
uv run --group dev python scripts/generate_doc_screenshots.py
```

## Changelog

Update `CHANGELOG.md` when your change is user-facing. Add entries under the `[Unreleased]` section using [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

### Added
- Description of new feature

### Fixed
- Description of bug fix
```

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use for |
|--------|---------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation only |
| `test:` | Adding or updating tests |
| `refactor:` | Code changes that don't add features or fix bugs |
| `style:` | Formatting, import ordering |
| `chore:` | Maintenance tasks |
