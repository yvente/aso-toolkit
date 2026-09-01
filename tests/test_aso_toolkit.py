import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "aso_toolkit.py"
SPEC = importlib.util.spec_from_file_location("aso_toolkit", MODULE_PATH)
aso = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(aso)


def metadata(**overrides):
    value = {
        "app_name": "Focus Timer",
        "subtitle": "Plan calm work sessions",
        "keywords": ["productivity", "pomodoro"],
        "promotional_text": "Make time for focused work.",
        "description": "Plan focused sessions and review your progress.",
        "whats_new": "Improved timer reliability.",
    }
    value.update(overrides)
    return value


class MetadataTests(unittest.TestCase):
    def test_valid_metadata_counts_rendered_keywords(self):
        counts = aso.validate_metadata(metadata())
        self.assertEqual(counts["keywords"], len("productivity,pomodoro"))

    def test_rejects_limit_violation(self):
        with self.assertRaises(aso.ValidationError):
            aso.validate_metadata(metadata(app_name="x" * 31))

    def test_keyword_diff_is_case_insensitive(self):
        before = metadata(keywords=["Focus", "timer"])
        after = metadata(keywords=["focus", "planner"])
        changes = aso.metadata_changes(before, after)
        self.assertEqual(changes["keywords"]["added"], ["planner"])
        self.assertEqual(changes["keywords"]["removed"], ["timer"])


class StateTests(unittest.TestCase):
    def test_append_experiment_increments_per_locale(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            before_path = root / "before.json"
            after_path = root / "after.json"
            log_path = root / "experiment_log.json"
            before_path.write_text(json.dumps(metadata()), encoding="utf-8")
            after_path.write_text(json.dumps(metadata(subtitle="Focus with less friction")), encoding="utf-8")
            base = dict(log=str(log_path), before=str(before_path), after=str(after_path), locale="en-US", date="2026-01-01", app_id="1", app_name="Focus", before_version="1.0", after_version="1.0")
            first = aso.append_experiment(Namespace(**base))
            second = aso.append_experiment(Namespace(**base))
            self.assertEqual(first["round"], 1)
            self.assertEqual(second["round"], 2)
            aso.validate_experiment_log(aso.load_json(log_path))

    def test_profile_update_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            profile_path = root / "app-profile.json"
            record_path = root / "record.json"
            record = {
                "round": 1,
                "locale": "en-US",
                "date": "2026-01-01",
                "keyword_outcomes": [{"keyword": "focus", "intent_type": "feature", "outcome_score": 0.8}],
            }
            record_path.write_text(json.dumps(record), encoding="utf-8")
            args = Namespace(profile=str(profile_path), record=str(record_path))
            aso.update_profile(args)
            aso.update_profile(args)
            profile = aso.load_json(profile_path)
            self.assertEqual(len(profile["experiment_history"]), 1)
            self.assertEqual(profile["keyword_type_stats"]["feature"]["count"], 1)


class PackagingTests(unittest.TestCase):
    def test_repo_scoped_skills_are_self_contained(self):
        root = Path(__file__).parents[1]
        skill_root = root / "skills"
        names = [
            "aso-project-init",
            "aso-research",
            "aso-keywords",
            "aso-optimize",
            "aso-learn",
        ]
        for name in names:
            directory = skill_root / name
            self.assertTrue((directory / "SKILL.md").is_file(), name)
            discovery_path = root / ".agents" / "skills" / name
            self.assertTrue(discovery_path.is_symlink(), name)
            self.assertEqual(discovery_path.resolve(), directory.resolve(), name)

        canonical_reference = (
            root / "references" / "aso-system-specification.md"
        ).read_bytes()
        for name in names:
            bundled_reference = (
                skill_root
                / name
                / "references"
                / "aso-system-specification.md"
            )
            self.assertEqual(bundled_reference.read_bytes(), canonical_reference, name)

        canonical_helper = (root / "scripts" / "aso_toolkit.py").read_bytes()
        for name in ["aso-project-init", "aso-optimize", "aso-learn"]:
            bundled_helper = skill_root / name / "scripts" / "aso_toolkit.py"
            self.assertEqual(bundled_helper.read_bytes(), canonical_helper, name)

    def test_marketplace_points_to_repository_plugin(self):
        root = Path(__file__).parents[1]
        marketplace = json.loads(
            (root / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(marketplace["name"], "aso-toolkit")
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "aso-toolkit")
        self.assertEqual(entry["source"]["source"], "url")
        self.assertEqual(
            entry["source"]["url"],
            "https://github.com/yvente/aso-toolkit.git",
        )

    def test_plugin_loads_canonical_skills(self):
        root = Path(__file__).parents[1]
        manifest = json.loads(
            (root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["skills"], "./skills/")


if __name__ == "__main__":
    unittest.main()
