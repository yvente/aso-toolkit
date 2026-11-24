import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASTRO = ROOT / "skills" / "astro-aso-data"
SPEC = importlib.util.spec_from_file_location(
    "validate_rank_snapshot", ASTRO / "scripts" / "validate_rank_snapshot.py"
)
snapshot = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(snapshot)

HEADER = ",".join(snapshot.HEADER) + "\n"
OBSERVATION = '1234567890,US,iphone,"video compressor, offline",1000,2024-11-06T09:00:00Z\n'


class AstroRankingSnapshotTests(unittest.TestCase):
    def validate(self, observations):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snapshot.csv"
            path.write_text(HEADER + observations, encoding="utf-8")
            return snapshot.validate(path, "1234567890", "US")

    def test_stock_export_can_include_ranked_outside_chart_and_unknown_observations(self):
        self.assertEqual(self.validate(
            OBSERVATION
            + OBSERVATION.replace(",1000,", ",22,").replace("11-06", "11-23")
            + OBSERVATION.replace(",1000,", ",,").replace("11-06", "11-24")
        ), 3)

    def test_invalid_export_is_rejected(self):
        invalid = {
            "mixed storefront": OBSERVATION.replace(",US,", ",DE,"),
            "missing technical data": OBSERVATION.replace("T09:00:00Z", ""),
            "footer comment": OBSERVATION + "# no baseline, no report\n",
            "duplicate instant": OBSERVATION + OBSERVATION.replace("09:00:00Z", "10:00:00+01:00"),
            "invalid rank": OBSERVATION.replace(",1000,", ",1001,"),
        }
        for name, value in invalid.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.validate(value)

    def test_packaged_contracts_match_canonical_source(self):
        filename = "astro-ranking-snapshot.md"
        contract = (ROOT / "references" / filename).read_bytes()
        for skill in (ASTRO, ROOT / "skills" / "aso-learn"):
            self.assertEqual((skill / "references" / filename).read_bytes(), contract)
        self.assertEqual((ROOT / ".agents" / "skills" / ASTRO.name).resolve(), ASTRO)
