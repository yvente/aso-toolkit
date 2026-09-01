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


if __name__ == "__main__":
    unittest.main()
