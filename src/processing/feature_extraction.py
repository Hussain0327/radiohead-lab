"""
Lightweight feature extraction for lyrics.

- Tokenization and sentence segmentation (regex-based to avoid heavy deps).
- Lexical stats: token counts, type-token ratio, avg token length, sentence counts.
- Sentiment: prefers VADER if available; falls back to a small lexicon.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Dict, List

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except Exception:  # pragma: no cover - optional dependency
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
    except Exception:
        SentimentIntensityAnalyzer = None  # type: ignore


def basic_tokenize(text: str) -> List[str]:
    """Simple word tokenizer; lowercases and keeps apostrophes inside words."""
    return re.findall(r"[a-zA-Z']+", text.lower())


def split_sentences(text: str) -> List[str]:
    """Very rough sentence split on punctuation."""
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def lexical_stats(tokens: List[str], sentences: List[str]) -> Dict[str, float]:
    token_count = len(tokens)
    unique_token_count = len(set(tokens))
    type_token_ratio = unique_token_count / token_count if token_count else 0.0
    avg_token_length = sum(len(t) for t in tokens) / token_count if token_count else 0.0
    sentence_count = len(sentences)
    avg_sentence_length = token_count / sentence_count if sentence_count else 0.0

    return {
        "token_count": token_count,
        "unique_token_count": unique_token_count,
        "type_token_ratio": round(type_token_ratio, 4),
        "avg_token_length": round(avg_token_length, 3),
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 3),
    }


@lru_cache(maxsize=1)
def _get_vader():
    """Initialize VADER once if available and data is present."""
    if SentimentIntensityAnalyzer is None:
        return None
    try:
        return SentimentIntensityAnalyzer()
    except Exception:
        return None


# Minimal fallback lexicon
POSITIVE = {
    "love",
    "happy",
    "beautiful",
    "perfect",
    "hope",
    "angel",
    "rainbow",
    "wonderful",
    "warm",
    "alive",
    "bloom",
    "glow",
}
NEGATIVE = {
    "hurt",
    "cry",
    "sad",
    "cold",
    "fear",
    "die",
    "alone",
    "blood",
    "drown",
    "kill",
    "broken",
    "ghost",
    "weapon",
    "blackout",
    "paranoid",
}


def sentiment_score(text: str, tokens: List[str]) -> float:
    """
    Return polarity in [-1, 1]. Uses VADER if available, else a tiny lexicon.
    """
    sia = _get_vader()
    if sia:
        try:
            return round(sia.polarity_scores(text)["compound"], 4)
        except Exception:
            pass

    if not tokens:
        return 0.0
    pos = sum(1 for t in tokens if t in POSITIVE)
    neg = sum(1 for t in tokens if t in NEGATIVE)
    return round((pos - neg) / len(tokens), 4)


def compute_features(text: str) -> Dict[str, float | int]:
    tokens = basic_tokenize(text)
    sentences = split_sentences(text)
    lex = lexical_stats(tokens, sentences)
    sent = sentiment_score(text, tokens)
    return {**lex, "sentiment_score": sent}
