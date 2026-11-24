"""Validate the Astro desktop ranking CSV format."""

import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

HEADER = [
    "App Name", "App Id", "Platform", "Keyword", "Store Domain", "Store", "Note",
    "Last Update", "Ranking", "Change", "Popularity", "Difficulty", "Apps in Ranking", "Tags",
]


def validate(path: Path, app_id: str, storefront: str) -> int:
    if not re.fullmatch(r"[0-9]+", app_id) or not re.fullmatch(r"[A-Z]{2}", storefront):
        raise ValueError("Expected a numeric app ID and a two-letter uppercase storefront.")
    with path.open("rb") as source:
        data = source.read(1_048_577)
    if len(data) > 1_048_576:
        raise ValueError("The CSV exceeds the Storeward 1 MB limit.")
    rows = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
    if next(rows, None) != HEADER:
        raise ValueError("Expected header: " + ",".join(HEADER))

    seen = set()
    now = datetime.now(timezone.utc)
    for index, row in enumerate(rows, start=1):
        if index > 1000:
            raise ValueError("The CSV exceeds the Storeward 1,000-observation limit.")
        if len(row) != len(HEADER):
            raise ValueError(f"Observation {index} has the wrong column count.")
        _, row_id, platform, keyword, row_store, _, _, timestamp, rank, *_ = row
        if (row_id, row_store, platform) != (app_id, storefront.lower(), "iphone"):
            raise ValueError(f"Observation {index} does not match the App, storefront or device.")
        if not keyword.strip() or len(keyword) > 150 or keyword != keyword.strip():
            raise ValueError(f"Observation {index} has an invalid keyword.")
        if rank and not re.fullmatch(r"(?:[1-9][0-9]{0,2}|1000)", rank):
            raise ValueError(f"Observation {index} has an invalid rank.")
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [+-][0-9]{4}", timestamp):
            raise ValueError(f"Observation {index} needs an Astro desktop timestamp with a timezone.")
        try:
            observed_at = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S %z")
        except ValueError as error:
            raise ValueError(f"Observation {index} has an invalid timestamp.") from error
        if observed_at > now:
            raise ValueError(f"Observation {index} is dated in the future.")
        key = (unicodedata.normalize("NFC", keyword).lower(), observed_at)
        if key in seen:
            raise ValueError(f"Observation {index} duplicates a keyword and observation time.")
        seen.add(key)

    if not seen:
        raise ValueError("Expected at least one observation.")
    return len(seen)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--storefront", required=True)
    args = parser.parse_args()
    try:
        count = validate(args.csv, args.app_id, args.storefront)
    except (ValueError, OSError, csv.Error) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Validated {count} Astro observations for {args.app_id} / {args.storefront}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
