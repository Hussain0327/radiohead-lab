export default function ReunionTour2025({ data }) {
  if (!data?.tour_2025) return null;

  const tour = data.tour_2025;
  const info = tour.tour_info || {};
  const topSongs = tour.top_songs || [];
  const eraDist = tour.era_distribution?.by_era || {};
  const tlw = tour.true_love_waits || {};
  const completeAlbums = tour.complete_album_shows || [];

  const eraOrder = ["Early", "Peak", "Reinvention", "Middle", "Late"];
  const eraColors = {
    "Early": "#f97316",
    "Peak": "#60a5fa",
    "Reinvention": "#ef4444",
    "Middle": "#f59e0b",
    "Late": "#9ca3af"
  };

  return (
    <section className="panel tour-section">
      <div className="panel-header">
        <div>
          <h2>2025 Reunion Tour</h2>
          <p className="panel-sub">
            After seven years of silence, Radiohead returned to the stage.
            Here's what they played.
          </p>
        </div>
        <div className="pill">
          {info.total_shows} shows
        </div>
      </div>

      {/* Tour Overview */}
      <div className="tour-hero">
        <div className="tour-stat-grid">
          <div className="tour-stat">
            <span className="tour-number">7</span>
            <span className="tour-label">years since last show</span>
          </div>
          <div className="tour-stat">
            <span className="tour-number">{info.song_pool || 65}</span>
            <span className="tour-label">songs in rotation</span>
          </div>
          <div className="tour-stat">
            <span className="tour-number">{tlw.appearance_rate || 100}%</span>
            <span className="tour-label">shows with True Love Waits</span>
          </div>
        </div>
        <p className="tour-context">{info.notes}</p>
      </div>

      {/* Era Distribution */}
      <div className="era-distribution">
        <h4>Songs by Era</h4>
        <div className="era-bars">
          {eraOrder.map(era => {
            const eraData = eraDist[era];
            if (!eraData) return null;
            return (
              <div key={era} className="era-bar-row">
                <span className="era-name" style={{ color: eraColors[era] }}>
                  {era}
                </span>
                <div className="era-bar-track">
                  <div
                    className="era-bar-fill"
                    style={{
                      width: `${eraData.percentage}%`,
                      background: eraColors[era]
                    }}
                  />
                </div>
                <span className="era-pct">{eraData.percentage}%</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Top Songs */}
      <div className="top-songs">
        <h4>Most Played Songs</h4>
        <div className="song-grid">
          {topSongs.slice(0, 10).map((item, i) => (
            <div key={item.song} className="song-card">
              <span className="song-rank">{i + 1}</span>
              <div className="song-info">
                <span className="song-title">{item.song}</span>
                <span className="song-appearances">
                  {item.appearances} shows
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Complete Album Shows */}
      {completeAlbums.length > 0 && (
        <div className="complete-albums">
          <h4>Full Album Performances</h4>
          <div className="album-show-list">
            {completeAlbums.map(show => (
              <div key={show.date} className="album-show">
                <span className="show-date">{show.date}</span>
                <span className="show-city">{show.city}</span>
                <span className="show-album">{show.album}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Interpretation */}
      <div className="tour-interpretation">
        <p>{tour.interpretation}</p>
      </div>
    </section>
  );
}
