# Radiohead Data Lab

A data science and web project exploring Radiohead's lyrical evolution through NLP, statistical analysis, and interactive visualization. Built as a tribute to the band's 2025 reunion tour, their first performances in seven years.

<p align="center">
  <img src="assets/the-bends.jpg" width="130" alt="The Bends"/>
  <img src="assets/ok-computer.jpg" width="130" alt="OK Computer"/>
  <img src="assets/kid-a.jpg" width="130" alt="Kid A"/>
  <img src="assets/Inrainbows.jpg" width="130" alt="In Rainbows"/>
  <img src="assets/moon-shaped-pool.jpg" width="130" alt="A Moon Shaped Pool"/>
</p>

## Context: The 2025 Reunion

After seven years of silence, Radiohead returned to the stage in November 2025 for a 20-date European tour. They played in the round for the first time since 1993, drawing from a 65-song pool that Thom Yorke compiled for rotating setlists. The tour came after years of grief, mental health struggles, and uncertainty about whether the band would ever perform together again.

This project explores the patterns in their music that brought fans back.

## The Central Question

Critics and fans often describe Radiohead's trajectory in familiar terms: the band became "colder," "more abstract," and "emotionally detached" after OK Computer. Kid A is treated as a clean break, a band abandoning warmth for alienation.

But is any of that actually true in the lyrics, or are we conflating sonic texture with thematic content? Did the words change, or just the sounds around them?

This project attempts to quantify what "cold" and "detached" actually mean, then test whether the data supports the narrative.

## The Discography

| Era         | Album              | Year | Narrative                                  |
| ----------- | ------------------ | ---- | ------------------------------------------ |
| Early       | Pablo Honey        | 1993 | Raw, unformed, Creep-dependent             |
| Early       | The Bends          | 1995 | Anthemic, emotional, guitar-driven         |
| Peak        | OK Computer        | 1997 | Paranoid, sprawling, the "last rock album" |
| Reinvention | Kid A              | 2000 | Cold, fractured, electronic alienation     |
| Reinvention | Amnesiac           | 2001 | Kid A's darker twin, jazz-inflected        |
| Middle      | Hail to the Thief  | 2003 | Political, dense, return to guitars        |
| Late        | In Rainbows        | 2007 | Warm, direct, romantic                     |
| Late        | The King of Limbs  | 2011 | Rhythmic, skeletal, loop-based             |
| Late        | A Moon Shaped Pool | 2016 | Orchestral, mournful, retrospective        |

## Hypotheses

**H1: The "coldness" narrative is overstated.**
Kid A's reputation as emotionally distant may be driven more by its production than its lyrics. Sentiment analysis and emotion classification will test whether the lyrical content actually shifted, or whether critics projected the sonic palette onto the words.

**H2: Vocabulary fragmentation increased, not negativity.**
Thom Yorke's later lyrics feel different because they're structurally fragmented, not because they're sadder. Metrics like lexical diversity, sentence completeness, and coherence scores may explain the "abstract" feeling better than sentiment alone.

**H3: Thematic clustering reveals more continuity than change.**
Topic modeling across albums will test whether Radiohead's core concerns (technology, isolation, identity, decay) remain stable even as delivery changes. The hypothesis is that the band's thematic DNA is more consistent than the "reinvention" narrative suggests.

**H4: In Rainbows is the outlier, not Kid A.**
Conventional wisdom treats Kid A as the pivot point. But In Rainbows may represent a larger emotional shift, a return to directness that breaks from the Kid A through Hail to the Thief period. The data will show which album is the true statistical outlier.

## Key Analyses

### The Wait

Chart every song by how long it took from first live performance to studio release. True Love Waits existed for 21 years as a live-only track before appearing on A Moon Shaped Pool in 2016, the same year Rachel Owen passed away. Twenty-one years of waiting to release a song called "True Love Waits," and when they finally did, it was a goodbye.

### Glass Eyes and the A Moon Shaped Pool Cluster

Sentiment and emotional valence analysis showing how that album sits apart from everything else in the discography.

### The Coldness Test

H1 visualized. Show whether Kid A's lyrics are actually colder or if critics projected the electronic production onto the words.

### Vocabulary Fragmentation Over Time

Lexical diversity plots tracking how Thom's writing became more abstract across eras.

### Setlist Archaeology

2025 tour setlist analysis showing which eras the band drew from for their return.

## Project Structure

```
radiohead-lab/
├── assets/                          # Album artwork for README
├── data/
│   ├── raw/                         # Original scraped data
│   ├── processed/                   # Cleaned datasets
│   └── exports/
│       └── radiohead_complete.json  # Final dataset for web
├── src/
│   ├── scrapers/
│   │   ├── lyrics_scraper.py        # Genius API
│   │   ├── audio_features.py        # Spotify API
│   │   └── setlist_scraper.py       # setlist.fm for 2025 tour
│   ├── processing/
│   │   ├── clean_lyrics.py
│   │   ├── tokenization.py
│   │   └── feature_extraction.py
│   ├── analysis/
│   │   ├── sentiment.py
│   │   ├── lexical_diversity.py
│   │   ├── topic_modeling.py
│   │   └── hypothesis_tests.py
│   └── visualization/
│       ├── album_trajectories.py
│       ├── clustering_plots.py
│       └── timeline_charts.py
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_sentiment_deep_dive.ipynb
│   ├── 04_true_love_waits_case_study.ipynb
│   ├── 05_lexical_evolution.ipynb
│   ├── 06_topic_modeling.ipynb
│   ├── 07_hypothesis_testing.ipynb
│   └── 08_export_for_web.ipynb
├── web/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AlbumExplorer.jsx
│   │   │   ├── SentimentTimeline.jsx
│   │   │   ├── LyricAnalyzer.jsx
│   │   │   ├── TrueLoveWaits.jsx
│   │   │   └── ReunionTour2025.jsx
│   │   ├── data/
│   │   │   └── radiohead_complete.json
│   │   ├── styles/
│   │   │   └── donwood.css
│   │   └── App.jsx
│   ├── public/
│   └── package.json
├── results/
│   └── figures/
├── requirements.txt
└── README.md
```

## Visual Language

The web experience shifts palettes based on Stanley Donwood's artwork for each album era:

| Album              | Palette                          | Texture               |
| ------------------ | -------------------------------- | --------------------- |
| The Bends          | Clinical whites, medical imagery | Sterile, unsettling   |
| OK Computer        | Washed blues, highway grays      | Smeared, ghostly      |
| Kid A              | Reds, mountain whites            | Jagged, digital decay |
| Amnesiac           | Sepia, minotaur blacks           | Labyrinthine          |
| Hail to the Thief  | Map colors, dense text           | Cartographic chaos    |
| In Rainbows        | Spectrum explosion               | Layered, warm         |
| The King of Limbs  | Forest greens, newspaper         | Organic, fragmented   |
| A Moon Shaped Pool | Muted, ash, water                | Grief, dissolution    |

## Stack

**Data Pipeline**

- Python 3.11+
- pandas, NumPy, SciPy
- spaCy, NLTK, Hugging Face transformers
- scikit-learn
- Genius API, Spotify API, setlist.fm API

**Analysis**

- Jupyter notebooks
- matplotlib, seaborn, plotly

**Web**

- React
- Tailwind CSS
- Vercel/Netlify deployment

## Status

In progress. Data collection complete, exploratory analysis underway.

## What’s been done (portfolio snapshot)

- Wired a minimal ingestion pipeline: ingest `data/raw/new_data_1.csv` (Kaggle lyrics set), clean album/track names, add lexical stats and VADER sentiment placeholders, export to `data/exports/radiohead_complete.json` (mirrored to `web/src/data/`).
- Added analysis notebooks that now load reliably regardless of working directory:
  - `02_exploratory_analysis.ipynb`: quick EDA on words/sentiment.
  - `03_sentiment_deep_dive.ipynb`: album averages + distribution.
  - `05_lexical_evolution.ipynb`: type-token ratio and sentence length over time.
  - `06_topic_modeling.ipynb`: rough LDA sketch.
  - `07_hypothesis_testing.ipynb`: quick H1/H4 tests (Kid A coldness, In Rainbows outlier).
  - `04_true_love_waits_case_study.ipynb`: placeholder wait-time calc until setlists arrive.
- Built a thin React/Vite slice (`web/`) with album-era palette bars and a sentiment timeline pulling from the exported JSON.
- Scaffolding in place for scrapers (Genius lyrics, Spotify audio features, setlist.fm).
- Local `.env` and `.gitignore` added to keep secrets out of git.

Data source (current):
- `data/raw/new_data_1.csv` (Kaggle lyrics dataset, 100 tracks across 9 albums). No other sources are merged yet.

Where we’re stuck:
- Spotify `audio-features` endpoint returns 403 with client-credential tokens. Need a short-lived user access token (`SPOTIFY_ACCESS_TOKEN`) to enrich tracks; until then, `radiohead_with_audio.json` has empty features.
- No setlist.fm or live True Love Waits timing data pulled yet.

What’s next:
1) Add a user access token to `.env` (`SPOTIFY_ACCESS_TOKEN=...`) and rerun `src/processing/ingest_csv.py` plus the audio enrichment to fill `data/exports/radiohead_with_audio.json`.
2) Add setlist.fm API key to `.env`, scrape 2025 tour setlists, and compute the True Love Waits wait-time properly.
3) Swap naive sentiment for a better model and expand emotion/coherence metrics; update notebooks and export.
4) Flesh out web components (AlbumExplorer, LyricAnalyzer, ReunionTour2025, TrueLoveWaits) with Donwood-era theming and add more plots to `results/`.
5) Optional: Tailwind + deployment (Vercel/Netlify) once visuals firm up.

Safety/commits:
- Secrets live only in `.env` (ignored by git). Do not commit `.env`. The repo is safe to commit as-is.***

## Disclaimer

For educational and analytical purposes only. Built as a tribute to Radiohead's 2025 reunion. Album artwork shown under fair use for commentary. All music, lyrics, and artwork remain the property of Radiohead and their respective rights holders.
