import { useState } from 'react';
import data from './data/radiohead_web_data.json';
import './styles/donwood.css';

import AlbumExplorer from './components/AlbumExplorer';
import SentimentTimeline from './components/SentimentTimeline';
import LyricAnalyzer from './components/LyricAnalyzer';
import TrueLoveWaits from './components/TrueLoveWaits';
import ReunionTour2025 from './components/ReunionTour2025';

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview' },
  { id: 'albums', label: 'Albums' },
  { id: 'coldness', label: 'Coldness Test' },
  { id: 'analyzer', label: 'Lyric Analyzer' },
  { id: 'wait', label: 'The Wait' },
  { id: 'tour', label: '2025 Tour' },
];

export default function App() {
  const [activeSection, setActiveSection] = useState('overview');

  const palettes = data?.donwood_palettes || {};
  const meta = data?.meta || {};
  const albums = data?.albums || [];
  const h1 = data?.hypothesis_tests?.h1_coldness_test;

  // Overview stats
  const maxWords = Math.max(...albums.map(a => a.avg_word_count || 0), 1);

  return (
    <div className="app-shell">
      {/* Navigation */}
      <nav className="nav-bar">
        {NAV_ITEMS.map(item => (
          <button
            key={item.id}
            className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
            onClick={() => setActiveSection(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      {/* Hero */}
      <header className="hero">
        <div>
          <p className="eyebrow">Radiohead Data Lab</p>
          <h1>Exploring the Myths of Musical Evolution</h1>
          <p className="lede">
            Did Radiohead's lyrics actually get "colder" after OK Computer?
            Is Kid A the pivot point, or is In Rainbows the outlier?
            What does it mean to wait 21 years for True Love Waits?
          </p>
        </div>
        <div className="hero-stats">
          <div className="pill">{meta.total_tracks} tracks</div>
          <div className="pill">{meta.total_albums} albums</div>
          <div className="pill">{meta.years_span}</div>
        </div>
      </header>

      {/* Overview Section */}
      {activeSection === 'overview' && (
        <>
          <section className="panel">
            <div className="panel-header">
              <div>
                <h2>The Hypotheses</h2>
                <p className="panel-sub">
                  This project tests four hypotheses about Radiohead's lyrical evolution
                  using NLP analysis and statistical testing.
                </p>
              </div>
            </div>
            <div className="hypothesis-grid">
              <div className="hypothesis-card">
                <span className="h-label">H1</span>
                <h3>The Coldness Narrative is Overstated</h3>
                <p>Kid A's reputation as emotionally distant may be driven by production, not lyrics.</p>
                {h1 && (
                  <span className={`verdict ${h1.results?.significant_05 ? 'challenge' : 'support'}`}>
                    {h1.results?.significant_05 ? 'Challenged' : 'Supported'}
                  </span>
                )}
              </div>
              <div className="hypothesis-card">
                <span className="h-label">H2</span>
                <h3>Fragmentation, Not Negativity</h3>
                <p>Later lyrics feel different because they're structurally fragmented, not sadder.</p>
              </div>
              <div className="hypothesis-card">
                <span className="h-label">H3</span>
                <h3>Thematic Continuity</h3>
                <p>Core concerns (technology, isolation, identity) remain stable across eras.</p>
              </div>
              <div className="hypothesis-card">
                <span className="h-label">H4</span>
                <h3>In Rainbows is the Outlier</h3>
                <p>Not Kid A - In Rainbows represents the larger emotional shift.</p>
              </div>
            </div>
          </section>

          <section className="panel">
            <div className="panel-header">
              <div>
                <h2>Average Words Per Track</h2>
                <p className="panel-sub">
                  Bars scaled to the wordiest album. Colors from Stanley Donwood's artwork.
                </p>
              </div>
            </div>
            <div className="bar-list">
              {albums.map(album => (
                <div className="bar-row" key={album.album}>
                  <div className="bar-meta">
                    <div className="bar-title">
                      {album.album}
                      <span className="era">{album.era}</span>
                    </div>
                    <div className="bar-sub">
                      {album.year} - {album.track_count} tracks
                    </div>
                  </div>
                  <div className="bar-shell">
                    <div
                      className="bar-fill"
                      style={{
                        background: palettes[album.album]?.primary || '#f472b6',
                        width: `${Math.max(8, (album.avg_word_count / maxWords) * 100)}%`
                      }}
                    />
                  </div>
                  <div className="bar-value">{Math.round(album.avg_word_count || 0)}</div>
                </div>
              ))}
            </div>
          </section>
        </>
      )}

      {/* Album Explorer */}
      {activeSection === 'albums' && (
        <AlbumExplorer data={data} palettes={palettes} />
      )}

      {/* Coldness Test */}
      {activeSection === 'coldness' && (
        <SentimentTimeline data={data} palettes={palettes} />
      )}

      {/* Lyric Analyzer */}
      {activeSection === 'analyzer' && (
        <LyricAnalyzer data={data} palettes={palettes} />
      )}

      {/* The Wait / True Love Waits */}
      {activeSection === 'wait' && (
        <TrueLoveWaits data={data} />
      )}

      {/* 2025 Tour */}
      {activeSection === 'tour' && (
        <ReunionTour2025 data={data} />
      )}

      {/* Footer */}
      <footer className="footer">
        <p>
          Built as a tribute to Radiohead's 2025 reunion.
          Data from Kaggle lyrics dataset. For educational purposes only.
        </p>
      </footer>
    </div>
  );
}
