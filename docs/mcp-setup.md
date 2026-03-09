# MCP Server Setup

textcharts includes a [Model Context Protocol](https://modelcontextprotocol.io)
server that exposes all 15 chart types as tools for AI assistants.

## Installation

```bash
pip install textcharts[mcp]
```

This installs the `mcp` dependency alongside textcharts. The server binary is
`textcharts-mcp`.

## Configuration

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "textcharts": {
      "command": "textcharts-mcp"
    }
  }
}
```

### Claude Code

Add to your project's `.mcp.json` or global MCP config:

```json
{
  "mcpServers": {
    "textcharts": {
      "command": "textcharts-mcp"
    }
  }
}
```

### Using uvx (no install)

If you prefer not to install textcharts globally, use `uvx` to run it directly:

```json
{
  "mcpServers": {
    "textcharts": {
      "command": "uvx",
      "args": ["--from", "textcharts[mcp]", "textcharts-mcp"]
    }
  }
}
```

## Available Tools

The server registers 17 tools:

| Tool                      | Description                                    |
|---------------------------|------------------------------------------------|
| `textcharts_bar`          | Horizontal bar chart                           |
| `textcharts_histogram`    | Vertical bar histogram                         |
| `textcharts_heatmap`      | Matrix heatmap                                 |
| `textcharts_boxplot`      | Box plot with quartiles                        |
| `textcharts_line`         | Line chart for trends                          |
| `textcharts_scatter`      | Scatter plot with Pareto frontier              |
| `textcharts_comparison`   | Side-by-side paired bar chart                  |
| `textcharts_diverging`    | Centered diverging bar chart                   |
| `textcharts_summary`      | Bordered summary statistics box                |
| `textcharts_percentile`   | Percentile band chart (P50/P90/P95/P99)        |
| `textcharts_speedup`      | Log-scale normalized speedup chart             |
| `textcharts_stacked`      | Stacked horizontal bar chart                   |
| `textcharts_sparkline`    | Compact table with sparkline mini-charts       |
| `textcharts_cdf`          | Cumulative distribution function chart         |
| `textcharts_rank`         | Competitive ranking table                      |
| `textcharts_list`         | List all available chart types                 |
| `textcharts_describe`     | Get detailed usage info for a chart type       |

## Usage

### Discovering chart types

Call `textcharts_list` to see all available charts, or `textcharts_describe`
with a chart type name for detailed field and parameter info:

```
Tool: textcharts_describe
Input: {"chart_type": "bar"}
```

### Rendering a chart

Each chart tool accepts a `data` parameter (plus optional `title` and common
options). The input format matches the JSON schemas in
[input-formats.md](input-formats.md).

**Example — bar chart:**

```
Tool: textcharts_bar
Input: {
  "data": [
    {"label": "Fiction", "value": 18.4},
    {"label": "Children", "value": 14.2},
    {"label": "Comics", "value": 9.8}
  ],
  "title": "Bookstore Revenue",
  "use_color": false
}
```

**Example — heatmap:**

```
Tool: textcharts_heatmap
Input: {
  "data": {
    "matrix": [[1.2, 3.4], [4.5, 1.8]],
    "row_labels": ["Row A", "Row B"],
    "col_labels": ["Col 1", "Col 2"]
  },
  "title": "Response Times"
}
```

### Chart-specific parameters

Some charts accept additional parameters beyond `data` and `title`. Pass them
via the `chart_params` key:

```
Tool: textcharts_bar
Input: {
  "data": [{"label": "A", "value": 10}, {"label": "B", "value": 20}],
  "chart_params": {"sort_by": "label", "metric_label": "Count"}
}
```

### Common options

All chart tools accept these top-level options:

| Option        | Type    | Default | Description                     |
|---------------|---------|---------|----------------------------------|
| `title`       | string  | —       | Chart title                      |
| `subtitle`    | string  | —       | Subtitle line below the title    |
| `width`       | integer | auto    | Chart width in characters        |
| `height`      | integer | auto    | Chart height in rows             |
| `use_color`   | boolean | true    | Enable ANSI color output         |
| `use_unicode` | boolean | true    | Enable Unicode box-drawing       |
| `theme`       | string  | light   | Color theme (light or dark)      |
| `show_legend` | boolean | true    | Show chart legend                |
| `show_values` | boolean | true    | Show numeric values on chart     |

## Transport

The server uses **stdio** transport. It reads JSON-RPC messages from stdin and
writes responses to stdout — no network ports needed.

## Troubleshooting

**"mcp package not found"** — Install the MCP extra: `pip install textcharts[mcp]`

**Server doesn't start** — Verify the binary is on your PATH:
```bash
which textcharts-mcp
textcharts-mcp  # should start and wait for stdin
```

**Tool returns "Error: ..."** — Check that your `data` matches the expected
format. Use `textcharts_describe` to see required fields for any chart type.
