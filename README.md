# aso-toolkit

Claude Code skills and MCP server for App Store Optimization workflows.

Pairs with [ASOMinds](https://asominds.com/) for data-driven ASO automation.

## Structure

```
aso-toolkit/
├── skills/
│   └── aso-optimize.md   # Claude Code slash command
└── mcp/                  # MCP server (coming soon)
```

## Skills

### `/aso-optimize`

Analyzes your app's source code and keyword data to produce optimized App Store metadata.

**Install:**

```bash
ln -s /path/to/aso-toolkit/skills/aso-optimize.md ~/.claude/commands/aso-optimize.md
```

**Usage:**

```bash
/aso-optimize --metadata ~/Downloads/metadata.csv --code-path ./MyApp

# With keyword data from ASOMinds
/aso-optimize \
  --metadata ~/Downloads/metadata.csv \
  --code-path ./MyApp \
  --keywords ~/Desktop/my-app-keywords.csv \
  --competitors ~/Desktop/comp1.csv ~/Desktop/comp2.csv \
  --locale en-US
```

**Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `--metadata` | ✅ | Path to current ASO metadata CSV |
| `--code-path` | — | App source code path (default: current dir) |
| `--keywords` | — | Own app keyword CSV from ASOMinds |
| `--competitors` | — | Competitor keyword CSVs (supports multiple) |
| `--locale` | — | Target locale (default: en-US) |

**Workflow:**
1. Reads app source code to understand features and differentiators
2. Loads current metadata to establish baseline
3. Searches Apple docs + reputable ASO sources for best practices
4. Analyzes keyword data (popularity > 20, difficulty < 70)
5. Outputs optimized metadata with before/after comparison

## MCP Server

Coming in Phase 2 — will expose the same workflow as an MCP tool, usable from any MCP-compatible client.

## Roadmap

- [x] Claude Code Skill (`/aso-optimize`)
- [ ] Install script (`curl | sh`)
- [ ] MCP server — support Claude Desktop, Cursor, Windsurf and other MCP-compatible clients
- [ ] Standalone CLI — no Claude dependency required
