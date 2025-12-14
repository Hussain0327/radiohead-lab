"""
Advanced sentiment and emotion analysis for Radiohead lyrics.

Goes beyond simple positive/negative polarity to classify emotions:
- joy, sadness, anger, fear, disgust, surprise, trust, anticipation
- "coldness" score (key for H1 hypothesis)
- emotional intensity/arousal

Uses NRC Emotion Lexicon approach with Radiohead-tuned word lists.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple
from functools import lru_cache

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    SentimentIntensityAnalyzer = None


# NRC-style emotion lexicons, curated for rock/alternative lyric context
EMOTION_LEXICONS = {
    "joy": {
        "love", "happy", "beautiful", "perfect", "hope", "angel", "rainbow",
        "wonderful", "warm", "alive", "bloom", "glow", "smile", "laugh",
        "light", "bright", "free", "peace", "heaven", "dream", "sunshine",
        "lucky", "amazing", "sweet", "soft", "gentle", "tender", "bliss",
        "celebrate", "embrace", "kiss", "dance", "fly", "float", "rise"
    },
    "sadness": {
        "sad", "cry", "tears", "alone", "lost", "empty", "broken", "hurt",
        "pain", "grief", "mourn", "weep", "sorrow", "despair", "misery",
        "lonely", "abandoned", "miss", "gone", "fade", "wither", "drown",
        "fall", "sink", "dark", "grey", "gray", "rain", "cold", "numb",
        "hollow", "ache", "regret", "sorry", "heartbreak", "goodbye"
    },
    "anger": {
        "hate", "angry", "rage", "fury", "mad", "kill", "destroy", "fight",
        "war", "attack", "violent", "scream", "yell", "shout", "blood",
        "revenge", "bitter", "hostile", "aggressive", "cruel", "brutal",
        "smash", "crash", "burn", "explode", "weapon", "bullet", "knife"
    },
    "fear": {
        "fear", "afraid", "scared", "terror", "horror", "panic", "dread",
        "nightmare", "monster", "ghost", "haunt", "creep", "shadow", "dark",
        "danger", "threat", "warning", "alarm", "paranoid", "nervous",
        "anxiety", "worry", "tremble", "shake", "hide", "escape", "run"
    },
    "disgust": {
        "disgust", "sick", "vomit", "rotten", "decay", "filth", "dirt",
        "ugly", "nasty", "gross", "repulsive", "toxic", "poison", "waste",
        "trash", "stink", "smell", "contaminate", "corrupt", "disease"
    },
    "surprise": {
        "surprise", "shock", "sudden", "unexpected", "wonder", "amazed",
        "astonish", "startle", "jolt", "gasp", "breathless", "speechless",
        "miracle", "incredible", "unbelievable", "strange", "weird", "odd"
    },
    "trust": {
        "trust", "believe", "faith", "loyal", "honest", "true", "real",
        "friend", "together", "promise", "commit", "depend", "rely",
        "safe", "secure", "protect", "care", "support", "help", "hold"
    },
    "anticipation": {
        "wait", "expect", "hope", "wish", "want", "need", "yearn", "long",
        "crave", "desire", "dream", "plan", "ready", "prepare", "future",
        "tomorrow", "coming", "soon", "next", "forward", "ahead"
    }
}

# Coldness lexicon - key for testing H1 (Kid A coldness hypothesis)
COLDNESS_LEXICON = {
    "cold_words": {
        "cold", "ice", "frozen", "freeze", "chill", "winter", "snow",
        "numb", "distant", "remote", "detached", "machine", "robot",
        "computer", "digital", "static", "void", "empty", "hollow",
        "clinical", "sterile", "synthetic", "artificial", "mechanical",
        "electronic", "plastic", "glass", "metal", "chrome", "grey", "gray"
    },
    "warm_words": {
        "warm", "hot", "heat", "fire", "burn", "sun", "summer", "glow",
        "touch", "hold", "embrace", "heart", "blood", "flesh", "skin",
        "breath", "alive", "human", "organic", "natural", "real", "soul",
        "love", "passion", "tender", "soft", "gentle", "close", "near"
    }
}

# Alienation/isolation lexicon - for testing emotional distance
ALIENATION_LEXICON = {
    "isolated": {
        "alone", "lonely", "isolated", "separate", "apart", "away",
        "distant", "remote", "outsider", "stranger", "alien", "foreign",
        "different", "other", "nowhere", "lost", "invisible", "forgotten",
        "abandoned", "rejected", "excluded", "disconnected", "detached"
    },
    "connected": {
        "together", "us", "we", "our", "friend", "family", "home",
        "belong", "join", "unite", "share", "bond", "connection",
        "community", "people", "human", "touch", "hold", "embrace"
    }
}


def basic_tokenize(text: str) -> List[str]:
    """Simple word tokenizer; lowercases and keeps apostrophes inside words."""
    return re.findall(r"[a-zA-Z']+", text.lower())


@lru_cache(maxsize=1)
def _get_vader():
    if SentimentIntensityAnalyzer is None:
        return None
    try:
        return SentimentIntensityAnalyzer()
    except Exception:
        return None


def vader_sentiment(text: str) -> Dict[str, float]:
    """Get VADER sentiment scores."""
    sia = _get_vader()
    if sia:
        scores = sia.polarity_scores(text)
        return {
            "vader_compound": round(scores["compound"], 4),
            "vader_positive": round(scores["pos"], 4),
            "vader_negative": round(scores["neg"], 4),
            "vader_neutral": round(scores["neu"], 4)
        }
    return {
        "vader_compound": 0.0,
        "vader_positive": 0.0,
        "vader_negative": 0.0,
        "vader_neutral": 1.0
    }


def emotion_scores(tokens: List[str]) -> Dict[str, float]:
    """
    Calculate emotion scores based on lexicon matching.
    Returns normalized scores (0-1) for each emotion category.
    """
    if not tokens:
        return {f"emotion_{e}": 0.0 for e in EMOTION_LEXICONS.keys()}

    token_set = set(tokens)
    scores = {}

    for emotion, lexicon in EMOTION_LEXICONS.items():
        matches = token_set.intersection(lexicon)
        # Count occurrences, not just unique matches
        count = sum(1 for t in tokens if t in lexicon)
        # Normalize by total tokens
        scores[f"emotion_{emotion}"] = round(count / len(tokens), 4)

    return scores


def coldness_score(tokens: List[str]) -> Dict[str, float]:
    """
    Calculate coldness vs warmth score.
    Key metric for testing H1 hypothesis about Kid A.

    Returns:
        coldness: ratio of cold words (0-1)
        warmth: ratio of warm words (0-1)
        coldness_index: (cold - warm) / total, ranges -1 to 1
    """
    if not tokens:
        return {"coldness": 0.0, "warmth": 0.0, "coldness_index": 0.0}

    cold_count = sum(1 for t in tokens if t in COLDNESS_LEXICON["cold_words"])
    warm_count = sum(1 for t in tokens if t in COLDNESS_LEXICON["warm_words"])

    total = len(tokens)
    coldness = round(cold_count / total, 4)
    warmth = round(warm_count / total, 4)

    # Coldness index: positive = colder, negative = warmer
    if cold_count + warm_count > 0:
        index = round((cold_count - warm_count) / (cold_count + warm_count), 4)
    else:
        index = 0.0

    return {
        "coldness": coldness,
        "warmth": warmth,
        "coldness_index": index
    }


def alienation_score(tokens: List[str]) -> Dict[str, float]:
    """
    Calculate alienation vs connection score.
    Measures emotional distance/isolation in lyrics.
    """
    if not tokens:
        return {"alienation": 0.0, "connection": 0.0, "alienation_index": 0.0}

    iso_count = sum(1 for t in tokens if t in ALIENATION_LEXICON["isolated"])
    conn_count = sum(1 for t in tokens if t in ALIENATION_LEXICON["connected"])

    total = len(tokens)
    alienation = round(iso_count / total, 4)
    connection = round(conn_count / total, 4)

    if iso_count + conn_count > 0:
        index = round((iso_count - conn_count) / (iso_count + conn_count), 4)
    else:
        index = 0.0

    return {
        "alienation": alienation,
        "connection": connection,
        "alienation_index": index
    }


def emotional_intensity(tokens: List[str]) -> float:
    """
    Calculate overall emotional intensity/arousal.
    High intensity = lots of emotion words (any type).
    """
    if not tokens:
        return 0.0

    all_emotion_words = set()
    for lexicon in EMOTION_LEXICONS.values():
        all_emotion_words.update(lexicon)

    count = sum(1 for t in tokens if t in all_emotion_words)
    return round(count / len(tokens), 4)


def compute_all_sentiment_features(text: str) -> Dict[str, float]:
    """
    Compute comprehensive sentiment and emotion features for a text.

    Returns dict with:
    - VADER scores (compound, pos, neg, neu)
    - 8 emotion category scores
    - coldness/warmth metrics
    - alienation/connection metrics
    - emotional intensity
    """
    tokens = basic_tokenize(text)

    features = {}

    # VADER sentiment
    features.update(vader_sentiment(text))

    # Emotion categories
    features.update(emotion_scores(tokens))

    # Coldness (H1 key metric)
    features.update(coldness_score(tokens))

    # Alienation
    features.update(alienation_score(tokens))

    # Overall intensity
    features["emotional_intensity"] = emotional_intensity(tokens)

    return features


# Convenience function for quick sentiment
def get_sentiment(text: str) -> float:
    """Simple interface - returns VADER compound score."""
    return vader_sentiment(text)["vader_compound"]
