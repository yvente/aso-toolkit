---
name: aso-project-init
description: Initialize the standard files and directories for a reusable App Store Optimization experiment workflow. Use for first-time ASO setup in an iOS app repository; do not use merely to research competitors or rewrite metadata.
---

# ASO Project Init

Initialize ASO state without changing app source code or publishing metadata.

## Inputs

- App root: use the user-provided path, otherwise the current working directory.
- Locale: default to `en-US`.
- App name: infer it from the Xcode project or product configuration when reliable; otherwise ask.

Before writing, read [the shared system specification](references/aso-system-specification.md), especially “Project layout” and “State ownership.”

Resolve the bundled helper at `scripts/aso_toolkit.py` relative to this `SKILL.md`, then run:

```bash
python3 <skill-root>/scripts/aso_toolkit.py init-project --root <app-root> --app-name <app-name> --locale <locale>
```

## Create

The helper creates the following when absent:

```text
aso/
├── README.md
├── STRUCTURE.md
├── APP_BRIEF.md
└── metadata/
app-profile.json
```

- `APP_BRIEF.md` contains `Core Features`, `Target Users`, `Key Differentiators`, and `Recent Changes`.
- `app-profile.json` starts with empty history, default thresholds (`min_popularity: 20`, `max_difficulty: 70`), and all four keyword intent types.
- `aso/README.md` describes the sequence `$aso-research` → `$aso-keywords` → `$aso-optimize` → `$aso-learn`.
- `aso/STRUCTURE.md` documents which files are user-maintained and which are generated.

Do not create an empty `experiment_log.json`. `$aso-optimize` creates it only when baseline metadata is available.

## Safety

- Preserve existing files. If a target exists, inspect it and only add missing compatible structure.
- Ask before replacing a conflicting schema or template.
- Never modify application source, App Store Connect, or external services.

Finish with the created and preserved paths plus the next recommended command.
