"""
Setlist.fm API client scaffolding for the 2025 tour analysis.

Requires a Setlist.fm API key set in SETLISTFM_API_KEY.
This is a thin helper to fetch and normalize setlists; real network calls
should be gated/approved before running.
"""

from __future__ import annotations

import os
from typing import Dict, List

import requests

BASE_URL = "https://api.setlist.fm/rest/1.0"
USER_AGENT = "radiohead-data-lab/0.1"


def fetch_tour_setlists(artist_mbid: str, year: int, page: int = 1) -> dict:
    api_key = os.getenv("SETLISTFM_API_KEY")
    if not api_key:
        raise RuntimeError("SETLISTFM_API_KEY not set")
    headers = {"x-api-key": api_key, "Accept": "application/json", "User-Agent": USER_AGENT}
    url = f"{BASE_URL}/artist/{artist_mbid}/setlists"
    params = {"year": year, "p": page}
    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def collect_all_setlists(artist_mbid: str, year: int) -> List[dict]:
    results: List[dict] = []
    page = 1
    while True:
        payload = fetch_tour_setlists(artist_mbid, year, page)
        setlists = payload.get("setlist", [])
        if not setlists:
            break
        results.extend(setlists)
        if page >= payload.get("pageTotal", 0):
            break
        page += 1
    return results


def normalize_setlist(s: dict) -> Dict[str, object]:
    songs = []
    for set_data in s.get("sets", {}).get("set", []):
        for song in set_data.get("song", []):
            title = song.get("name")
            if title:
                songs.append(title)
    return {
        "event_date": s.get("eventDate"),
        "tour": s.get("tour", {}).get("name"),
        "venue": s.get("venue", {}).get("name"),
        "city": s.get("venue", {}).get("city", {}).get("name"),
        "country": s.get("venue", {}).get("city", {}).get("country", {}).get("code"),
        "songs": songs,
    }


def export_setlists_json(setlists: List[dict], out_path: str) -> None:
    import json
    from pathlib import Path

    normalized = [normalize_setlist(s) for s in setlists]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(normalized, indent=2), encoding="utf-8")
