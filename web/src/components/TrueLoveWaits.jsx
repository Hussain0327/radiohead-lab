export default function TrueLoveWaits({ data }) {
  if (!data?.the_wait?.true_love_waits) return null;

  const tlw = data.the_wait.true_love_waits;
  const longWaiters = data.the_wait.long_waiters || [];
  const stats = data.the_wait.stats || {};

  // Timeline markers
  const timelineEvents = [
    { year: 1995, label: "First live performance", detail: "Clapham Grand, London" },
    { year: 1997, label: "OK Computer", detail: "Not included" },
    { year: 2000, label: "Kid A", detail: "Not included" },
    { year: 2001, label: "Amnesiac / I Might Be Wrong", detail: "Live version released" },
    { year: 2003, label: "Hail to the Thief", detail: "Not included" },
    { year: 2007, label: "In Rainbows", detail: "Not included" },
    { year: 2011, label: "The King of Limbs", detail: "Not included" },
    { year: 2016, label: "A Moon Shaped Pool", detail: "Finally released" },
  ];

  return (
    <section className="panel tlw-section">
      <div className="panel-header">
        <div>
          <h2>The Wait</h2>
          <p className="panel-sub">
            Some songs existed for years as live-only tracks before finally
            getting studio releases. True Love Waits holds the record.
          </p>
        </div>
      </div>

      {/* True Love Waits Hero */}
      <div className="tlw-hero">
        <div className="tlw-years">
          <span className="tlw-number">{Math.round(tlw.wait_years)}</span>
          <span className="tlw-unit">years</span>
        </div>
        <div className="tlw-story">
          <h3>True Love Waits</h3>
          <p className="tlw-dates">
            {tlw.first_live_year} live debut to {tlw.studio_release_year} studio release
          </p>
          <p className="tlw-context">{tlw.context}</p>
        </div>
      </div>

      {/* Timeline */}
      <div className="tlw-timeline">
        <div className="timeline-track">
          {timelineEvents.map((event, i) => {
            const isStart = i === 0;
            const isEnd = i === timelineEvents.length - 1;
            return (
              <div
                key={event.year}
                className={`timeline-point ${isStart ? 'start' : ''} ${isEnd ? 'end' : ''}`}
              >
                <div className="timeline-dot" />
                <div className="timeline-content">
                  <span className="timeline-year">{event.year}</span>
                  <span className="timeline-label">{event.label}</span>
                  <span className="timeline-detail">{event.detail}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Other Long Waiters */}
      <div className="long-waiters">
        <h4>Other Songs That Waited</h4>
        <div className="waiter-list">
          {longWaiters.slice(0, 6).map(song => (
            <div key={song.song} className="waiter-row">
              <div className="waiter-info">
                <span className="waiter-name">{song.song}</span>
                <span className="waiter-album">{song.studio_album}</span>
              </div>
              <div className="waiter-years">
                <span className="waiter-bar" style={{
                  width: `${Math.min(100, (song.wait_years / 25) * 100)}%`
                }} />
                <span className="waiter-value">{song.wait_years.toFixed(1)} years</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="tlw-stats">
        <div className="tlw-stat">
          <span className="stat-number">{stats.total_songs}</span>
          <span className="stat-desc">songs tracked</span>
        </div>
        <div className="tlw-stat">
          <span className="stat-number">{stats.songs_over_10_years}</span>
          <span className="stat-desc">waited 10+ years</span>
        </div>
        <div className="tlw-stat">
          <span className="stat-number">{stats.songs_over_20_years}</span>
          <span className="stat-desc">waited 20+ years</span>
        </div>
        <div className="tlw-stat">
          <span className="stat-number">{stats.mean_wait_years?.toFixed(1)}</span>
          <span className="stat-desc">avg wait (years)</span>
        </div>
      </div>
    </section>
  );
}
