"""
Ingest the Kaggle lyric CSV, clean metadata, and export JSON for analysis/web.
Uses only the standard library so it can run in minimal environments.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Dict, List

from feature_extraction import compute_features

# Canonical album metadata derived from README
ALBUM_META: Dict[str, Dict[str, str | int]] = {
    "Pablo Honey": {"year": 1993, "era": "Early"},
    "The Bends": {"year": 1995, "era": "Early"},
    "OK Computer": {"year": 1997, "era": "Peak"},
    "Kid A": {"year": 2000, "era": "Reinvention"},
    "Amnesiac": {"year": 2001, "era": "Reinvention"},
    "Hail to the Thief": {"year": 2003, "era": "Middle"},
    "In Rainbows": {"year": 2007, "era": "Late"},
    "The King of Limbs": {"year": 2011, "era": "Late"},
    "A Moon Shaped Pool": {"year": 2016, "era": "Late"},
}


def clean_text(value: str) -> str:
    """Normalize whitespace and strip non-breaking spaces."""
    normalized = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", normalized).strip()


def strip_by_radiohead(value: str) -> str:
    """Remove the trailing 'by Radiohead' tag."""
    cleaned = clean_text(value)
    return re.sub(r"\s*by\s+Radiohead$", "", cleaned, flags=re.IGNORECASE).strip()


def load_rows(csv_path: Path) -> List[dict]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def normalize_rows(rows: List[dict]) -> List[dict]:
    normalized = []
    for row in rows:
        album_raw = row.get("Album Name", "")
        track_raw = row.get("Track Name", "")
        lyrics_raw = row.get("Lyrics", "")

        album_name = strip_by_radiohead(album_raw)
        track_name = strip_by_radiohead(track_raw)
        lyrics = clean_text(lyrics_raw)

        if album_name not in ALBUM_META:
            raise ValueError(f"Unknown album: {album_name!r}")

        char_count = int(row.get("No_of_Characters", 0) or 0)
        word_count = int(row.get("No_of_Words", 0) or 0)

        features = compute_features(lyrics)

        normalized.append(
            {
                "track_name": track_name,
                "album_name": album_name,
                "album_year": ALBUM_META[album_name]["year"],
                "era": ALBUM_META[album_name]["era"],
                "lyrics": lyrics,
                "char_count": char_count,
                "word_count": word_count,
                **features,
                "source": "new_data_1.csv",
            }
        )
    return normalized


def write_json(records: List[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    raw_csv = repo_root / "data" / "raw" / "new_data_1.csv"
    export_json = repo_root / "data" / "exports" / "radiohead_complete.json"
    web_json = repo_root / "web" / "src" / "data" / "radiohead_complete.json"

    rows = load_rows(raw_csv)
    records = normalize_rows(rows)

    write_json(records, export_json)
    write_json(records, web_json)
    print(f"Wrote {len(records)} records to {export_json} and {web_json}")


if __name__ == "__main__":
    main()
