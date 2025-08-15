import React, { useMemo, useState, useEffect } from 'react';
import {
  AreaChart, Area, Line, LineChart,
  CartesianGrid, XAxis, YAxis, Tooltip, Legend,
  ResponsiveContainer, PieChart, Pie, Cell,
  ScatterChart, Scatter, ZAxis
} from 'recharts';
import './NextGenAnalyticsPage.css';

const neon = {
  primary: '#7C3AED', // violet-600
  primaryGlow: '#8B5CF6',
  cyan: '#00D9FF',
  coral: '#FF6B6B',
  gold: '#FFD93D',
  bg: '#0F1419',
  grid: 'rgba(255,255,255,0.12)'
};

const NextGenAnalyticsPage = () => {
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('overview');
  const [timeRange, setTimeRange] = useState('6m');
  const [selectedGrade, setSelectedGrade] = useState(null);
  const [search, setSearch] = useState('');
  const [filtersOpen, setFiltersOpen] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 900);
    return () => clearTimeout(timer);
  }, []);

  // Mock data
  const trendData = useMemo(() => (
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
      .slice(0, timeRange === '3m' ? 3 : timeRange === '6m' ? 6 : 12)
      .map((m, i) => ({ month: m, score: 70 + Math.sin(i/2)*8 + i*0.8 }))
  ), [timeRange]);

  const grades = [
    { name: 'A+', value: 14 }, { name: 'A', value: 24 }, { name: 'A-', value: 18 },
    { name: 'B+', value: 16 }, { name: 'B', value: 12 }, { name: 'B-', value: 8 },
    { name: 'C+', value: 5 }, { name: 'C', value: 3 }
  ];

  const subjects = [
    { subject: 'Mathematics', overall: 85, classAvg: 79 },
    { subject: 'Physics', overall: 80, classAvg: 76 },
    { subject: 'Chemistry', overall: 82, classAvg: 78 },
    { subject: 'Computer Science', overall: 90, classAvg: 84 },
    { subject: 'English', overall: 75, classAvg: 72 }
  ];

  const improvBubbles = [
    { x: 60, y: 70, z: 1200, name: 'Math' },
    { x: 65, y: 64, z: 900, name: 'Physics' },
    { x: 72, y: 76, z: 700, name: 'Chem' },
    { x: 80, y: 78, z: 600, name: 'CS' },
    { x: 58, y: 62, z: 1000, name: 'English' },
  ];

  const filteredGrades = useMemo(() => (
    grades.filter(g => !selectedGrade || g.name === selectedGrade)
  ), [grades, selectedGrade]);

  const gradeColors = [neon.cyan, neon.primaryGlow, neon.gold, neon.coral, '#60A5FA', '#A78BFA', '#22C55E', '#F472B6'];

  return (
    <div className="nextgen-root">
      <div className="nextgen-particles" aria-hidden="true" />

      <header className="nextgen-header">
        <div className="title-wrap">
          <h1 className="title">
            <span role="img" aria-label="chart">📊</span> Next‑Gen Analytics
          </h1>
          <p className="subtitle">Premium performance intelligence with a futuristic touch</p>
        </div>
        <div className="header-actions">
          <div className="time-range">
            <label htmlFor="range" className="sr-only">Time range</label>
            <select id="range" value={timeRange} onChange={e=>setTimeRange(e.target.value)} className="glass-select">
              <option value="3m">Last 3 months</option>
              <option value="6m">Last 6 months</option>
              <option value="12m">Last 12 months</option>
            </select>
          </div>
          <button className="btn glass" onClick={()=>setFiltersOpen(true)} aria-expanded={filtersOpen}>Filters</button>
          <button className="btn primary" onClick={()=>window.location.reload()}>
            <span className="spinner" /> Refresh
          </button>
        </div>
      </header>

      <nav className="tabs" role="tablist" aria-label="Analytics views">
        {['overview','distribution','improvement'].map(t => (
          <button
            key={t}
            role="tab"
            aria-selected={selectedTab===t}
            className={`tab ${selectedTab===t?'active':''}`}
            onClick={()=>setSelectedTab(t)}
          >{t === 'overview' ? 'Overview' : t === 'distribution' ? 'Grade Distribution' : 'Areas for Improvement'}</button>
        ))}
        <span className="tab-indicator" style={{ transform: `translateX(${['overview','distribution','improvement'].indexOf(selectedTab)*100}%)` }} />
      </nav>

      <main className="grid">
        {/* Performance Trend */}
        <section className="card glass fade-in" aria-live="polite">
          <div className="card-head">
            <h2>Performance Trend</h2>
            <span className="badge">Live</span>
          </div>
          <div className="chart-wrap">
            {loading ? (
              <div className="skeleton" />
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={trendData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="gradLine" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={neon.primaryGlow} stopOpacity={0.55} />
                      <stop offset="100%" stopColor={neon.primaryGlow} stopOpacity={0.05} />
                    </linearGradient>
                    <filter id="glow" height="300%" width="300%" x="-75%" y="-75%">
                      <feGaussianBlur stdDeviation="6" result="coloredBlur" />
                      <feMerge>
                        <feMergeNode in="coloredBlur" />
                        <feMergeNode in="SourceGraphic" />
                      </feMerge>
                    </filter>
                  </defs>
                  <CartesianGrid stroke={neon.grid} vertical={false} />
                  <XAxis dataKey="month" tick={{ fill: '#E5E7EB' }} axisLine={{ stroke: neon.grid }} tickLine={{ stroke: neon.grid }} />
                  <YAxis domain={[60, 100]} tick={{ fill: '#E5E7EB' }} axisLine={{ stroke: neon.grid }} tickLine={{ stroke: neon.grid }} />
                  <Tooltip contentStyle={{ background: 'rgba(17,24,39,0.85)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 12, color: '#E5E7EB', backdropFilter: 'blur(10px)' }} />
                  <Area type="monotone" dataKey="score" stroke={neon.primaryGlow} strokeWidth={3} filter="url(#glow)" fill="url(#gradLine)" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </section>

        {/* Top Performers Rings and Distribution */}
        <section className="card glass fade-in delay-1">
          <div className="card-head">
            <h2>Grade Distribution</h2>
            {selectedGrade && <button className="chip" onClick={()=>setSelectedGrade(null)}>Clear: {selectedGrade} ✕</button>}
          </div>
          <div className="chart-wrap">
            {loading ? (
              <div className="skeleton" />
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie data={filteredGrades} dataKey="value" nameKey="name" innerRadius={60} outerRadius={100} paddingAngle={2} onClick={(d)=>setSelectedGrade(d?.name)}>
                    {filteredGrades.map((entry, i) => (
                      <Cell key={`c-${i}`} fill={gradeColors[i % gradeColors.length]} stroke="rgba(255,255,255,0.2)" strokeWidth={1} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ background: 'rgba(17,24,39,0.85)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 12, color: '#E5E7EB', backdropFilter: 'blur(10px)' }} />
                  <Legend wrapperStyle={{ color: '#E5E7EB' }} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        </section>

        {/* Areas for Improvement Bubble Chart */}
        <section className="card glass fade-in delay-2">
          <div className="card-head">
            <h2>Areas for Improvement</h2>
            <span className="hint">Impact vs Effort</span>
          </div>
          <div className="chart-wrap">
            {loading ? (
              <div className="skeleton" />
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <ScatterChart margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <CartesianGrid stroke={neon.grid} />
                  <XAxis type="number" dataKey="x" name="Impact" tick={{ fill: '#E5E7EB' }} axisLine={{ stroke: neon.grid }} tickLine={{ stroke: neon.grid }} />
                  <YAxis type="number" dataKey="y" name="Effort" tick={{ fill: '#E5E7EB' }} axisLine={{ stroke: neon.grid }} tickLine={{ stroke: neon.grid }} />
                  <ZAxis type="number" dataKey="z" range={[80, 320]} />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ background: 'rgba(17,24,39,0.85)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 12, color: '#E5E7EB', backdropFilter: 'blur(10px)' }} />
                  <Scatter data={improvBubbles} fill={neon.coral} stroke={neon.coral} opacity={0.9} />
                </ScatterChart>
              </ResponsiveContainer>
            )}
          </div>
        </section>

        {/* Subject cards */}
        <section className="card glass span-2 fade-in delay-3">
          <div className="card-head">
            <h2>Subject Comparison</h2>
            <input aria-label="Search subjects" className="glass-input" placeholder="Search subjects…" value={search} onChange={e=>setSearch(e.target.value)} />
          </div>
          <div className="subjects-grid">
            {subjects.filter(s => s.subject.toLowerCase().includes(search.toLowerCase())).map((s) => {
              const diff = (s.overall - s.classAvg).toFixed(1);
              const positive = parseFloat(diff) >= 0;
              return (
                <div key={s.subject} className="subject-card" role="article" aria-label={`${s.subject} card`}>
                  <div className="subject-head">
                    <h3>{s.subject}</h3>
                    <span className={`delta ${positive? 'up':'down'}`}>{positive? '⬆️' : '⬇️'} {Math.abs(diff)}%</span>
                  </div>
                  <div className="bars">
                    <div className="bar"><span>Student</span><div className="track"><div className="fill student" style={{ width: `${s.overall}%` }} /></div><strong>{s.overall}%</strong></div>
                    <div className="bar"><span>Class Avg</span><div className="track"><div className="fill class" style={{ width: `${s.classAvg}%` }} /></div><strong>{s.classAvg}%</strong></div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </main>

      {/* Slide-out Filters Panel */}
      <aside className={`filters ${filtersOpen? 'open':''}`} aria-hidden={!filtersOpen}>
        <div className="filters-head">
          <h3>Filters</h3>
          <button className="btn ghost" onClick={()=>setFiltersOpen(false)}>Close ✕</button>
        </div>
        <div className="filters-body">
          <label className="label">Grades</label>
          <div className="chips">
            {['A+','A','A-','B+','B','B-','C+','C'].map(g => (
              <button key={g} className={`chip ${selectedGrade===g? 'active':''}`} onClick={()=>setSelectedGrade(selectedGrade===g? null : g)}>{g}</button>
            ))}
          </div>
          <label className="label">Time Range</label>
          <div className="chips">
            {['3m','6m','12m'].map(r => (
              <button key={r} className={`chip ${timeRange===r? 'active':''}`} onClick={()=>setTimeRange(r)}>{r}</button>
            ))}
          </div>
        </div>
      </aside>
    </div>
  );
};

export default NextGenAnalyticsPage;
