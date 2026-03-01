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

Produces optimized App Store metadata from your app brief, current metadata, and keyword data.

**Install:**

```bash
curl -fsSL https://raw.githubusercontent.com/yvente/aso-toolkit/main/skills/aso-optimize.md \
  -o ~/.claude/commands/aso-optimize.md
```

**Usage:**

```bash
# First run: scans source code and generates APP_BRIEF.md
/aso-optimize --metadata ~/Downloads/metadata.csv --code-path ./MyApp

# Subsequent runs: reads APP_BRIEF.md directly (fast)
/aso-optimize --metadata ~/Downloads/metadata.csv

# With keyword data from a research tool (e.g. Astro)
/aso-optimize \
  --metadata ~/Downloads/metadata.csv \
  --keywords ~/Desktop/my-app-keywords.csv \
  --competitors ~/Desktop/comp1.csv ~/Desktop/comp2.csv \
  --locale en-US

# After a major feature update: re-scan source code
/aso-optimize --metadata ~/Downloads/metadata.csv --code-path ./MyApp --refresh-brief
```

**Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `--metadata` | ✅ | Path to current ASO metadata CSV |
| `--code-path` | — | App source code path (default: current dir) |
| `--keywords` | — | Own app keyword CSV from a research tool e.g. Astro |
| `--competitors` | — | Competitor keyword CSVs (supports multiple) |
| `--locale` | — | Target locale (default: en-US) |
| `--refresh-brief` | — | Force re-scan source code and regenerate APP_BRIEF.md |

**Workflow:**
1. Reads `APP_BRIEF.md` if present; otherwise scans source code and generates it
2. Loads current metadata CSV (supports ASOMinds export and custom formats)
3. Applies inlined Apple ASO rules + one targeted category keyword search
4. Analyzes keyword data: preserves top-10 rankings, filters by popularity/difficulty
5. Outputs optimized metadata with before/after comparison and keyword rationale

## MCP Server

Coming in Phase 2 — will expose the same workflow as an MCP tool, usable from any MCP-compatible client.

## Roadmap

- [x] Claude Code Skill (`/aso-optimize`)
- [x] Install script (`curl`)
- [ ] MCP server — support Claude Desktop, Cursor, Windsurf and other MCP-compatible clients
- [ ] Standalone CLI — no Claude dependency required
