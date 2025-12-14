"""
The Wait: Analysis of song gestation times from live debut to studio release.

The most famous example is True Love Waits - 21 years from first live performance
in 1995 to its studio release on A Moon Shaped Pool in 2016, the same year
Rachel Owen passed away.

This module computes wait times and provides data for visualization.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def load_live_debuts(path: Path | None = None) -> Dict[str, Any]:
    """Load live debut data from JSON."""
    if path is None:
        path = Path(__file__).resolve().parents[2] / "data" / "raw" / "live_debuts.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_wait_time(first_live: str, studio_release: str) -> Dict[str, Any]:
    """
    Calculate the wait time between live debut and studio release.

    Returns:
        dict with years, months, days, and total_days
    """
    live_date = datetime.strptime(first_live, "%Y-%m-%d")
    release_date = datetime.strptime(studio_release, "%Y-%m-%d")

    delta = release_date - live_date
    total_days = delta.days

    # Could be negative if released before live debut
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_days": total_days,
        "total_years": round(total_days / 365.25, 2)
    }


def get_all_wait_times() -> List[Dict[str, Any]]:
    """
    Get wait times for all songs with live debut data.

    Returns:
        List of dicts with song info and wait times, sorted by wait time descending
    """
    data = load_live_debuts()
    songs = data.get("songs", {})

    results = []
    for song_name, song_data in songs.items():
        first_live = song_data.get("first_live")
        studio_release = song_data.get("studio_release")

        if first_live and studio_release:
            wait = calculate_wait_time(first_live, studio_release)

            results.append({
                "song": song_name,
                "first_live_date": first_live,
                "first_live_venue": song_data.get("first_live_venue", "Unknown"),
                "studio_release_date": studio_release,
                "studio_album": song_data.get("studio_album", "Unknown"),
                "wait_years": wait["total_years"],
                "wait_days": wait["total_days"],
                "notes": song_data.get("notes", "")
            })

    # Sort by wait time descending
    results.sort(key=lambda x: x["wait_days"], reverse=True)

    return results


def get_long_waiters(min_years: float = 5.0) -> List[Dict[str, Any]]:
    """Get songs that waited at least min_years for studio release."""
    all_waits = get_all_wait_times()
    return [s for s in all_waits if s["wait_years"] >= min_years]


def get_wait_stats() -> Dict[str, Any]:
    """Get summary statistics about song wait times."""
    all_waits = get_all_wait_times()

    # Filter to only positive wait times (released after live debut)
    positive_waits = [s for s in all_waits if s["wait_days"] > 0]

    if not positive_waits:
        return {}

    years = [s["wait_years"] for s in positive_waits]

    return {
        "total_songs": len(positive_waits),
        "mean_wait_years": round(sum(years) / len(years), 2),
        "median_wait_years": round(sorted(years)[len(years) // 2], 2),
        "max_wait_years": max(years),
        "min_wait_years": min(years),
        "longest_wait_song": positive_waits[0]["song"],
        "songs_over_10_years": len([y for y in years if y >= 10]),
        "songs_over_20_years": len([y for y in years if y >= 20])
    }


def true_love_waits_story() -> Dict[str, Any]:
    """
    Get the full True Love Waits story - the emotional centerpiece.

    21 years of waiting. First played in December 1995.
    Finally released on A Moon Shaped Pool in May 2016.
    That was the year Rachel Owen, Thom Yorke's partner of 23 years
    and mother of their two children, passed away.

    Twenty-one years of waiting to release a song called "True Love Waits,"
    and when they finally did, it was a goodbye.
    """
    data = load_live_debuts()
    tlw = data.get("songs", {}).get("True Love Waits", {})

    if not tlw:
        return {}

    wait = calculate_wait_time(tlw["first_live"], tlw["studio_release"])

    return {
        "song": "True Love Waits",
        "first_live_date": tlw["first_live"],
        "first_live_venue": tlw["first_live_venue"],
        "first_live_year": 1995,
        "studio_release_date": tlw["studio_release"],
        "studio_album": tlw["studio_album"],
        "studio_release_year": 2016,
        "wait_years": wait["total_years"],
        "wait_days": wait["total_days"],
        "context": (
            "First played live in December 1995 at the Clapham Grand in London. "
            "For 21 years, it existed only as a live track and bootleg recordings. "
            "Fans waited through OK Computer, Kid A, Amnesiac, Hail to the Thief, "
            "In Rainbows, and The King of Limbs. Each album came and went without it. "
            "Then in May 2016, A Moon Shaped Pool arrived. The album closer was "
            "True Love Waits - but transformed. The lush band arrangement was gone. "
            "Just Thom, alone at the piano. "
            "Rachel Owen, Thom's partner of 23 years and mother of their children, "
            "passed away in December 2016. "
            "Twenty-one years of waiting to release a song called 'True Love Waits,' "
            "and when they finally did, it was a goodbye."
        ),
        "live_versions": [
            {"year": 1995, "version": "Full band acoustic, emotional and raw"},
            {"year": 2001, "version": "I Might Be Wrong live album (Vauxhall version)"},
            {"year": 2003, "version": "Brief revival in setlists"},
            {"year": 2006, "version": "Solo Thom performances"},
            {"year": 2016, "version": "Solo piano, sparse and devastating"}
        ]
    }


def export_wait_data_for_web() -> Dict[str, Any]:
    """Export all wait time data formatted for web visualization."""
    return {
        "all_songs": get_all_wait_times(),
        "long_waiters": get_long_waiters(min_years=5.0),
        "stats": get_wait_stats(),
        "true_love_waits": true_love_waits_story()
    }


if __name__ == "__main__":
    import pprint

    print("=" * 60)
    print("THE WAIT: Song Gestation Times")
    print("=" * 60)

    print("\n--- Wait Time Statistics ---")
    pprint.pprint(get_wait_stats())

    print("\n--- Longest Waiters (5+ years) ---")
    for song in get_long_waiters(5.0):
        print(f"  {song['song']}: {song['wait_years']} years")

    print("\n--- True Love Waits Story ---")
    story = true_love_waits_story()
    print(f"  Wait time: {story['wait_years']} years")
    print(f"  {story['context']}")
