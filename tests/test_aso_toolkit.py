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


def metadata_document(role, version, locale="en-US", **overrides):
    value = {
        "schema_version": 1,
        "role": role,
        "locale": locale,
        "metadata": metadata(**overrides),
    }
    if role == "live":
        value["version"] = version
        value["captured_at"] = "2026-01-01"
        value["source"] = "https://apps.apple.com/app/id123"
    else:
        value["target_version"] = version
        value["baseline_version"] = "1.0.0"
        value["generated_at"] = "2026-01-02"
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

    def test_role_aware_live_and_proposed_metadata(self):
        live = metadata_document("live", "1.0.0")
        proposed = metadata_document("proposed", "1.1.0")
        self.assertEqual(
            aso.validate_metadata_document(live, expected_role="live", filename="live-1.0.0.json")["role"],
            "live",
        )
        self.assertEqual(
            aso.validate_metadata_document(
                proposed,
                expected_role="proposed",
                expected_version="1.1.0",
                filename="proposed-1.1.0.json",
            )["role"],
            "proposed",
        )

    def test_live_and_proposed_roles_cannot_be_confused(self):
        with self.assertRaises(aso.ValidationError):
            aso.validate_metadata_document(metadata_document("proposed", "1.1.0"), expected_role="live")
        with self.assertRaises(aso.ValidationError):
            aso.validate_metadata_document(metadata_document("live", "1.0.0"), expected_role="proposed")


class LayoutTests(unittest.TestCase):
    def init_args(self, root, locale="en-US"):
        return Namespace(root=str(root), app_name="Focus Timer", locale=locale)

    def prepare_args(self, root, version="1.1.0", locale="en-US"):
        return Namespace(root=str(root), target_version=version, locale=locale)

    def test_init_is_minimal_idempotent_and_preserves_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = aso.init_project(self.init_args(root))
            brief = root / "aso" / "APP_BRIEF.md"
            brief.write_text("# My Existing Brief\n", encoding="utf-8")
            second = aso.init_project(self.init_args(root))
            self.assertTrue(first["created"])
            self.assertFalse(second["created"])
            self.assertEqual(brief.read_text(encoding="utf-8"), "# My Existing Brief\n")
            self.assertTrue((root / "aso" / "versions").is_dir())
            files = {path.name for path in (root / "aso").rglob("*") if path.is_file()}
            self.assertEqual(files, {"README.md", "STRUCTURE.md", "APP_BRIEF.md"})
            self.assertFalse((root / "experiment_log.json").exists())

    def test_prepare_version_locales_and_idempotency(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            aso.init_project(self.init_args(root))
            for locale in ("en-US", "ja", "zh-Hant"):
                first = aso.prepare_version(self.prepare_args(root, locale=locale))
                second = aso.prepare_version(self.prepare_args(root, locale=locale))
                self.assertTrue(Path(first["path"]).is_dir())
                self.assertTrue(first["created"])
                self.assertFalse(second["created"])
                self.assertTrue(second["preserved"])

    def test_rejects_path_traversal_and_unsafe_segments(self):
        bad_versions = ("../1.1.0", "1/1", r"1\\1", "1..1", ".hidden", "1 1")
        bad_locales = ("../en-US", "en/US", r"en\\US", "zh..Hant", "en_US")
        for value in bad_versions:
            with self.subTest(version=value), self.assertRaises(aso.ValidationError):
                aso.validate_version(value)
        for value in bad_locales:
            with self.subTest(locale=value), self.assertRaises(aso.ValidationError):
                aso.validate_locale(value)
        self.assertEqual(aso.validate_version("2026.09-beta+1"), "2026.09-beta+1")

    def test_validate_new_layout_and_metadata_documents(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            aso.init_project(self.init_args(root))
            work = Path(aso.prepare_version(self.prepare_args(root))["path"])
            (work / "live-1.0.0.json").write_text(
                json.dumps(metadata_document("live", "1.0.0")), encoding="utf-8"
            )
            (work / "proposed-1.1.0.json").write_text(
                json.dumps(metadata_document("proposed", "1.1.0")), encoding="utf-8"
            )
            result = aso.validate_project(
                Namespace(root=str(root), target_version="1.1.0", locale="en-US")
            )
            self.assertTrue(result["valid"])
            self.assertEqual(len(result["metadata_documents"]), 2)

    def test_legacy_layout_is_reported_and_never_modified(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            aso_dir = root / "aso"
            aso_dir.mkdir()
            legacy = aso_dir / "ASO_RESEARCH_en-US.md"
            legacy.write_text("legacy research\n", encoding="utf-8")
            before = legacy.read_bytes()
            result = aso.init_project(self.init_args(root))
            self.assertIn(str(legacy.resolve()), result["legacy_paths"])
            self.assertIn("Manually move", result["warnings"][0])
            self.assertEqual(legacy.read_bytes(), before)


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
        self.assertEqual(manifest["version"], "0.3.0")


if __name__ == "__main__":
    unittest.main()
