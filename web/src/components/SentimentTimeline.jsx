const ALBUM_ORDER = [
  "Pablo Honey",
  "The Bends",
  "OK Computer",
  "Kid A",
  "Amnesiac",
  "Hail to the Thief",
  "In Rainbows",
  "The King of Limbs",
  "A Moon Shaped Pool"
];

export default function SentimentTimeline({ data, palettes }) {
  if (!data?.albums) return null;

  const albums = ALBUM_ORDER
    .map(name => data.albums.find(a => a.album === name))
    .filter(Boolean);

  // Get hypothesis test results
  const h1 = data.hypothesis_tests?.h1_coldness_test;
  const h4 = data.hypothesis_tests?.h4_in_rainbows_test;

  // SVG dimensions
  const width = 800;
  const height = 300;
  const padding = { top: 40, right: 40, bottom: 60, left: 60 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  // Scales
  const years = albums.map(a => a.year);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);

  const coldnessValues = albums.map(a => a.avg_coldness_index || 0);
  const minCold = Math.min(...coldnessValues, -1);
  const maxCold = Math.max(...coldnessValues, 1);

  const xScale = (year) =>
    padding.left + ((year - minYear) / (maxYear - minYear)) * chartWidth;
  const yScale = (value) =>
    padding.top + chartHeight - ((value - minCold) / (maxCold - minCold)) * chartHeight;

  // Build path
  const pathPoints = albums
    .map(a => `${xScale(a.year)},${yScale(a.avg_coldness_index || 0)}`)
    .join(' ');

  return (
    <section className="panel sentiment-section">
      <div className="panel-header">
        <div>
          <h2>The Coldness Test</h2>
          <p className="panel-sub">
            H1: Kid A's "coldness" is overstated. Testing whether the lyrics
            actually got colder, or if critics projected the electronic
            production onto the words.
          </p>
        </div>
      </div>

      {/* Hypothesis Result */}
      {h1 && (
        <div className={`hypothesis-result ${h1.results?.significant_05 ? 'challenges' : 'supports'}`}>
          <div className="hypothesis-verdict">
            {h1.results?.significant_05 ? 'CHALLENGES' : 'SUPPORTS'} H1
          </div>
          <div className="hypothesis-detail">
            <p>{h1.interpretation}</p>
            <div className="hypothesis-stats">
              <span>Effect size: {h1.effect_size_cohens_d} ({h1.effect_interpretation})</span>
              <span>p-value: {h1.results?.p_value}</span>
            </div>
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="coldness-chart">
        <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Coldness index by album">
          {/* Zero line */}
          <line
            x1={padding.left}
            y1={yScale(0)}
            x2={width - padding.right}
            y2={yScale(0)}
            stroke="#374151"
            strokeWidth="1"
            strokeDasharray="4,4"
          />
          <text
            x={padding.left - 10}
            y={yScale(0)}
            textAnchor="end"
            className="axis-label"
            fill="#6b7280"
          >
            0 (neutral)
          </text>

          {/* Labels */}
          <text
            x={padding.left - 10}
            y={yScale(minCold)}
            textAnchor="end"
            className="axis-label"
            fill="#60a5fa"
          >
            Warmer
          </text>
          <text
            x={padding.left - 10}
            y={yScale(maxCold)}
            textAnchor="end"
            className="axis-label"
            fill="#ef4444"
          >
            Colder
          </text>

          {/* Line */}
          <polyline
            fill="none"
            stroke="#f472b6"
            strokeWidth="3"
            points={pathPoints}
          />

          {/* Points */}
          {albums.map(album => {
            const x = xScale(album.year);
            const y = yScale(album.avg_coldness_index || 0);
            const color = palettes[album.album]?.primary || '#fff';

            return (
              <g key={album.album}>
                <circle
                  cx={x}
                  cy={y}
                  r="8"
                  fill={color}
                  stroke="#0f1115"
                  strokeWidth="2"
                />
                <text
                  x={x}
                  y={y - 15}
                  textAnchor="middle"
                  className="chart-label"
                  fill="#e5e7eb"
                  fontSize="11"
                >
                  {album.album.replace('A Moon Shaped Pool', 'AMSP')}
                </text>
                <text
                  x={x}
                  y={height - 20}
                  textAnchor="middle"
                  className="year-label"
                  fill="#6b7280"
                  fontSize="10"
                >
                  {album.year}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Coldness by Album Table */}
      <div className="coldness-table">
        <h4>Coldness Index by Album</h4>
        <div className="coldness-rows">
          {albums.map(album => {
            const coldness = album.avg_coldness_index || 0;
            const warmth = album.avg_warmth || 0;
            const isWarm = coldness < 0;

            return (
              <div key={album.album} className="coldness-row">
                <span
                  className="album-dot"
                  style={{ background: palettes[album.album]?.primary }}
                />
                <span className="coldness-album">{album.album}</span>
                <div className="coldness-bar-container">
                  <div
                    className={`coldness-bar ${isWarm ? 'warm' : 'cold'}`}
                    style={{
                      width: `${Math.abs(coldness) * 50}%`,
                      marginLeft: isWarm ? `${50 - Math.abs(coldness) * 50}%` : '50%'
                    }}
                  />
                </div>
                <span className="coldness-value">
                  {coldness > 0 ? '+' : ''}{coldness.toFixed(2)}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* In Rainbows Outlier Test */}
      {h4 && (
        <div className="h4-section">
          <h4>H4: In Rainbows as Outlier</h4>
          <p className="h4-desc">
            Testing whether In Rainbows represents a larger emotional shift
            than Kid A. The warmth and joy metrics suggest it was a deliberate
            return to directness.
          </p>
          <div className="warmth-comparison">
            {Object.entries(h4.warmth_by_album || {}).map(([album, warmth]) => (
              <div key={album} className="warmth-row">
                <span className="warmth-album">{album}</span>
                <div className="warmth-bar-track">
                  <div
                    className="warmth-bar-fill"
                    style={{
                      width: `${warmth * 500}%`,
                      background: palettes[album]?.primary || '#fff'
                    }}
                  />
                </div>
                <span className="warmth-value">{(warmth * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
