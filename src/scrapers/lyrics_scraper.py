"""
Genius lyrics fetcher scaffolding.

Requires GENIUS_ACCESS_TOKEN; network calls should be gated/approved.
"""

from __future__ import annotations

import os
from typing import Dict, List

import requests
from bs4 import BeautifulSoup  # type: ignore

SEARCH_URL = "https://api.genius.com/search"


def _headers():
    token = os.getenv("GENIUS_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("GENIUS_ACCESS_TOKEN not set")
    return {"Authorization": f"Bearer {token}"}


def search_song(query: str) -> Dict[str, object] | None:
    params = {"q": query}
    resp = requests.get(SEARCH_URL, headers=_headers(), params=params, timeout=10)
    resp.raise_for_status()
    hits = resp.json().get("response", {}).get("hits", [])
    if not hits:
        return None
    return hits[0]["result"]


def scrape_lyrics(url: str) -> str:
    """Basic HTML scraper for Genius lyrics page."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    lines: List[str] = []
    for div in lyrics_divs:
        lines.append(div.get_text(separator=" ", strip=True))
    return "\n".join(lines)


def fetch_track_lyrics(track: str, artist: str = "Radiohead") -> str | None:
    hit = search_song(f"{track} {artist}")
    if not hit:
        return None
    url = hit.get("url")
    if not url:
        return None
    return scrape_lyrics(url)
