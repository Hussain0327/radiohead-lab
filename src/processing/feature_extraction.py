"""
Feature extraction for Radiohead lyrics analysis.

- Tokenization and sentence segmentation (regex-based to avoid heavy deps).
- Lexical stats: token counts, type-token ratio, avg token length, sentence counts.
- Comprehensive sentiment and emotion analysis via src/analysis/sentiment.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List

# Add src directory to path for imports
src_dir = Path(__file__).resolve().parents[1]
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from analysis.sentiment import compute_all_sentiment_features


def basic_tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def split_sentences(text: str) -> List[str]:
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


def compute_features(text: str) -> Dict[str, float | int]:
    tokens = basic_tokenize(text)
    sentences = split_sentences(text)

    # Lexical features
    lex = lexical_stats(tokens, sentences)

    # Comprehensive sentiment and emotion features
    sentiment_features = compute_all_sentiment_features(text)

    # Keep 'sentiment_score' as alias for vader_compound for backwards compatibility
    sentiment_features["sentiment_score"] = sentiment_features["vader_compound"]

    return {**lex, **sentiment_features}
