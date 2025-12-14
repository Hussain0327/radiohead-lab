import { useState } from 'react';

export default function LyricAnalyzer({ data, palettes }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTrack, setSelectedTrack] = useState(null);

  if (!data?.tracks) return null;

  const standouts = data.standout_tracks || {};
  const lexical = data.lexical_evolution?.album_metrics || [];

  // Filter tracks by search
  const filteredTracks = searchTerm.length > 1
    ? data.tracks.filter(t =>
        t.track_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.album_name.toLowerCase().includes(searchTerm.toLowerCase())
      ).slice(0, 10)
    : [];

  const track = selectedTrack
    ? data.tracks.find(t => t.track_name === selectedTrack)
    : null;

  const trackPalette = track
    ? palettes[track.album_name]
    : null;

  return (
    <section className="panel analyzer-section">
      <div className="panel-header">
        <div>
          <h2>Lyric Analyzer</h2>
          <p className="panel-sub">
            Search for a song to see its emotional profile, or explore the
            standout tracks from the analysis.
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="Search for a song..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setSelectedTrack(null);
          }}
        />
        {filteredTracks.length > 0 && !selectedTrack && (
          <div className="search-results">
            {filteredTracks.map(t => (
              <button
                key={`${t.track_name}-${t.album_name}`}
                className="search-result"
                onClick={() => {
                  setSelectedTrack(t.track_name);
                  setSearchTerm(t.track_name);
                }}
              >
                <span className="result-track">{t.track_name}</span>
                <span className="result-album">{t.album_name}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Selected Track Analysis */}
      {track && (
        <div
          className="track-analysis"
          style={{
            '--track-color': trackPalette?.primary || 'var(--accent)',
            borderColor: trackPalette?.primary || 'var(--border)'
          }}
        >
          <div className="track-header">
            <div>
              <h3>{track.track_name}</h3>
              <p className="track-album-info">
                {track.album_name} ({track.album_year}) - {track.era} era
              </p>
            </div>
            <button
              className="close-btn"
              onClick={() => {
                setSelectedTrack(null);
                setSearchTerm('');
              }}
            >
              Close
            </button>
          </div>

          <div className="analysis-grid">
            {/* Emotions */}
            <div className="analysis-card">
              <h4>Emotion Profile</h4>
              <div className="emotion-bars">
                {['joy', 'sadness', 'anger', 'fear', 'trust', 'anticipation'].map(emotion => {
                  const value = track[`emotion_${emotion}`] || 0;
                  return (
                    <div key={emotion} className="emotion-row">
                      <span className="emotion-name">{emotion}</span>
                      <div className="emotion-bar-track">
                        <div
                          className="emotion-bar-fill"
                          style={{
                            width: `${value * 100}%`,
                            background: trackPalette?.primary || 'var(--accent)'
                          }}
                        />
                      </div>
                      <span className="emotion-value">{(value * 100).toFixed(1)}%</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Temperature */}
            <div className="analysis-card">
              <h4>Temperature</h4>
              <div className="temp-meter">
                <div className="temp-scale">
                  <span className="temp-cold">Cold</span>
                  <span className="temp-warm">Warm</span>
                </div>
                <div className="temp-bar-track">
                  <div
                    className="temp-marker"
                    style={{
                      left: `${50 + (track.coldness_index || 0) * 50}%`
                    }}
                  />
                </div>
                <div className="temp-values">
                  <div>
                    <span className="temp-label">Coldness</span>
                    <span className="temp-val">{((track.coldness || 0) * 100).toFixed(1)}%</span>
                  </div>
                  <div>
                    <span className="temp-label">Warmth</span>
                    <span className="temp-val">{((track.warmth || 0) * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Lexical Stats */}
            <div className="analysis-card">
              <h4>Lexical Profile</h4>
              <div className="stat-grid">
                <div className="stat-item">
                  <span className="stat-num">{track.word_count}</span>
                  <span className="stat-label">words</span>
                </div>
                <div className="stat-item">
                  <span className="stat-num">{track.unique_token_count}</span>
                  <span className="stat-label">unique</span>
                </div>
                <div className="stat-item">
                  <span className="stat-num">{(track.type_token_ratio * 100).toFixed(0)}%</span>
                  <span className="stat-label">diversity</span>
                </div>
                <div className="stat-item">
                  <span className="stat-num">{((track.emotional_intensity || 0) * 100).toFixed(0)}%</span>
                  <span className="stat-label">intensity</span>
                </div>
              </div>
            </div>
          </div>

          {/* Lyrics Preview */}
          <div className="lyrics-preview">
            <h4>Lyrics</h4>
            <p className="lyrics-text">
              {track.lyrics?.slice(0, 500)}
              {track.lyrics?.length > 500 && '...'}
            </p>
          </div>
        </div>
      )}

      {/* Standout Tracks */}
      {!selectedTrack && (
        <div className="standouts">
          <h4>Standout Tracks</h4>
          <div className="standout-grid">
            {Object.entries(standouts).map(([category, tracks]) => (
              <div key={category} className="standout-category">
                <h5>{category.replace(/_/g, ' ')}</h5>
                <div className="standout-list">
                  {tracks.slice(0, 3).map((t, i) => (
                    <button
                      key={t.track}
                      className="standout-item"
                      onClick={() => {
                        setSelectedTrack(t.track);
                        setSearchTerm(t.track);
                      }}
                    >
                      <span className="standout-rank">{i + 1}</span>
                      <span className="standout-track">{t.track}</span>
                      <span className="standout-album">{t.album}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Vocabulary Evolution */}
      <div className="vocab-evolution">
        <h4>Vocabulary Evolution</h4>
        <p className="vocab-desc">
          Type-token ratio measures lexical diversity. Higher means more unique
          words relative to total words.
        </p>
        <div className="vocab-chart">
          {lexical.map(album => (
            <div key={album.album} className="vocab-row">
              <span
                className="vocab-dot"
                style={{ background: palettes[album.album]?.primary }}
              />
              <span className="vocab-album">{album.album}</span>
              <div className="vocab-bar-track">
                <div
                  className="vocab-bar-fill"
                  style={{
                    width: `${album.avg_type_token_ratio * 100}%`,
                    background: palettes[album.album]?.primary || 'var(--accent)'
                  }}
                />
              </div>
              <span className="vocab-value">
                {(album.avg_type_token_ratio * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
