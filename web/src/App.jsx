import data from "./data/radiohead_complete.json";
import "./styles/donwood.css";

function buildAlbumStats(tracks) {
  const map = {};
  tracks.forEach((track) => {
    const album = track.album_name;
    if (!map[album]) {
      map[album] = {
        album,
        year: track.album_year,
        era: track.era,
        wordSum: 0,
        sentimentSum: 0,
        tracks: 0,
      };
    }
    map[album].wordSum += track.word_count || 0;
    map[album].sentimentSum += track.sentiment_score || 0;
    map[album].tracks += 1;
  });

  return Object.values(map)
    .map((entry) => ({
      album: entry.album,
      year: entry.year,
      era: entry.era,
      avgWords: entry.wordSum / entry.tracks,
      avgSentiment: entry.sentimentSum / entry.tracks,
      tracks: entry.tracks,
    }))
    .sort((a, b) => a.year - b.year);
}

const stats = buildAlbumStats(data);
const maxWords = Math.max(...stats.map((s) => s.avgWords), 1);
const minYear = Math.min(...stats.map((s) => s.year));
const maxYear = Math.max(...stats.map((s) => s.year));
const sentiments = stats.map((s) => s.avgSentiment);
const minSent = Math.min(...sentiments);
const maxSent = Math.max(...sentiments);

const albumPalette = {
  "Pablo Honey": "#f97316",
  "The Bends": "#e5e7eb",
  "OK Computer": "#60a5fa",
  "Kid A": "#ef4444",
  Amnesiac: "#b45309",
  "Hail to the Thief": "#f59e0b",
  "In Rainbows": "#fbbf24",
  "The King of Limbs": "#10b981",
  "A Moon Shaped Pool": "#9ca3af",
};

function barColor(album) {
  return albumPalette[album] || "#f472b6";
}

function sentimentPoints() {
  const w = 780;
  const h = 220;
  const pad = 40;
  const yrRange = maxYear - minYear || 1;
  const sentRange = maxSent - minSent || 1;

  return stats.map((s) => {
    const x = pad + ((s.year - minYear) / yrRange) * (w - pad * 2);
    const y =
      h - pad - ((s.avgSentiment - minSent) / sentRange) * (h - pad * 2);
    return { ...s, x, y };
  });
}

export default function App() {
  const points = sentimentPoints();

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Radiohead Data Lab</p>
          <h1>Lyric length + sentiment by album</h1>
          <p className="lede">
            Cleaned tracks from the Kaggle CSV, lexical features, and a quick
            sentiment pass to tee up the deeper H1–H4 tests.
          </p>
        </div>
        <div className="pill">
          {data.length} tracks · {stats.length} albums
        </div>
      </header>

      <section className="panel">
        <div className="panel-header">
          <h2>Average words per track</h2>
          <p className="panel-sub">
            Bars scale to the wordiest album; colors echo the album-era palette.
          </p>
        </div>

        {stats.length === 0 ? (
          <p>No data loaded.</p>
        ) : (
          <div className="bar-list">
            {stats.map((stat) => (
              <div className="bar-row" key={stat.album}>
                <div className="bar-meta">
                  <div className="bar-title">
                    {stat.album} <span className="era">· {stat.era}</span>
                  </div>
                  <div className="bar-sub">
                    {stat.year} · {stat.tracks} tracks · sentiment{" "}
                    {stat.avgSentiment.toFixed(3)}
                  </div>
                </div>
                <div className="bar-shell">
                  <div
                    className="bar-fill"
                    style={{
                      background: `linear-gradient(90deg, ${barColor(
                        stat.album
                      )}, ${barColor(stat.album)}aa)`,
                      width: `${Math.max(
                        8,
                        Math.round((stat.avgWords / maxWords) * 100)
                      )}%`,
                    }}
                  />
                </div>
                <div className="bar-value">{Math.round(stat.avgWords)}</div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Sentiment timeline</h2>
          <p className="panel-sub">
            Album-average sentiment (VADER compound) plotted against release
            year. This will evolve into the full Coldness Test and emotional
            trajectory overlays.
          </p>
        </div>
        <div className="timeline">
          <svg viewBox="0 0 820 260" role="img" aria-label="Album sentiment timeline">
            <g transform="translate(20, 20)">
              <line
                x1="40"
                y1="200"
                x2="800"
                y2="200"
                stroke="#1f2430"
                strokeWidth="1"
              />
              <line
                x1="40"
                y1="0"
                x2="40"
                y2="200"
                stroke="#1f2430"
                strokeWidth="1"
              />
              <polyline
                fill="none"
                stroke="#f472b6"
                strokeWidth="3"
                points={points.map((p) => `${p.x},${p.y}`).join(" ")}
              />
              {points.map((p) => (
                <g key={p.album}>
                  <circle cx={p.x} cy={p.y} r="6" fill={barColor(p.album)} />
                  <text x={p.x} y={p.y - 10} className="timeline-label">
                    {p.album}
                  </text>
                </g>
              ))}
            </g>
          </svg>
          <div className="timeline-meta">
            <div>
              <div className="stat-label">Sentiment range</div>
              <div className="stat-value">
                {minSent.toFixed(2)} to {maxSent.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="stat-label">Years</div>
              <div className="stat-value">
                {minYear}–{maxYear}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
