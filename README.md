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

The canonical contract for paths, schemas, state ownership, locales, and metadata is in [`references/aso-system-specification.md`](references/aso-system-specification.md). Each installable skill carries the reference material and helper scripts it needs, so standalone installation does not depend on files outside the skill directory.

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

## Install

### Install the complete plugin (recommended)

Add this GitHub repository as a Codex marketplace, then install the plugin:

```bash
codex plugin marketplace add yvente/aso-toolkit
codex plugin add aso-toolkit@aso-toolkit
```

Start a new Codex task after installation. The plugin bundles all five skills and keeps them on the same version.

### Install standalone skills

In Codex, invoke `$skill-installer` and ask it to install the desired paths from `yvente/aso-toolkit`:

```text
$skill-installer Install these skills from yvente/aso-toolkit:
skills/aso-project-init
skills/aso-research
skills/aso-keywords
skills/aso-optimize
skills/aso-learn
```

Every directory is self-contained, so installing one skill does not require cloning the complete repository.

### Use directly from a checkout

Codex automatically discovers repository-scoped skills under `.agents/skills`. Clone the repository, open Codex anywhere inside the checkout, and start a new task:

```bash
git clone https://github.com/yvente/aso-toolkit.git
cd aso-toolkit
codex
```

No user-level symlinks are required.

## Use

Invoke a skill explicitly by typing `$` in Codex, or describe a matching ASO task and let Codex select it automatically:

```text
$aso-project-init Initialize ASO for this iOS app in en-US.
$aso-research Research benchmark competitors for this app in en-US.
$aso-keywords Generate a localized keyword measurement backlog.
$aso-optimize Propose and validate the next metadata experiment.
$aso-learn Evaluate round 1 from the supplied before/after CSV files.
```

Run the workflow in the target app repository. Generated ASO state belongs to that app, not to this toolkit checkout.

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
- [x] GitHub marketplace packaging
- [ ] Universal Plugins Directory publication
- [ ] Optional ASO data-provider connector/MCP integration

## License

MIT
