"""
Export comprehensive analysis data for web visualization.

Generates a single JSON file with all the data needed for:
- Album Explorer
- Sentiment/Emotion Timeline
- Lyric Analyzer
- True Love Waits story
- 2025 Reunion Tour analysis
- Hypothesis test results
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).resolve().parents[1]
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from analysis.the_wait import export_wait_data_for_web
from analysis.setlist_archaeology import export_for_web as export_setlist
from analysis.lexical_diversity import export_for_web as export_lexical
from analysis.hypothesis_tests import generate_full_report


def load_track_data() -> list:
    path = Path(__file__).resolve().parents[2] / "data" / "exports" / "radiohead_complete.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_album_summary(tracks: list) -> list:
    albums = {}

    for track in tracks:
        album = track["album_name"]
        if album not in albums:
            albums[album] = {
                "album": album,
                "year": track["album_year"],
                "era": track["era"],
                "tracks": [],
                "metrics": {
                    "word_count": [],
                    "sentiment_score": [],
                    "type_token_ratio": [],
                    "coldness_index": [],
                    "warmth": [],
                    "emotion_sadness": [],
                    "emotion_joy": [],
                    "emotion_fear": [],
                    "emotional_intensity": []
                }
            }

        albums[album]["tracks"].append(track["track_name"])
        for metric in albums[album]["metrics"]:
            if metric in track:
                albums[album]["metrics"][metric].append(track[metric])

    # Calculate averages
    result = []
    for album_data in albums.values():
        summary = {
            "album": album_data["album"],
            "year": album_data["year"],
            "era": album_data["era"],
            "track_count": len(album_data["tracks"]),
            "tracks": album_data["tracks"]
        }

        for metric, values in album_data["metrics"].items():
            if values:
                summary[f"avg_{metric}"] = round(sum(values) / len(values), 4)
                summary[f"min_{metric}"] = round(min(values), 4)
                summary[f"max_{metric}"] = round(max(values), 4)

        result.append(summary)

    return sorted(result, key=lambda x: x["year"])


def get_standout_tracks(tracks: list) -> dict:
    if not tracks:
        return {}

    # Sort and get extremes
    by_sadness = sorted(tracks, key=lambda x: x.get("emotion_sadness", 0), reverse=True)
    by_joy = sorted(tracks, key=lambda x: x.get("emotion_joy", 0), reverse=True)
    by_coldness = sorted(tracks, key=lambda x: x.get("coldness_index", 0), reverse=True)
    by_warmth = sorted(tracks, key=lambda x: x.get("warmth", 0), reverse=True)
    by_intensity = sorted(tracks, key=lambda x: x.get("emotional_intensity", 0), reverse=True)

    return {
        "saddest": [{"track": t["track_name"], "album": t["album_name"], "score": t.get("emotion_sadness", 0)}
                    for t in by_sadness[:5]],
        "most_joyful": [{"track": t["track_name"], "album": t["album_name"], "score": t.get("emotion_joy", 0)}
                        for t in by_joy[:5]],
        "coldest": [{"track": t["track_name"], "album": t["album_name"], "score": t.get("coldness_index", 0)}
                    for t in by_coldness[:5]],
        "warmest": [{"track": t["track_name"], "album": t["album_name"], "score": t.get("warmth", 0)}
                    for t in by_warmth[:5]],
        "most_intense": [{"track": t["track_name"], "album": t["album_name"], "score": t.get("emotional_intensity", 0)}
                         for t in by_intensity[:5]]
    }


def export_all():
    print("Loading track data...")
    tracks = load_track_data()

    print("Building album summaries...")
    albums = build_album_summary(tracks)

    print("Getting standout tracks...")
    standouts = get_standout_tracks(tracks)

    print("Loading Wait analysis...")
    wait_data = export_wait_data_for_web()

    print("Loading setlist archaeology...")
    try:
        setlist_data = export_setlist()
    except (FileNotFoundError, KeyError, ValueError, ImportError) as e:
        print(f"  Warning: Could not load setlist data: {e}")
        setlist_data = None

    print("Loading lexical diversity...")
    try:
        lexical_data = export_lexical()
    except (FileNotFoundError, KeyError, ValueError, ImportError) as e:
        print(f"  Warning: Could not load lexical data: {e}")
        lexical_data = None

    print("Running hypothesis tests...")
    try:
        hypothesis_data = generate_full_report()
        # Clean up numpy types for JSON serialization
        hypothesis_data = json.loads(json.dumps(hypothesis_data, default=str))
    except (FileNotFoundError, KeyError, ValueError, ImportError) as e:
        print(f"  Warning: Could not run hypothesis tests: {e}")
        hypothesis_data = None

    # Build the complete export
    export = {
        "meta": {
            "total_tracks": len(tracks),
            "total_albums": len(albums),
            "years_span": f"{min(t['album_year'] for t in tracks)}-{max(t['album_year'] for t in tracks)}"
        },
        "tracks": tracks,
        "albums": albums,
        "standout_tracks": standouts,
        "the_wait": wait_data,
        "tour_2025": setlist_data,
        "lexical_evolution": lexical_data,
        "hypothesis_tests": hypothesis_data,
        "donwood_palettes": {
            "Pablo Honey": {
                "primary": "#f97316",
                "secondary": "#fbbf24",
                "background": "#1c1917",
                "text": "#fef3c7",
                "description": "Raw orange, baby imagery"
            },
            "The Bends": {
                "primary": "#e5e7eb",
                "secondary": "#9ca3af",
                "background": "#f8fafc",
                "text": "#1f2937",
                "description": "Clinical whites, medical imagery"
            },
            "OK Computer": {
                "primary": "#60a5fa",
                "secondary": "#93c5fd",
                "background": "#0f172a",
                "text": "#e2e8f0",
                "description": "Washed blues, highway grays"
            },
            "Kid A": {
                "primary": "#ef4444",
                "secondary": "#fecaca",
                "background": "#1c1917",
                "text": "#f5f5f4",
                "description": "Reds, mountain whites, digital decay"
            },
            "Amnesiac": {
                "primary": "#b45309",
                "secondary": "#f59e0b",
                "background": "#1c1917",
                "text": "#d6d3d1",
                "description": "Sepia, minotaur blacks"
            },
            "Hail to the Thief": {
                "primary": "#f59e0b",
                "secondary": "#fbbf24",
                "background": "#292524",
                "text": "#fef3c7",
                "description": "Map colors, dense text"
            },
            "In Rainbows": {
                "primary": "#fbbf24",
                "secondary": "#f472b6",
                "background": "#1f2937",
                "text": "#fef9c3",
                "description": "Spectrum explosion, layered"
            },
            "The King of Limbs": {
                "primary": "#10b981",
                "secondary": "#6ee7b7",
                "background": "#022c22",
                "text": "#d1fae5",
                "description": "Forest greens, newspaper"
            },
            "A Moon Shaped Pool": {
                "primary": "#9ca3af",
                "secondary": "#d1d5db",
                "background": "#1f2937",
                "text": "#e5e7eb",
                "description": "Muted, ash, water, grief"
            }
        }
    }

    # Write to web directory
    out_path = Path(__file__).resolve().parents[2] / "web" / "src" / "data" / "radiohead_web_data.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2, ensure_ascii=False)

    print(f"\nExported to {out_path}")
    print(f"  - {len(tracks)} tracks")
    print(f"  - {len(albums)} albums")
    print(f"  - Wait analysis: {'Yes' if wait_data else 'No'}")
    print(f"  - Tour 2025: {'Yes' if setlist_data else 'No'}")
    print(f"  - Lexical: {'Yes' if lexical_data else 'No'}")
    print(f"  - Hypothesis tests: {'Yes' if hypothesis_data else 'No'}")

    return export


if __name__ == "__main__":
    export_all()
