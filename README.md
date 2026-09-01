# ASO Toolkit

ASO Toolkit is an agent plugin for Codex and ZCode containing five focused skills for repeatable App Store Optimization work: product research, keyword discovery, metadata experiments, and post-release learning.

It can consume keyword exports from ASOMinds, Astro, or similar tools. Those services provide measurement data; ASO Toolkit turns the data and the app's actual product context into a reviewable optimization loop.

## Skills

| Skill | Purpose | Primary output |
|---|---|---|
| `$aso-project-init` | Initialize and prepare a version/locale workspace | `aso/`, `app-profile.json` |
| `$aso-research` | Research competitors for one version and locale | `aso/versions/<version>/<locale>/research.md` |
| `$aso-keywords` | Generate a localized measurement backlog | `aso/versions/<version>/<locale>/keywords.md` |
| `$aso-optimize` | Propose validated metadata and derive a workbook | `proposed-<version>.json`, `deliverable.xlsx` |
| `$aso-learn` | Evaluate a released version from observed data | `learn.md`, `app-profile.json` |

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

Each step hands its output to the next:

- `$aso-project-init` creates the one shared `aso/APP_BRIEF.md`, `aso/versions/`, and `app-profile.json`, then prepares `aso/versions/<target-version>/<locale>/` on request.
- `$aso-research` writes competitor, review, screenshot, and positioning evidence to that version/locale directory.
- `$aso-keywords` consumes same-locale evidence and produces a measurement backlog there.
- `$aso-optimize` separates verified `live-<baseline-version>.json` from `proposed-<target-version>.json`, derives one locale-specific `deliverable.xlsx`, and records a proposed experiment.
- `$aso-learn` runs only after release and real observations, writes `learn.md`, and updates root learning state.

## Install

### Install the complete plugin (recommended)

Add this GitHub repository as a Codex marketplace, then install the plugin:

```bash
codex plugin marketplace add yvente/aso-toolkit
codex plugin add aso-toolkit@aso-toolkit
```

Start a new Codex task after installation. The plugin bundles all five skills and keeps them on the same version.

### Install with ZCode

In ZCode, open Settings → Plugin Management → Discover, press **+**, and add `yvente/aso-toolkit`. ZCode locates the marketplace through `.claude-plugin/marketplace.json` and resolves the plugin through the `.codex-plugin/plugin.json` manifest, so Codex and ZCode install from the same repository without extra configuration.

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

Codex and ZCode automatically discover repository-scoped skills under `.agents/skills`. Clone the repository, open the agent anywhere inside the checkout, and start a new task:

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

## First run (en-US example)

1. `$aso-project-init Initialize ASO for this iOS app and prepare version 1.1.0 in en-US.` — then fill in `aso/APP_BRIEF.md`.
2. `$aso-research Research benchmark competitors for version 1.1.0 in en-US.` — review `aso/versions/1.1.0/en-US/research.md`.
3. `$aso-keywords Generate the en-US keyword measurement backlog for version 1.1.0.` — review `keywords.md` in the same directory.
4. `$aso-optimize Propose and validate en-US metadata for version 1.1.0 from the verified 1.0.0 live baseline.` — review the proposed JSON and its derived `deliverable.xlsx`, then release through App Store Connect yourself.
5. After release and a real observation window, collect before/after metrics and run `$aso-learn Evaluate released version 1.1.0 in en-US.` The result lands beside the version artifacts and updates root learning state.

## Deterministic helper

[`scripts/aso_toolkit.py`](scripts/aso_toolkit.py) handles operations that should not depend on free-form model output:

```bash
python3 scripts/aso_toolkit.py --help
python3 scripts/aso_toolkit.py init-project --root /path/to/app --app-name "My App"
python3 scripts/aso_toolkit.py prepare-version --root /path/to/app --target-version 1.1.0 --locale en-US
python3 scripts/aso_toolkit.py validate-project --root /path/to/app --target-version 1.1.0 --locale en-US
python3 scripts/aso_toolkit.py validate-metadata --file proposed-1.1.0.json --role proposed --version 1.1.0 --locale en-US
python3 scripts/aso_toolkit.py compare-metrics --before before.csv --after after.csv
```

It validates metadata limits and JSON state, appends locale-specific experiment rounds atomically, compares metrics, and recomputes learning statistics idempotently.

## 0.3.0 workspace

ASO Toolkit 0.3.0 is version-first and locale-second:

```text
aso/
├── README.md
├── STRUCTURE.md
├── APP_BRIEF.md
└── versions/<target-version>/<locale>/
    ├── research.md
    ├── keywords.md
    ├── optimize.md
    ├── live-<baseline-version>.json
    ├── proposed-<target-version>.json
    ├── keyword-measurements-<date>.csv
    ├── deliverable.xlsx
    ├── screenshots/
    └── learn.md
```

Only `README.md`, `STRUCTURE.md`, `APP_BRIEF.md`, `versions/`, and root `app-profile.json` are initialized. Lifecycle artifacts appear only when produced. Root `experiment_log.json` and `app-profile.json` remain compatible state locations.

The helper detects 0.2.x root-level reports and `aso/metadata/` but never migrates them. Follow the manual role-aware migration in the canonical specification; back up first, classify each artifact by target version and locale, distinguish verified live metadata from proposals, regenerate each workbook from its proposed JSON, validate, and only then remove old copies yourself.

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
