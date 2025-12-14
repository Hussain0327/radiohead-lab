import { useState } from 'react';

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

export default function AlbumExplorer({ data, palettes }) {
  const [selectedAlbum, setSelectedAlbum] = useState(null);

  if (!data?.albums) return null;

  const albums = ALBUM_ORDER
    .map(name => data.albums.find(a => a.album === name))
    .filter(Boolean);

  const selected = selectedAlbum
    ? data.albums.find(a => a.album === selectedAlbum)
    : null;

  const palette = selected
    ? palettes[selected.album]
    : palettes["OK Computer"];

  const tracks = selected
    ? data.tracks.filter(t => t.album_name === selected.album)
    : [];

  return (
    <section className="panel album-explorer">
      <div className="panel-header">
        <div>
          <h2>Album Explorer</h2>
          <p className="panel-sub">
            Click an album to explore its tracks. Colors shift to match
            Stanley Donwood's artwork for each era.
          </p>
        </div>
      </div>

      <div className="album-grid">
        {albums.map(album => (
          <button
            key={album.album}
            className={`album-card ${selectedAlbum === album.album ? 'active' : ''}`}
            onClick={() => setSelectedAlbum(
              selectedAlbum === album.album ? null : album.album
            )}
            style={{
              '--album-color': palettes[album.album]?.primary || '#fff',
              borderColor: selectedAlbum === album.album
                ? palettes[album.album]?.primary
                : 'var(--border)'
            }}
          >
            <div className="album-year">{album.year}</div>
            <div className="album-name">{album.album}</div>
            <div className="album-era">{album.era}</div>
            <div className="album-stats">
              {album.track_count} tracks
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div
          className="album-detail"
          style={{
            '--detail-bg': palette?.background || 'var(--panel)',
            '--detail-primary': palette?.primary || 'var(--accent)',
            '--detail-text': palette?.text || 'var(--text)'
          }}
        >
          <div className="detail-header">
            <div>
              <span className="detail-year">{selected.year}</span>
              <h3>{selected.album}</h3>
              <p className="detail-desc">{palette?.description}</p>
            </div>
            <div className="detail-metrics">
              <div className="metric">
                <span className="metric-value">
                  {selected.avg_sentiment_score?.toFixed(3) || '0.000'}
                </span>
                <span className="metric-label">Sentiment</span>
              </div>
              <div className="metric">
                <span className="metric-value">
                  {selected.avg_coldness_index?.toFixed(2) || '0.00'}
                </span>
                <span className="metric-label">Coldness</span>
              </div>
              <div className="metric">
                <span className="metric-value">
                  {(selected.avg_emotional_intensity * 100)?.toFixed(1) || '0.0'}%
                </span>
                <span className="metric-label">Intensity</span>
              </div>
            </div>
          </div>

          <div className="track-list">
            {tracks.map(track => (
              <div key={track.track_name} className="track-row">
                <div className="track-name">{track.track_name}</div>
                <div className="track-metrics">
                  <span
                    className="emotion-bar"
                    style={{
                      width: `${Math.max(5, track.emotional_intensity * 100)}%`,
                      background: palette?.primary || 'var(--accent)'
                    }}
                  />
                  <span className="track-words">{track.word_count} words</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
