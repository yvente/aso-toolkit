# ASO Toolkit

ASO Toolkit is a Codex plugin containing five focused skills for repeatable App Store Optimization work: product research, keyword discovery, metadata experiments, and post-release learning.

It can consume keyword exports from ASOMinds, Astro, or similar tools. Those services provide measurement data; ASO Toolkit turns the data and the app's actual product context into a reviewable optimization loop.

## Skills

| Skill | Purpose | Primary output |
|---|---|---|
| `$aso-project-init` | Initialize a standard ASO workspace | `aso/`, `app-profile.json` |
| `$aso-research` | Build the product profile and research competitors | `aso/ASO_RESEARCH_<locale>.md` |
| `$aso-keywords` | Generate a 40–60 term measurement backlog | `aso/ASO_KEYWORDS_<locale>.md` |
| `$aso-optimize` | Propose validated metadata and record an experiment | `aso/ASO_OPTIMIZE_<locale>.md`, `experiment_log.json` |
| `$aso-learn` | Compare before/after metrics and update evidence | `aso/ASO_LEARN_<locale>.md`, `app-profile.json` |

The shared contract for paths, schemas, state ownership, locales, and metadata is in [`references/aso-system-specification.md`](references/aso-system-specification.md).

## Workflow

```text
$aso-project-init
        ↓
$aso-research → $aso-keywords
        ↓             ↓ measured keyword CSVs
        └──────→ $aso-optimize
                       ↓ human review and App Store release
             collect comparable metrics
                       ↓
                  $aso-learn
                       ↓
                next experiment
```

The toolkit never publishes to App Store Connect by itself. It creates proposals and experiment state for human review.

## Local development

Codex discovers personal standalone skills under `$HOME/.agents/skills`. For a development checkout, symlink each skill folder you want to test:

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/aso-project-init" "$HOME/.agents/skills/aso-project-init"
ln -s "$PWD/skills/aso-research" "$HOME/.agents/skills/aso-research"
ln -s "$PWD/skills/aso-keywords" "$HOME/.agents/skills/aso-keywords"
ln -s "$PWD/skills/aso-optimize" "$HOME/.agents/skills/aso-optimize"
ln -s "$PWD/skills/aso-learn" "$HOME/.agents/skills/aso-learn"
```

Start a new Codex task after installation. The repository also contains a valid [Codex plugin manifest](.codex-plugin/plugin.json) for packaging all five skills together.

## Deterministic helper

[`scripts/aso_toolkit.py`](scripts/aso_toolkit.py) handles operations that should not depend on free-form model output:

```bash
python3 scripts/aso_toolkit.py --help
python3 scripts/aso_toolkit.py init-project --root /path/to/app --app-name "My App"
python3 scripts/aso_toolkit.py validate-project --root /path/to/app --locale en-US
python3 scripts/aso_toolkit.py validate-metadata --file proposed-metadata.json
python3 scripts/aso_toolkit.py compare-metrics --before before.csv --after after.csv
```

It validates metadata limits and JSON state, appends locale-specific experiment rounds atomically, compares metrics, and recomputes learning statistics idempotently.

## Validate the repository

```bash
python3 -m unittest discover -s tests -v

for skill in skills/aso-project-init skills/aso-research skills/aso-keywords skills/aso-optimize skills/aso-learn; do
  python3 /path/to/skill-creator/scripts/quick_validate.py "$skill"
done

python3 /path/to/plugin-creator/scripts/validate_plugin.py .
git diff --check
```

## Status

- [x] Five Codex Skills
- [x] Shared state/schema specification
- [x] Deterministic validation and experiment helpers
- [x] Plugin manifest
- [ ] Real-project behavioral evaluations
- [ ] Marketplace packaging and publication
- [ ] Optional ASO data-provider connector/MCP integration

## License

MIT
