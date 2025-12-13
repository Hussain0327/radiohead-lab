"""
Spotify audio feature fetcher scaffolding.

Requires Spotify client credentials; set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.
Network calls should be gated/approved before use.
"""

from __future__ import annotations

import os
from typing import Dict, List

import requests

TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"
FEATURES_URL = "https://api.spotify.com/v1/audio-features"


def _get_token() -> str:
    # Allow a pre-generated user access token (e.g., from Spotify console) to bypass client-cred limits.
    override = os.getenv("SPOTIFY_ACCESS_TOKEN")
    if override:
        return override

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("SPOTIFY_CLIENT_ID/SECRET not set")
    resp = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def search_track(query: str, token: str) -> str | None:
    """Return the first track ID for a query."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}
    resp = requests.get(SEARCH_URL, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    items = resp.json().get("tracks", {}).get("items", [])
    if not items:
        return None
    return items[0]["id"]


def fetch_audio_features(track_ids: List[str], token: str) -> List[Dict[str, object]]:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        FEATURES_URL, headers=headers, params={"ids": ",".join(track_ids)}, timeout=10
    )
    if resp.status_code == 403:
        # Some apps/tokens are blocked from audio-features via client credentials; caller can fall back.
        return []
    resp.raise_for_status()
    return resp.json().get("audio_features", [])


def enrich_tracks_with_audio_features(tracks: List[dict]) -> List[dict]:
    """Attach Spotify audio features to track dicts where possible."""
    token = _get_token()
    enriched = []
    for row in tracks:
        query = f"{row['track_name']} radiohead"
        track_id = search_track(query, token)
        if not track_id:
            enriched.append(row)
            continue
        feats = fetch_audio_features([track_id], token)
        audio = feats[0] if feats else {}
        enriched.append({**row, "spotify_id": track_id, "audio_features": audio})
    return enriched
