# Contributing to aso-toolkit

Thanks for your interest in contributing!

## Prerequisites

- [Claude Code](https://claude.ai/code) CLI installed
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

The `skills/` directory contains Claude Code slash command definitions in Markdown. To improve an existing skill or add a new one:

- Keep prompts clear and step-by-step
- Document all parameters with a table
- Test locally by symlinking to `~/.claude/commands/`

### MCP Server (Phase 2)

The `mcp/` directory is reserved for the upcoming MCP server implementation. Contributions here are especially welcome — see the roadmap in README for scope.

## Code Style

- Markdown: use ATX headings (`#`), fenced code blocks
- Commit messages: follow [Conventional Commits](https://www.conventionalcommits.org/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
