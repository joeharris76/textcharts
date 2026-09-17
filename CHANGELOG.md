# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.1.5] - 2026-09-17

### Fixed

- **Non-finite float sanitization:** Filter NaN/Inf before bounds, statistics,
  and grid math across heatmap, line chart, scatter plot, box plot, sparkline
  table, histogram, percentile ladder, rank table, and stacked bar. Invalid
  cells render `-`, unplottable points are skipped, and all-invalid inputs
  return "No data to display". Fixes a rank-table infinite loop on NaN tie
  comparison and a `statistics.stdev` crash on NaN in box plots.
- **Strict ASCII fallback:** `use_unicode=False` output is now strictly ASCII
  across all 15 chart types — box-drawing characters resolve through
  `get_box_chars()`, truncation markers fall back to `>`, and axis-label
  arrows honor terminal Unicode detection.
- **Dark theme palette:** Multi-series charts (BoxPlot, Histogram, CDFChart,
  StackedBar, ComparisonBar, ScatterPlot, LineChart) now render
  `DARK_PALETTE` when `theme="dark"` instead of the hardcoded light palette.
- **Diverging bar direction:** `lower_is_better=False` renders Worse | Better
  headers with mirrored sort order, and `from_data` accepts the flag.

### Added

- `outlier_cap` plumbed through the shared executor, command registry, CLI
  (`--outlier-cap`), and MCP server tools.
- `lower_is_better` chart parameter on the diverging command; registry
  histogram `max_per_chart` default synchronized to 25.
- `outlier_severity_markers(..., use_unicode=False)` ASCII fallback.

## [0.1.4] - 2026-09-16

### Fixed

- **Histogram bar width consistency:** Track maximum chunk length across multi-chart series (`_series_max_chunk_len`) to ensure uniform bar spacing across all chunks and prevent oversized bars in trailing chunks.
- **Histogram query label sorting:** Natural sort key now accounts for letter suffixes (`Q14a` before `Q14b`).
- **Histogram compact label collision:** Retain variant suffixes when compacting narrow query labels to avoid collapsing distinct queries to duplicate labels.
- **Histogram default bar count:** Adjust `DEFAULT_MAX_BARS` from 33 to 25 to ensure 3-character bar widths on standard 130-character terminal widths.
- **CI test coverage gate:** Install all optional integration extras (`--all-extras`) during CI test matrix runs to ensure coverage gates pass.

### Added

- Behavioral tests verifying non-collapsing variant query labels and prefix retention under terminal width constraints.
## [0.1.3] - 2026-03-28

### Added

- Textual widget integration — `TextChart` base widget plus typed chart
  widgets, compound widgets, and factory functions for building TUI dashboards
- Base chart class (`BaseChart`) extracted for shared rendering logic
- Wrap long x-axis labels onto 2 lines instead of truncating

### Fixed

- Preserve explicit chart settings when merging with defaults
- Improve wrapped x-axis label rendering alignment

## [0.1.2] - 2026-03-10

### Changed

- **Breaking:** Generalize BenchBox-specific field names to generic terms
  across all chart types (`query_id` → `label`, `latency_ms` → `value`,
  `platforms` → `rows`/`groups`, etc.)
- Add configurable rendered labels to `SummaryStats`

## [0.1.1] - 2026-03-10

### Added

- CLI guide and MCP/input-formats documentation
- Greyscale box plot output in README quick start

### Fixed

- Resolve all ruff lint errors; add lint gate to release script

## [0.1.0] - 2026-03-10

### Added

- 15 chart types: bar, histogram, heatmap, box plot, line, scatter,
  comparison bar, diverging bar, summary box, percentile ladder,
  normalized speedup, stacked bar, sparkline table, CDF, rank table
- Zero-dependency core library (Python 3.10+)
- CLI interface (`textcharts` command)
- MCP server (`textcharts-mcp` command)
- Sphinx documentation with Furo theme

[Unreleased]: https://github.com/joeharris76/textcharts/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/joeharris76/textcharts/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/joeharris76/textcharts/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/joeharris76/textcharts/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/joeharris76/textcharts/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/joeharris76/textcharts/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/joeharris76/textcharts/releases/tag/v0.1.0
