# Radiohead Data Lab

A data science project testing whether the common narratives about Radiohead's evolution hold up to quantitative analysis.

## The Central Question

Critics and fans often describe Radiohead's trajectory in familiar terms: the band became "colder," "more abstract," and "emotionally detached" after OK Computer. Kid A is treated as a clean break, a band abandoning warmth for alienation.

But is any of that actually true in the lyrics, or are we conflating sonic texture with thematic content? Did the words change, or just the sounds around them?

This project attempts to quantify what "cold" and "detached" actually mean, then test whether the data supports the narrative.

## Hypotheses

**H1: The "coldness" narrative is overstated.**
Kid A's reputation as emotionally distant may be driven more by its production than its lyrics. Sentiment analysis and emotion classification will test whether the lyrical content actually shifted, or whether critics projected the sonic palette onto the words.

**H2: Vocabulary fragmentation increased, not negativity.**
Thom Yorke's later lyrics feel different because they're structurally fragmented, not because they're sadder. Metrics like lexical diversity, sentence completeness, and coherence scores may explain the "abstract" feeling better than sentiment alone.

**H3: Thematic clustering reveals more continuity than change.**
Topic modeling across albums will test whether Radiohead's core concerns (technology, isolation, identity, decay) remain stable even as delivery changes. The hypothesis is that the band's thematic DNA is more consistent than the "reinvention" narrative suggests.

**H4: In Rainbows is the outlier, not Kid A.**
Conventional wisdom treats Kid A as the pivot point. But In Rainbows may represent a larger emotional shift, a return to directness that breaks from the Kid A through Hail to the Thief period. The data will show which album is the true statistical outlier.

## Methodology

### Data Collection
- Lyrics scraped and cleaned for all studio albums (Pablo Honey through A Moon Shaped Pool)
- Audio features via Spotify API (tempo, energy, valence, acousticness)
- Metadata: release dates, track positions, album context

### Lyrical Analysis
- Sentiment scoring (VADER, TextBlob, and transformer-based models for comparison)
- Emotion classification beyond positive/negative (anger, fear, sadness, joy, disgust, surprise)
- Lexical diversity metrics (TTR, MTLD, vocd-D)
- Sentence structure analysis (completeness, fragmentation indices)

### Statistical Testing
- Album-to-album comparisons with appropriate corrections for multiple testing
- Era-based hypothesis tests (pre-Kid A vs post-Kid A vs post-In Rainbows)
- Effect size calculations to distinguish statistical significance from meaningful difference

### Visualization
- Album trajectories across sentiment and complexity dimensions
- Clustering visualizations to identify natural groupings
- Timeline plots showing evolution of specific metrics

## Project Structure

```
radiohead-lab/
├── data/
│   ├── raw/              # Original scraped lyrics
│   ├── processed/        # Cleaned and tokenized text
│   └── features/         # Extracted metrics per song
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_sentiment_analysis.ipynb
│   ├── 04_lexical_complexity.ipynb
│   ├── 05_topic_modeling.ipynb
│   └── 06_hypothesis_testing.ipynb
├── src/
│   ├── scraping.py
│   ├── preprocessing.py
│   ├── features.py
│   └── visualization.py
├── results/
│   └── figures/
└── README.md
```

## Stack

- Python 3.11+
- pandas, NumPy, SciPy
- matplotlib, seaborn, plotly
- spaCy, NLTK, Hugging Face transformers
- scikit-learn
- Jupyter

## Status

In progress. Data collection complete, exploratory analysis underway.

## Disclaimer

For educational and exploratory purposes only. All music and lyrics remain the property of Radiohead and their respective rights holders.
