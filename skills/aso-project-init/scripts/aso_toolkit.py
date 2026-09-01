#!/usr/bin/env python3
"""Deterministic helpers for the ASO Toolkit skills.

The agent owns research and judgment. This module owns repeatable validation,
diffing, and cumulative JSON updates.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


FIELD_LIMITS = {
    "app_name": 30,
    "subtitle": 30,
    "keywords": 100,
    "promotional_text": 170,
    "description": 4000,
    "whats_new": 4000,
}
TEXT_FIELDS = tuple(field for field in FIELD_LIMITS if field != "keywords")
INTENT_TYPES = ("problem_intent", "feature", "broad", "long_tail")


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"expected a JSON object in {path}")
    return value


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def normalize_keywords(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise ValidationError("keywords must be an array of strings")
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str):
            raise ValidationError("keywords must contain only strings")
        word = item.strip()
        if not word:
            raise ValidationError("keywords must not contain empty values")
        if "," in word:
            raise ValidationError(f"keyword must not contain a comma: {word!r}")
        key = word.casefold()
        if key not in seen:
            seen.add(key)
            normalized.append(word)
    return normalized


def validate_metadata(metadata: dict[str, Any]) -> dict[str, int]:
    missing = [field for field in FIELD_LIMITS if field not in metadata]
    if missing:
        raise ValidationError(f"missing metadata fields: {', '.join(missing)}")

    counts: dict[str, int] = {}
    for field in TEXT_FIELDS:
        value = metadata[field]
        if not isinstance(value, str):
            raise ValidationError(f"{field} must be a string")
        counts[field] = len(value)

    keywords = normalize_keywords(metadata["keywords"])
    counts["keywords"] = len(",".join(keywords))

    exceeded = [
        f"{field}={counts[field]}/{limit}"
        for field, limit in FIELD_LIMITS.items()
        if counts[field] > limit
    ]
    if exceeded:
        raise ValidationError("metadata limits exceeded: " + ", ".join(exceeded))
    return counts


def validate_experiment_log(log: dict[str, Any]) -> None:
    entries = log.get("entries")
    if not isinstance(entries, list):
        raise ValidationError("experiment_log.json must contain entries[]")
    identities: set[tuple[int, str]] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValidationError(f"entries[{index}] must be an object")
        round_number = entry.get("round")
        locale = entry.get("locale")
        if not isinstance(round_number, int) or round_number < 1:
            raise ValidationError(f"entries[{index}].round must be a positive integer")
        if not isinstance(locale, str) or not locale:
            raise ValidationError(f"entries[{index}].locale must be a string")
        identity = (round_number, locale)
        if identity in identities:
            raise ValidationError(f"duplicate experiment identity: round {round_number}/{locale}")
        identities.add(identity)
        for snapshot in ("metadata_before", "metadata_after"):
            value = entry.get(snapshot)
            if not isinstance(value, dict):
                raise ValidationError(f"entries[{index}].{snapshot} must be an object")
            validate_metadata(value)
        if not isinstance(entry.get("changes"), dict):
            raise ValidationError(f"entries[{index}].changes must be an object")


def metadata_changes(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    changes: dict[str, Any] = {}
    for field in TEXT_FIELDS:
        changes[field] = {"changed": before[field] != after[field]}
    before_keywords = normalize_keywords(before["keywords"])
    after_keywords = normalize_keywords(after["keywords"])
    before_map = {value.casefold(): value for value in before_keywords}
    after_map = {value.casefold(): value for value in after_keywords}
    added = [after_map[key] for key in after_map.keys() - before_map.keys()]
    removed = [before_map[key] for key in before_map.keys() - after_map.keys()]
    changes["keywords"] = {
        "changed": bool(added or removed),
        "added": sorted(added, key=str.casefold),
        "removed": sorted(removed, key=str.casefold),
    }
    return changes


def default_profile(app_name: str = "", locale: str = "en-US") -> dict[str, Any]:
    return {
        "schema_version": 1,
        "app_name": app_name,
        "locale": locale,
        "experiment_history": [],
        "keyword_type_stats": {
            intent: {
                "success_rate": None,
                "avg_outcome_score": None,
                "outcome_scores_list": [],
                "count": 0,
            }
            for intent in INTENT_TYPES
        },
        "thresholds": {
            "min_popularity": 20,
            "max_difficulty": 70,
            "confidence": "low_confidence",
            "last_updated_by_experiment": None,
            "note": "Defaults until at least three evaluated experiments.",
        },
        "preferred_keyword_types": [],
    }


def init_project(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).resolve()
    aso_dir = root / "aso"
    metadata_dir = aso_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    files = {
        aso_dir / "APP_BRIEF.md": (
            f"# App Brief\n\n> Last updated: {date.today().isoformat()}\n\n"
            "## Core Features\n\n## Target Users\n\n## Key Differentiators\n\n"
            "## Recent Changes\n"
        ),
        aso_dir / "README.md": (
            f"# ASO Workflow for {args.app_name}\n\n"
            "Run `$aso-research`, `$aso-keywords`, `$aso-optimize`, then `$aso-learn`.\n"
        ),
        aso_dir / "STRUCTURE.md": (
            "# ASO Structure\n\n"
            "`APP_BRIEF.md` and `metadata/` are maintained inputs. ASO reports, "
            "`experiment_log.json`, and `app-profile.json` are generated state.\n"
        ),
    }
    created: list[str] = []
    preserved: list[str] = []
    for path, content in files.items():
        if path.exists():
            preserved.append(str(path))
        else:
            path.write_text(content, encoding="utf-8")
            created.append(str(path))

    profile_path = root / "app-profile.json"
    if profile_path.exists():
        preserved.append(str(profile_path))
    else:
        atomic_write_json(profile_path, default_profile(args.app_name, args.locale))
        created.append(str(profile_path))
    return {"created": created, "preserved": preserved}


def validate_project(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    brief = root / "aso" / "APP_BRIEF.md"
    if not brief.is_file():
        errors.append(f"missing {brief}")

    log_path = root / "experiment_log.json"
    latest_round = None
    if log_path.exists():
        try:
            log = load_json(log_path)
            validate_experiment_log(log)
            matching = [entry for entry in log["entries"] if entry["locale"] == args.locale]
            if matching:
                latest_round = max(entry["round"] for entry in matching)
            else:
                warnings.append(f"no experiment entry for locale {args.locale}")
        except ValidationError as exc:
            errors.append(str(exc))
    else:
        warnings.append(f"missing {log_path}; a confirmed baseline is required for optimization")

    profile_path = root / "app-profile.json"
    if profile_path.exists():
        try:
            load_json(profile_path)
        except ValidationError as exc:
            errors.append(str(exc))
    else:
        warnings.append(f"missing {profile_path}; default thresholds will be used")
    if errors:
        raise ValidationError("; ".join(errors))
    return {"valid": True, "locale": args.locale, "latest_round": latest_round, "warnings": warnings}


def append_experiment(args: argparse.Namespace) -> dict[str, Any]:
    log_path = Path(args.log).resolve()
    before = load_json(Path(args.before))
    after = load_json(Path(args.after))
    validate_metadata(before)
    validate_metadata(after)

    if log_path.exists():
        log = load_json(log_path)
        validate_experiment_log(log)
    else:
        if not args.app_name:
            raise ValidationError("--app-name is required when creating an experiment log")
        log = {
            "schema_version": 1,
            "app_id": args.app_id or "",
            "app_name": args.app_name,
            "exported_at": "",
            "before_version": args.before_version or "",
            "after_version": args.after_version or args.before_version or "",
            "entries": [],
        }

    rounds = [entry["round"] for entry in log["entries"] if entry["locale"] == args.locale]
    next_round = max(rounds, default=0) + 1
    entry = {
        "round": next_round,
        "date": args.date or date.today().isoformat(),
        "locale": args.locale,
        "status": "proposed",
        "metadata_before": before,
        "metadata_after": after,
        "changes": metadata_changes(before, after),
    }
    log["entries"].append(entry)
    log["exported_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if args.before_version:
        log["before_version"] = args.before_version
    if args.after_version:
        log["after_version"] = args.after_version
    validate_experiment_log(log)
    atomic_write_json(log_path, log)
    return {"path": str(log_path), "round": next_round, "locale": args.locale, "changes": entry["changes"]}


def read_metric_csv(path: Path) -> dict[str, float]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"metric", "value"}.issubset(reader.fieldnames):
            raise ValidationError(f"{path} must contain metric,value columns")
        values: dict[str, float] = {}
        for row_number, row in enumerate(reader, start=2):
            metric = (row.get("metric") or "").strip()
            raw_value = (row.get("value") or "").strip()
            if not metric or not raw_value:
                continue
            if metric in values:
                raise ValidationError(f"duplicate metric {metric!r} in {path}:{row_number}")
            try:
                values[metric] = float(raw_value)
            except ValueError as exc:
                raise ValidationError(f"non-numeric value for {metric!r} in {path}:{row_number}") from exc
    return values


def compare_metrics(args: argparse.Namespace) -> dict[str, Any]:
    before = read_metric_csv(Path(args.before))
    after = read_metric_csv(Path(args.after))
    shared = sorted(before.keys() & after.keys())
    if not shared:
        raise ValidationError("before/after CSVs contain no shared metrics")
    rows = []
    for metric in shared:
        old = before[metric]
        new = after[metric]
        absolute = new - old
        percent = None if old == 0 else absolute / old * 100
        rows.append({"metric": metric, "before": old, "after": new, "absolute_delta": absolute, "percent_delta": percent})
    return {"metrics": rows, "only_before": sorted(before.keys() - after.keys()), "only_after": sorted(after.keys() - before.keys())}


def update_profile(args: argparse.Namespace) -> dict[str, Any]:
    profile_path = Path(args.profile).resolve()
    record = load_json(Path(args.record))
    for key in ("round", "locale"):
        if key not in record:
            raise ValidationError(f"learning record missing {key}")
    profile = load_json(profile_path) if profile_path.exists() else default_profile()
    history = profile.setdefault("experiment_history", [])
    if not isinstance(history, list):
        raise ValidationError("experiment_history must be an array")
    identity = (record["round"], record["locale"])
    history[:] = [item for item in history if (item.get("round"), item.get("locale")) != identity]
    history.append(record)
    history.sort(key=lambda item: (item.get("date", ""), item.get("locale", ""), item.get("round", 0)))

    stats: dict[str, dict[str, Any]] = {}
    for intent in INTENT_TYPES:
        scores: list[float] = []
        for experiment in history:
            for outcome in experiment.get("keyword_outcomes", []):
                if outcome.get("intent_type") == intent and isinstance(outcome.get("outcome_score"), (int, float)):
                    scores.append(float(outcome["outcome_score"]))
        stats[intent] = {
            "success_rate": None if not scores else sum(score >= 0.5 for score in scores) / len(scores),
            "avg_outcome_score": None if not scores else sum(scores) / len(scores),
            "outcome_scores_list": scores,
            "count": len(scores),
        }
    profile["keyword_type_stats"] = stats
    count = len(history)
    thresholds = profile.setdefault("thresholds", {})
    thresholds.setdefault("min_popularity", 20)
    thresholds.setdefault("max_difficulty", 70)
    thresholds["confidence"] = "high_confidence" if count >= 6 else "medium_confidence" if count >= 3 else "low_confidence"
    thresholds["last_updated_by_experiment"] = {"round": record["round"], "locale": record["locale"]}
    if count < 3:
        thresholds["min_popularity"] = 20
        thresholds["max_difficulty"] = 70
        thresholds["note"] = "Defaults until at least three evaluated experiments."
    ranked = sorted(
        ((intent, values["avg_outcome_score"]) for intent, values in stats.items() if values["avg_outcome_score"] is not None and values["avg_outcome_score"] >= 0.35),
        key=lambda pair: pair[1],
        reverse=True,
    )
    profile["preferred_keyword_types"] = [intent for intent, _ in ranked[:3]]
    atomic_write_json(profile_path, profile)
    return {"path": str(profile_path), "experiments": count, "confidence": thresholds["confidence"], "preferred_keyword_types": profile["preferred_keyword_types"]}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-project")
    init.add_argument("--root", required=True)
    init.add_argument("--app-name", required=True)
    init.add_argument("--locale", default="en-US")
    init.set_defaults(handler=init_project)

    project = subparsers.add_parser("validate-project")
    project.add_argument("--root", required=True)
    project.add_argument("--locale", default="en-US")
    project.set_defaults(handler=validate_project)

    metadata = subparsers.add_parser("validate-metadata")
    metadata.add_argument("--file", required=True)
    metadata.set_defaults(handler=lambda args: {"valid": True, "counts": validate_metadata(load_json(Path(args.file)))})

    append = subparsers.add_parser("append-experiment")
    append.add_argument("--log", required=True)
    append.add_argument("--before", required=True)
    append.add_argument("--after", required=True)
    append.add_argument("--locale", default="en-US")
    append.add_argument("--date")
    append.add_argument("--app-id")
    append.add_argument("--app-name")
    append.add_argument("--before-version")
    append.add_argument("--after-version")
    append.set_defaults(handler=append_experiment)

    metrics = subparsers.add_parser("compare-metrics")
    metrics.add_argument("--before", required=True)
    metrics.add_argument("--after", required=True)
    metrics.set_defaults(handler=compare_metrics)

    profile = subparsers.add_parser("update-profile")
    profile.add_argument("--profile", required=True)
    profile.add_argument("--record", required=True)
    profile.set_defaults(handler=update_profile)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = args.handler(args)
    except ValidationError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
