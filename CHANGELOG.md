# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]


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

[Unreleased]: https://github.com/joeharris76/textcharts/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/joeharris76/textcharts/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/joeharris76/textcharts/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/joeharris76/textcharts/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/joeharris76/textcharts/releases/tag/v0.1.0
