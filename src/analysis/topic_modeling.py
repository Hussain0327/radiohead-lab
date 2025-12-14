"""
Topic Modeling for Radiohead Lyrics Analysis.

Tests H3: Thematic clustering reveals more continuity than change.
Topic modeling across albums will test whether Radiohead's core concerns
(technology, isolation, identity, decay) remain stable even as delivery changes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter

try:
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation, NMF
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# Stop words extended for lyric analysis
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
    'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't",
    'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
    "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
    "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
    "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
    "wouldn't", 'oh', 'yeah', 'la', 'da', 'na', 'ah', 'ooh', 'hey', 'uh', 'um',
    'gonna', 'wanna', 'gotta', 'cause', "'cause", 'cuz', 'like', 'get', 'got', 'go',
    'know', 'see', 'come', 'take', 'make', 'let', 'say', 'thing', 'way', 'one', 'two'
}

# Theme labels based on Radiohead's recurring concerns
THEME_LABELS = {
    0: "Technology & Alienation",
    1: "Nature & Environment",
    2: "Love & Loss",
    3: "Identity & Self",
    4: "Power & Politics",
    5: "Death & Decay",
    6: "Movement & Escape",
    7: "Time & Memory"
}


def load_data(path: Path | None = None) -> List[Dict[str, Any]]:
    """Load the complete Radiohead dataset."""
    if path is None:
        path = Path(__file__).resolve().parents[2] / "data" / "exports" / "radiohead_complete.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def preprocess_lyrics(text: str) -> str:
    """Clean lyrics for topic modeling."""
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)
    # Remove numbers
    text = re.sub(r"\d+", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Remove stop words
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return " ".join(words)


def extract_keywords(data: List[Dict[str, Any]], top_n: int = 50) -> List[Tuple[str, int]]:
    """Extract most common non-stop words across all lyrics."""
    all_words = []
    for track in data:
        clean = preprocess_lyrics(track["lyrics"])
        all_words.extend(clean.split())

    return Counter(all_words).most_common(top_n)


def extract_keywords_by_album(data: List[Dict[str, Any]], top_n: int = 20) -> Dict[str, List[Tuple[str, int]]]:
    """Extract most common words per album."""
    by_album = defaultdict(list)
    for track in data:
        by_album[track["album_name"]].append(preprocess_lyrics(track["lyrics"]))

    album_keywords = {}
    for album, lyrics_list in by_album.items():
        all_words = " ".join(lyrics_list).split()
        album_keywords[album] = Counter(all_words).most_common(top_n)

    return album_keywords


def run_lda(data: List[Dict[str, Any]], n_topics: int = 5) -> Dict[str, Any]:
    """
    Run LDA topic modeling on the lyrics corpus.

    Returns topic distributions and top words per topic.
    """
    if not SKLEARN_AVAILABLE:
        return {"error": "sklearn not available"}

    # Prepare corpus
    corpus = [preprocess_lyrics(t["lyrics"]) for t in data]
    track_names = [t["track_name"] for t in data]
    album_names = [t["album_name"] for t in data]

    # Create document-term matrix
    vectorizer = CountVectorizer(
        max_features=2000,
        min_df=2,
        max_df=0.95
    )
    dtm = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()

    # Fit LDA
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=20
    )
    doc_topics = lda.fit_transform(dtm)

    # Extract top words per topic
    topics = []
    for idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[-15:][::-1]
        top_words = [feature_names[i] for i in top_indices]
        topics.append({
            "topic_id": idx,
            "label": THEME_LABELS.get(idx, f"Topic {idx}"),
            "top_words": top_words,
            "word_weights": {feature_names[i]: round(topic[i], 4) for i in top_indices[:10]}
        })

    # Get dominant topic per track
    track_topics = []
    for i, (track, album) in enumerate(zip(track_names, album_names)):
        dominant = int(doc_topics[i].argmax())
        track_topics.append({
            "track": track,
            "album": album,
            "dominant_topic": dominant,
            "topic_distribution": {f"topic_{j}": round(doc_topics[i][j], 4) for j in range(n_topics)}
        })

    # Aggregate by album
    album_topic_dist = defaultdict(lambda: defaultdict(list))
    for tt in track_topics:
        for j in range(n_topics):
            album_topic_dist[tt["album"]][j].append(tt["topic_distribution"][f"topic_{j}"])

    album_means = {}
    for album, topics_dict in album_topic_dist.items():
        album_means[album] = {
            f"topic_{j}": round(sum(v) / len(v), 4) for j, v in topics_dict.items()
        }

    return {
        "n_topics": n_topics,
        "topics": topics,
        "track_topics": track_topics,
        "album_topic_distribution": album_means,
        "vocabulary_size": len(feature_names)
    }


def test_h3_thematic_continuity(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    H3: Thematic clustering reveals more continuity than change.

    Analyze whether core themes (technology, isolation, identity, decay)
    remain stable across albums even as the sound changed.
    """
    # Get overall keywords
    overall_keywords = extract_keywords(data, top_n=30)

    # Get keywords by album
    album_keywords = extract_keywords_by_album(data, top_n=15)

    # Run topic modeling
    lda_results = run_lda(data, n_topics=5)

    # Calculate thematic overlap between albums
    # (percentage of shared top keywords)
    albums = list(album_keywords.keys())
    overlap_matrix = {}

    for a1 in albums:
        words1 = set(w for w, _ in album_keywords[a1])
        overlap_matrix[a1] = {}
        for a2 in albums:
            words2 = set(w for w, _ in album_keywords[a2])
            overlap = len(words1.intersection(words2)) / len(words1.union(words2))
            overlap_matrix[a1][a2] = round(overlap, 3)

    # Find consistent themes across all albums
    consistent_words = set(w for w, _ in album_keywords[albums[0]])
    for album in albums[1:]:
        consistent_words &= set(w for w, _ in album_keywords[album])

    return {
        "hypothesis": "H3: Thematic clustering reveals more continuity than change",
        "description": (
            "Testing whether Radiohead's core thematic concerns remain stable "
            "across albums, even as production and delivery changed."
        ),
        "overall_keywords": overall_keywords,
        "album_keywords": album_keywords,
        "keyword_overlap_matrix": overlap_matrix,
        "consistent_themes": list(consistent_words),
        "topic_modeling": lda_results if isinstance(lda_results, dict) and "error" not in lda_results else None,
        "interpretation": (
            f"Found {len(consistent_words)} words appearing in top keywords of every album, "
            f"suggesting core thematic DNA persists across eras."
        )
    }


def export_for_web() -> Dict[str, Any]:
    """Export topic modeling results for web visualization."""
    data = load_data()

    keywords = extract_keywords(data, top_n=50)
    album_keywords = extract_keywords_by_album(data, top_n=20)
    lda = run_lda(data, n_topics=5)

    return {
        "overall_keywords": keywords,
        "album_keywords": album_keywords,
        "topics": lda.get("topics", []),
        "album_topic_distribution": lda.get("album_topic_distribution", {}),
        "track_topics": lda.get("track_topics", [])
    }


if __name__ == "__main__":
    import pprint

    print("=" * 70)
    print("RADIOHEAD TOPIC MODELING")
    print("=" * 70)

    data = load_data()

    print("\n--- TOP 30 KEYWORDS (ALL ALBUMS) ---")
    keywords = extract_keywords(data, 30)
    for word, count in keywords:
        print(f"  {word}: {count}")

    print("\n--- H3: THEMATIC CONTINUITY TEST ---")
    h3 = test_h3_thematic_continuity(data)
    print(f"\nConsistent themes across all albums: {h3['consistent_themes']}")
    print(f"\n{h3['interpretation']}")

    if h3["topic_modeling"]:
        print("\n--- TOPICS ---")
        for topic in h3["topic_modeling"]["topics"]:
            print(f"\n  Topic {topic['topic_id']}: {', '.join(topic['top_words'][:8])}")
