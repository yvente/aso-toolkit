# Contributing to aso-toolkit

Thanks for your interest in contributing!

## Prerequisites

- Codex CLI or the Codex desktop app
- Python 3.10+
- Basic familiarity with App Store Optimization concepts

## How to Contribute

### Reporting Issues

Open a GitHub issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Make your changes
4. Commit with a clear message (`git commit -m 'feat: add X'`)
5. Push and open a Pull Request

### Improving Skills

The `skills/` directory contains the canonical, self-contained Codex skill packages. `.agents/skills/` contains repository-discovery links to those packages. To improve an existing skill or add a new one:

- Keep each `SKILL.md` focused and give it a discriminating description
- Put conditional detail in `references/` and deterministic behavior in tested scripts
- Keep every skill self-contained for `$skill-installer`
- Preserve the canonical schemas and state ownership in `references/aso-system-specification.md`, then synchronize the skill-local copies
- Run the unit, skill, and plugin validators described in `README.md`

### Plugin and integrations

The plugin manifest lives at `.codex-plugin/plugin.json`. The repository marketplace has two manifests: `.agents/plugins/marketplace.json` (the Codex-standard location, with a git-URL source) and `.claude-plugin/marketplace.json` (the Claude Code / ZCode-compatible location, with a relative source). Keep both in sync when adding or renaming plugins. Provider-specific APIs or MCP integrations should remain optional so the five skills continue to work with user-supplied exports.

## Code Style

- Markdown: use ATX headings (`#`), fenced code blocks
- Commit messages: follow [Conventional Commits](https://www.conventionalcommits.org/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
