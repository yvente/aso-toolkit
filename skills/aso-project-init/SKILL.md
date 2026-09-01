---
name: aso-project-init
description: Initialize and prepare the version-first ASO workspace for an iOS app. Use for first-time setup or to create a target-version/locale work directory; do not use to generate empty lifecycle artifacts.
---

# ASO Project Init

Initialize ASO state without changing app source code, migrating legacy files, or publishing metadata.

## Inputs

- App root: use the user-provided path, otherwise the current working directory.
- App name: infer it from first-party project configuration when reliable; otherwise ask.
- Locale: default to `en-US` for initialization.
- Target version and locale: require both when preparing a work directory.

Read [the shared system specification](references/aso-system-specification.md), especially project layout, artifact ownership, and legacy migration.

Resolve `scripts/aso_toolkit.py` relative to this `SKILL.md`. Initialize with:

```bash
python3 <skill-root>/scripts/aso_toolkit.py init-project --root <app-root> --app-name <app-name> --locale <locale>
```

When a target version is requested, then run:

```bash
python3 <skill-root>/scripts/aso_toolkit.py prepare-version --root <app-root> --target-version <version> --locale <locale>
```

Initialization creates only `aso/README.md`, `aso/STRUCTURE.md`, `aso/APP_BRIEF.md`, `aso/versions/`, and root `app-profile.json` when absent. Preparation creates only `aso/versions/<target-version>/<locale>/`. Do not create empty research, keywords, optimize, metadata, workbook, screenshots, learn, or experiment-log artifacts.

Both operations must be idempotent and preserve existing valid content. Report any detected 0.2.x paths with the manual migration guidance; never move or delete them automatically. Finish with created, preserved, and warned paths.
