Rendering behavior
==================

Terminal capability detection
-----------------------------

The renderer adapts to:

- available width
- interactivity
- ANSI color capability
- likely Unicode support

Capability detection is handled by
:func:`textcharts.detect_terminal_capabilities`.

Rendering invariants
--------------------

The library intentionally preserves a few important output rules:

- default rendering must not emit ANSI escapes in non-interactive contexts
- ``NO_COLOR`` must disable color regardless of terminal capability
- ASCII fallbacks must remain usable when Unicode is disabled
- chart-specific validation should raise clear errors instead of silently
  dropping malformed input

Why this matters
----------------

Terminal chart libraries are often used in CI logs, shell pipelines, benchmark
reports, and generated artifacts. In those contexts, stable plain-text behavior
matters as much as the interactive terminal presentation.
