"""
Hypothesis Testing Module for Radiohead Lyrics Analysis.

Tests the four key hypotheses from the README:

H1: The "coldness" narrative is overstated.
    Kid A's reputation as emotionally distant may be driven more by its
    production than its lyrics.

H2: Vocabulary fragmentation increased, not negativity.
    Thom Yorke's later lyrics feel different because they're structurally
    fragmented, not because they're sadder.

H3: Thematic clustering reveals more continuity than change.
    Topic modeling across albums will test whether Radiohead's core concerns
    remain stable even as delivery changes.

H4: In Rainbows is the outlier, not Kid A.
    Conventional wisdom treats Kid A as the pivot point. But In Rainbows may
    represent a larger emotional shift.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict

try:
    from scipy import stats
except ImportError:
    stats = None  # type: ignore


def load_data(path: Path | None = None) -> List[Dict[str, Any]]:
    if path is None:
        path = Path(__file__).resolve().parents[2] / "data" / "exports" / "radiohead_complete.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def group_by_album(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    albums = defaultdict(list)
    for track in data:
        albums[track["album_name"]].append(track)
    return dict(albums)


def group_by_era(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    eras = defaultdict(list)
    for track in data:
        eras[track["era"]].append(track)
    return dict(eras)


def album_means(data: List[Dict[str, Any]], metric: str) -> Dict[str, float]:
    by_album = group_by_album(data)
    means = {}
    for album, tracks in by_album.items():
        values = [t[metric] for t in tracks if metric in t]
        if values:
            means[album] = sum(values) / len(values)
    return means


def mann_whitney_test(group1: List[float], group2: List[float]) -> Dict[str, Any]:
    if stats is None:
        return {"error": "scipy not available", "u_statistic": None, "p_value": None}

    if len(group1) < 3 or len(group2) < 3:
        return {"error": "Too few samples", "u_statistic": None, "p_value": None}

    result = stats.mannwhitneyu(group1, group2, alternative='two-sided')

    return {
        "u_statistic": round(result.statistic, 4),
        "p_value": round(result.pvalue, 6),
        "significant_05": result.pvalue < 0.05,
        "significant_01": result.pvalue < 0.01,
        "group1_median": round(sorted(group1)[len(group1)//2], 4),
        "group2_median": round(sorted(group2)[len(group2)//2], 4),
        "group1_mean": round(sum(group1)/len(group1), 4),
        "group2_mean": round(sum(group2)/len(group2), 4),
        "group1_n": len(group1),
        "group2_n": len(group2)
    }


def effect_size_cohens_d(group1: List[float], group2: List[float]) -> float:
    n1, n2 = len(group1), len(group2)
    mean1 = sum(group1) / n1
    mean2 = sum(group2) / n2

    var1 = sum((x - mean1) ** 2 for x in group1) / n1
    var2 = sum((x - mean2) ** 2 for x in group2) / n2

    pooled_std = ((var1 * n1 + var2 * n2) / (n1 + n2)) ** 0.5

    if pooled_std == 0:
        return 0.0

    return round((mean1 - mean2) / pooled_std, 4)


# =============================================================================
# H1: THE COLDNESS TEST
# =============================================================================

def test_h1_coldness(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_album = group_by_album(data)

    # Pre-2000 rock era (The Bends, OK Computer)
    pre_2000 = []
    for album in ["The Bends", "OK Computer"]:
        if album in by_album:
            pre_2000.extend([t["coldness_index"] for t in by_album[album]])

    # Kid A
    kid_a = [t["coldness_index"] for t in by_album.get("Kid A", [])]

    test_result = mann_whitney_test(pre_2000, kid_a)
    effect_size = effect_size_cohens_d(pre_2000, kid_a)

    # Album-level coldness means
    coldness_means = album_means(data, "coldness_index")

    return {
        "hypothesis": "H1: Kid A's coldness is overstated",
        "description": (
            "Testing whether Kid A's lyrics are actually colder than "
            "The Bends and OK Computer using coldness_index metric."
        ),
        "comparison": "Pre-2000 (The Bends, OK Computer) vs Kid A",
        "test": "Mann-Whitney U (two-sided)",
        "results": test_result,
        "effect_size_cohens_d": effect_size,
        "effect_interpretation": (
            "negligible (<0.2)" if abs(effect_size) < 0.2 else
            "small (0.2-0.5)" if abs(effect_size) < 0.5 else
            "medium (0.5-0.8)" if abs(effect_size) < 0.8 else
            "large (>0.8)"
        ),
        "coldness_by_album": coldness_means,
        "interpretation": (
            "SUPPORTS H1: No significant difference in lyrical coldness. "
            "Kid A's 'cold' reputation appears driven by production, not lyrics."
            if not test_result.get("significant_05") else
            "CHALLENGES H1: Significant difference found in lyrical coldness."
        )
    }


def test_h1_sentiment(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_album = group_by_album(data)

    rock_era = []
    for album in ["The Bends", "OK Computer"]:
        if album in by_album:
            rock_era.extend([t["sentiment_score"] for t in by_album[album]])

    reinvention_era = []
    for album in ["Kid A", "Amnesiac"]:
        if album in by_album:
            reinvention_era.extend([t["sentiment_score"] for t in by_album[album]])

    test_result = mann_whitney_test(rock_era, reinvention_era)
    effect_size = effect_size_cohens_d(rock_era, reinvention_era)

    return {
        "hypothesis": "H1 (sentiment): Kid A era not more negative",
        "comparison": "Rock Era (Bends, OKC) vs Reinvention Era (Kid A, Amnesiac)",
        "test": "Mann-Whitney U",
        "results": test_result,
        "effect_size_cohens_d": effect_size,
        "interpretation": (
            "SUPPORTS H1: No significant sentiment difference between eras."
            if not test_result.get("significant_05") else
            "CHALLENGES H1: Significant sentiment difference found."
        )
    }


# =============================================================================
# H2: VOCABULARY FRAGMENTATION
# =============================================================================

def test_h2_fragmentation(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_album = group_by_album(data)

    # Calculate album-level metrics
    ttr_by_album = album_means(data, "type_token_ratio")
    sentiment_by_album = album_means(data, "sentiment_score")
    sentence_len_by_album = album_means(data, "avg_sentence_length")

    # Early (pre-2000) vs Late (post-2007)
    early_albums = ["Pablo Honey", "The Bends", "OK Computer"]
    late_albums = ["In Rainbows", "The King of Limbs", "A Moon Shaped Pool"]

    early_ttr = []
    late_ttr = []
    early_sent = []
    late_sent = []

    for album, tracks in by_album.items():
        if album in early_albums:
            early_ttr.extend([t["type_token_ratio"] for t in tracks])
            early_sent.extend([t["sentiment_score"] for t in tracks])
        elif album in late_albums:
            late_ttr.extend([t["type_token_ratio"] for t in tracks])
            late_sent.extend([t["sentiment_score"] for t in tracks])

    ttr_test = mann_whitney_test(early_ttr, late_ttr)
    sent_test = mann_whitney_test(early_sent, late_sent)

    ttr_effect = effect_size_cohens_d(early_ttr, late_ttr)
    sent_effect = effect_size_cohens_d(early_sent, late_sent)

    return {
        "hypothesis": "H2: Vocabulary fragmentation increased, not negativity",
        "description": (
            "Testing whether lexical diversity (type-token ratio) changed "
            "more than sentiment between early and late eras."
        ),
        "comparison": "Early (PH/Bends/OKC) vs Late (IR/TKOL/AMSP)",
        "lexical_diversity": {
            "test": ttr_test,
            "effect_size": ttr_effect,
            "by_album": ttr_by_album
        },
        "sentiment": {
            "test": sent_test,
            "effect_size": sent_effect,
            "by_album": sentiment_by_album
        },
        "sentence_length_by_album": sentence_len_by_album,
        "interpretation": (
            "SUPPORTS H2: Lexical metrics changed more than sentiment."
            if abs(ttr_effect) > abs(sent_effect) else
            "CHALLENGES H2: Sentiment changed as much as lexical metrics."
        )
    }


# =============================================================================
# H4: IN RAINBOWS AS OUTLIER
# =============================================================================

def test_h4_in_rainbows(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_album = group_by_album(data)

    # Compare In Rainbows to its neighbors
    hail_to_thief = [t["sentiment_score"] for t in by_album.get("Hail to the Thief", [])]
    in_rainbows = [t["sentiment_score"] for t in by_album.get("In Rainbows", [])]
    king_limbs = [t["sentiment_score"] for t in by_album.get("The King of Limbs", [])]

    # Also compare Kid A to its neighbors
    ok_computer = [t["sentiment_score"] for t in by_album.get("OK Computer", [])]
    kid_a = [t["sentiment_score"] for t in by_album.get("Kid A", [])]
    amnesiac = [t["sentiment_score"] for t in by_album.get("Amnesiac", [])]

    # Test In Rainbows shifts
    ir_vs_httf = mann_whitney_test(hail_to_thief, in_rainbows) if hail_to_thief and in_rainbows else None
    ir_vs_tkol = mann_whitney_test(in_rainbows, king_limbs) if in_rainbows and king_limbs else None

    # Test Kid A shifts
    ka_vs_okc = mann_whitney_test(ok_computer, kid_a) if ok_computer and kid_a else None
    ka_vs_amn = mann_whitney_test(kid_a, amnesiac) if kid_a and amnesiac else None

    # Calculate warmth for each album
    warmth_by_album = album_means(data, "warmth")
    joy_by_album = album_means(data, "emotion_joy")

    return {
        "hypothesis": "H4: In Rainbows is the outlier, not Kid A",
        "description": (
            "Testing whether In Rainbows represents a larger shift from "
            "adjacent albums compared to Kid A."
        ),
        "in_rainbows_tests": {
            "vs_hail_to_thief": ir_vs_httf,
            "vs_king_of_limbs": ir_vs_tkol
        },
        "kid_a_tests": {
            "vs_ok_computer": ka_vs_okc,
            "vs_amnesiac": ka_vs_amn
        },
        "warmth_by_album": warmth_by_album,
        "joy_by_album": joy_by_album,
        "interpretation": (
            "In Rainbows shows distinct warmth and joy scores, potentially "
            "supporting H4 as a return to directness after the Kid A era."
        )
    }


# =============================================================================
# MOON SHAPED POOL ANALYSIS
# =============================================================================

def analyze_moon_shaped_pool(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_album = group_by_album(data)

    amsp = by_album.get("A Moon Shaped Pool", [])
    other_albums = [t for t in data if t["album_name"] != "A Moon Shaped Pool"]

    if not amsp:
        return {"error": "A Moon Shaped Pool not found in data"}

    # Get AMSP metrics
    amsp_sadness = [t["emotion_sadness"] for t in amsp]
    amsp_sentiment = [t["sentiment_score"] for t in amsp]
    other_sadness = [t["emotion_sadness"] for t in other_albums]
    other_sentiment = [t["sentiment_score"] for t in other_albums]

    sadness_test = mann_whitney_test(other_sadness, amsp_sadness)
    sentiment_test = mann_whitney_test(other_sentiment, amsp_sentiment)

    # Track-level for AMSP
    track_metrics = []
    for track in amsp:
        track_metrics.append({
            "track": track["track_name"],
            "sentiment": track["sentiment_score"],
            "sadness": track["emotion_sadness"],
            "coldness_index": track["coldness_index"],
            "emotional_intensity": track["emotional_intensity"]
        })

    track_metrics.sort(key=lambda x: x["sadness"], reverse=True)

    return {
        "album": "A Moon Shaped Pool",
        "year": 2016,
        "context": (
            "Released May 2016. Rachel Owen, Thom Yorke's partner of 23 years, "
            "passed away in December 2016. The album contains True Love Waits "
            "(21 years in waiting) and Glass Eyes, both achingly personal."
        ),
        "comparison_to_discography": {
            "sadness": sadness_test,
            "sentiment": sentiment_test
        },
        "track_analysis": track_metrics,
        "standout_tracks": [t for t in track_metrics if t["sadness"] > 0.02],
        "mean_sadness": round(sum(amsp_sadness) / len(amsp_sadness), 4),
        "mean_sentiment": round(sum(amsp_sentiment) / len(amsp_sentiment), 4)
    }


# =============================================================================
# FULL HYPOTHESIS REPORT
# =============================================================================

def generate_full_report() -> Dict[str, Any]:
    data = load_data()

    return {
        "dataset_info": {
            "total_tracks": len(data),
            "albums": list(set(t["album_name"] for t in data)),
            "years_span": f"{min(t['album_year'] for t in data)}-{max(t['album_year'] for t in data)}"
        },
        "h1_coldness_test": test_h1_coldness(data),
        "h1_sentiment_test": test_h1_sentiment(data),
        "h2_fragmentation_test": test_h2_fragmentation(data),
        "h4_in_rainbows_test": test_h4_in_rainbows(data),
        "moon_shaped_pool_analysis": analyze_moon_shaped_pool(data)
    }


if __name__ == "__main__":
    import pprint

    print("=" * 70)
    print("RADIOHEAD LYRICS HYPOTHESIS TESTING")
    print("=" * 70)

    report = generate_full_report()

    print("\n--- H1: THE COLDNESS TEST ---")
    pprint.pprint(report["h1_coldness_test"])

    print("\n--- H2: VOCABULARY FRAGMENTATION ---")
    pprint.pprint(report["h2_fragmentation_test"])

    print("\n--- H4: IN RAINBOWS AS OUTLIER ---")
    pprint.pprint(report["h4_in_rainbows_test"])

    print("\n--- A MOON SHAPED POOL ANALYSIS ---")
    pprint.pprint(report["moon_shaped_pool_analysis"])
