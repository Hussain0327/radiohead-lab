"""
Generate static figures for Radiohead Data Lab analysis.

Outputs PNG files to results/figures/ for use in reports and documentation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).resolve().parents[1]
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Donwood-inspired palette
ALBUM_COLORS = {
    "Pablo Honey": "#f97316",
    "The Bends": "#e5e7eb",
    "OK Computer": "#60a5fa",
    "Kid A": "#ef4444",
    "Amnesiac": "#b45309",
    "Hail to the Thief": "#f59e0b",
    "In Rainbows": "#fbbf24",
    "The King of Limbs": "#10b981",
    "A Moon Shaped Pool": "#9ca3af"
}

ALBUM_ORDER = [
    "Pablo Honey", "The Bends", "OK Computer", "Kid A", "Amnesiac",
    "Hail to the Thief", "In Rainbows", "The King of Limbs", "A Moon Shaped Pool"
]

# Dark theme
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#0f1115'
plt.rcParams['axes.facecolor'] = '#141821'
plt.rcParams['axes.edgecolor'] = '#1f2430'
plt.rcParams['axes.labelcolor'] = '#e5e7eb'
plt.rcParams['text.color'] = '#e5e7eb'
plt.rcParams['xtick.color'] = '#9ca3af'
plt.rcParams['ytick.color'] = '#9ca3af'
plt.rcParams['grid.color'] = '#1f2430'
plt.rcParams['font.family'] = 'sans-serif'


def load_data():
    """Load the web data export."""
    path = Path(__file__).resolve().parents[2] / "web" / "src" / "data" / "radiohead_web_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_output_dir():
    """Ensure results/figures/ directory exists."""
    out_dir = Path(__file__).resolve().parents[2] / "results" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def fig_coldness_by_album(data, out_dir):
    """Generate coldness index by album chart."""
    albums = sorted(data["albums"], key=lambda x: ALBUM_ORDER.index(x["album"]))

    fig, ax = plt.subplots(figsize=(12, 6))

    names = [a["album"] for a in albums]
    coldness = [a.get("avg_coldness_index", 0) for a in albums]
    colors = [ALBUM_COLORS.get(a["album"], "#fff") for a in albums]

    bars = ax.barh(names, coldness, color=colors, edgecolor='#1f2430', linewidth=1)

    # Add zero line
    ax.axvline(x=0, color='#374151', linestyle='--', linewidth=1, alpha=0.7)

    ax.set_xlabel("Coldness Index (negative = warmer)", fontsize=11)
    ax.set_title("The Coldness Test: Lyrical Temperature by Album", fontsize=14, fontweight='bold', pad=15)

    # Annotate values
    for bar, val in zip(bars, coldness):
        ax.text(val + 0.02 if val >= 0 else val - 0.02,
                bar.get_y() + bar.get_height()/2,
                f"{val:.2f}",
                va='center', ha='left' if val >= 0 else 'right',
                fontsize=9, color='#9ca3af')

    plt.tight_layout()
    fig.savefig(out_dir / "coldness_by_album.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: coldness_by_album.png")


def fig_sentiment_timeline(data, out_dir):
    """Generate sentiment over time chart."""
    albums = sorted(data["albums"], key=lambda x: x["year"])

    fig, ax = plt.subplots(figsize=(12, 6))

    years = [a["year"] for a in albums]
    sentiment = [a.get("avg_sentiment_score", 0) for a in albums]
    colors = [ALBUM_COLORS.get(a["album"], "#fff") for a in albums]

    ax.plot(years, sentiment, color='#f472b6', linewidth=2, zorder=1)

    for x, y, c, a in zip(years, sentiment, colors, albums):
        ax.scatter(x, y, c=c, s=150, zorder=2, edgecolors='#0f1115', linewidths=2)
        ax.annotate(a["album"].replace("A Moon Shaped Pool", "AMSP"),
                    (x, y), textcoords="offset points", xytext=(0, 12),
                    ha='center', fontsize=8, color='#9ca3af')

    ax.axhline(y=0, color='#374151', linestyle='--', linewidth=1, alpha=0.5)

    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Sentiment Score (VADER compound)", fontsize=11)
    ax.set_title("Emotional Trajectory: Sentiment Over Time", fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    fig.savefig(out_dir / "sentiment_timeline.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: sentiment_timeline.png")


def fig_type_token_ratio(data, out_dir):
    """Generate type-token ratio (lexical diversity) chart."""
    lexical = data.get("lexical_evolution", {}).get("album_metrics", [])
    if not lexical:
        print("  Skipping: type_token_ratio.png (no lexical data)")
        return

    albums = sorted(lexical, key=lambda x: ALBUM_ORDER.index(x["album"]))

    fig, ax = plt.subplots(figsize=(12, 6))

    names = [a["album"] for a in albums]
    ttr = [a["avg_type_token_ratio"] for a in albums]
    colors = [ALBUM_COLORS.get(a["album"], "#fff") for a in albums]

    bars = ax.barh(names, ttr, color=colors, edgecolor='#1f2430', linewidth=1)

    ax.set_xlabel("Type-Token Ratio (vocabulary diversity)", fontsize=11)
    ax.set_title("Vocabulary Evolution: Lexical Diversity by Album", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, 0.6)

    for bar, val in zip(bars, ttr):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f"{val:.2%}", va='center', fontsize=9, color='#9ca3af')

    plt.tight_layout()
    fig.savefig(out_dir / "type_token_ratio.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: type_token_ratio.png")


def fig_wait_times(data, out_dir):
    """Generate song wait times chart."""
    wait_data = data.get("the_wait", {})
    long_waiters = wait_data.get("long_waiters", [])[:10]

    if not long_waiters:
        print("  Skipping: wait_times.png (no wait data)")
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    songs = [s["song"] for s in long_waiters]
    years = [s["wait_years"] for s in long_waiters]

    bars = ax.barh(songs, years, color='#f472b6', edgecolor='#1f2430', linewidth=1)

    ax.set_xlabel("Years from live debut to studio release", fontsize=11)
    ax.set_title("The Wait: Song Gestation Times", fontsize=14, fontweight='bold', pad=15)

    for bar, val in zip(bars, years):
        ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val:.1f} years", va='center', fontsize=9, color='#9ca3af')

    plt.tight_layout()
    fig.savefig(out_dir / "wait_times.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: wait_times.png")


def fig_era_distribution(data, out_dir):
    """Generate 2025 tour era distribution pie chart."""
    tour = data.get("tour_2025", {})
    era_dist = tour.get("era_distribution", {}).get("by_era", {})

    if not era_dist:
        print("  Skipping: era_distribution.png (no tour data)")
        return

    fig, ax = plt.subplots(figsize=(10, 8))

    era_colors = {
        "Early": "#f97316",
        "Peak": "#60a5fa",
        "Reinvention": "#ef4444",
        "Middle": "#f59e0b",
        "Late": "#9ca3af"
    }

    labels = list(era_dist.keys())
    sizes = [era_dist[e]["percentage"] for e in labels]
    colors = [era_colors.get(e, "#fff") for e in labels]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor='#0f1115')
    )

    for autotext in autotexts:
        autotext.set_color('#0f1115')
        autotext.set_fontweight('bold')

    ax.set_title("2025 Reunion Tour: Songs by Era", fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    fig.savefig(out_dir / "era_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: era_distribution.png")


def fig_emotion_comparison(data, out_dir):
    """Generate emotion comparison across albums."""
    albums = sorted(data["albums"], key=lambda x: ALBUM_ORDER.index(x["album"]))

    emotions = ["joy", "sadness", "anger", "fear"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, emotion in enumerate(emotions):
        ax = axes[i]
        names = [a["album"] for a in albums]
        values = [a.get(f"avg_emotion_{emotion}", 0) * 100 for a in albums]
        colors = [ALBUM_COLORS.get(a["album"], "#fff") for a in albums]

        ax.barh(names, values, color=colors, edgecolor='#1f2430', linewidth=1)
        ax.set_xlabel(f"{emotion.title()} %", fontsize=10)
        ax.set_title(f"{emotion.title()}", fontsize=12, fontweight='bold')
        ax.set_xlim(0, max(values) * 1.2 if values else 1)

    plt.suptitle("Emotion Profile by Album", fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(out_dir / "emotion_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: emotion_comparison.png")


def fig_word_count(data, out_dir):
    """Generate average word count by album."""
    albums = sorted(data["albums"], key=lambda x: ALBUM_ORDER.index(x["album"]))

    fig, ax = plt.subplots(figsize=(12, 6))

    names = [a["album"] for a in albums]
    words = [a.get("avg_word_count", 0) for a in albums]
    colors = [ALBUM_COLORS.get(a["album"], "#fff") for a in albums]

    bars = ax.barh(names, words, color=colors, edgecolor='#1f2430', linewidth=1)

    ax.set_xlabel("Average words per track", fontsize=11)
    ax.set_title("Lyric Length by Album", fontsize=14, fontweight='bold', pad=15)

    for bar, val in zip(bars, words):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2,
                f"{int(val)}", va='center', fontsize=9, color='#9ca3af')

    plt.tight_layout()
    fig.savefig(out_dir / "word_count.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Generated: word_count.png")


def main():
    print("=" * 60)
    print("Generating Radiohead Data Lab Figures")
    print("=" * 60)

    data = load_data()
    out_dir = ensure_output_dir()

    print(f"\nOutput directory: {out_dir}\n")

    fig_coldness_by_album(data, out_dir)
    fig_sentiment_timeline(data, out_dir)
    fig_type_token_ratio(data, out_dir)
    fig_wait_times(data, out_dir)
    fig_era_distribution(data, out_dir)
    fig_emotion_comparison(data, out_dir)
    fig_word_count(data, out_dir)

    print(f"\nDone! Figures saved to {out_dir}")


if __name__ == "__main__":
    main()
