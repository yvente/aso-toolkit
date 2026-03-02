# aso-toolkit

Claude Code skills and MCP server for App Store Optimization workflows.

Pairs with [ASOMinds](https://asominds.com/) for data-driven ASO automation.

## Structure

```
aso-toolkit/
├── skills/
│   ├── aso-optimize.md   # Claude Code slash command
│   └── aso-research.md   # Claude Code slash command
└── mcp/                  # MCP server (coming soon)
```

## Skills

### `/aso-research`

Discovers and segments competitors, analyzes their App Store presence, and produces an ASO growth strategy report — including screenshot visual analysis and immediate metadata recommendations.

Run this before `/aso-optimize` to identify the right competitors and build your initial keyword pack.

**Install:**

```bash
curl -fsSL https://raw.githubusercontent.com/yvente/aso-toolkit/main/skills/aso-research.md \
  -o ~/.claude/commands/aso-research.md
```

**Usage:**

```bash
# From a directory with APP_BRIEF.md or source code
/aso-research --code-path ./MyApp

# Target a specific locale
/aso-research --code-path ./MyApp --locale ja

# Without code path: Claude will ask you to describe your app
/aso-research

# Re-run analysis and overwrite existing ASO_RESEARCH.md
/aso-research --code-path ./MyApp --refresh
```

**Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `--code-path` | — | App source code path or directory containing APP_BRIEF.md |
| `--locale` | — | Target App Store locale (default: en-US) |
| `--refresh` | — | Force re-run the full workflow and overwrite existing `ASO_RESEARCH.md` |

**Workflow:**
1. If `ASO_RESEARCH.md` already exists and `--refresh` is not set, displays the existing report and stops
2. Builds app profile from `APP_BRIEF.md`, source code scan, or interactive description; writes `APP_BRIEF.md` if not already present (shared with `/aso-optimize`)
3. Discovers 10–15 competitor candidates via targeted web searches
4. Segments into **Benchmark Competitors** (3–5, for keyword gap analysis) and **Reference Competitors** (2–3 category leaders, for visual/CRO learning)
5. Analyzes Benchmark Competitors metadata and keyword signals; downloads and analyzes first 3 screenshots from Reference Competitors; extracts review pain points
6. Outputs strategy report with App Name candidates, 100-char keyword pack, and first 3 screenshots strategy; saves report to `ASO_RESEARCH.md`

---

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

# If APP_BRIEF.md was already created by /aso-research, skip --code-path
/aso-optimize --metadata ~/Downloads/metadata.csv

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
- [x] Claude Code Skill (`/aso-research`)
- [x] Install script (`curl`)
- [ ] MCP server — support Claude Desktop, Cursor, Windsurf and other MCP-compatible clients
- [ ] Standalone CLI — no Claude dependency required
