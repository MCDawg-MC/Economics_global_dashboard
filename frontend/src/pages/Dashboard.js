import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MomentumMap from '../components/MomentumMap';
import Leaderboard from '../components/Leaderboard';
import './Dashboard.css';

function Dashboard() {
  const [includeStructural, setIncludeStructural] = useState(false);
  const [period, setPeriod] = useState('1m');
  const navigate = useNavigate();

  const handleCountryClick = (countryCode) => {
    navigate(`/country/${countryCode}`);
  };

  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <div>
            <h2>Global Momentum Dashboard</h2>
            <p className="dashboard-subtitle">
              Real-time economic momentum tracking across countries
            </p>
          </div>
          <div className="dashboard-controls">
            <div className="control-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={includeStructural}
                  onChange={(e) => setIncludeStructural(e.target.checked)}
                />
                <span>Include Structural Score</span>
              </label>
            </div>
            <div className="control-group">
              <label>Time Period:</label>
              <select
                value={period}
                onChange={(e) => setPeriod(e.target.value)}
                className="period-select"
              >
                <option value="1m">1 Month</option>
                <option value="3m">3 Months</option>
                <option value="6m">6 Months</option>
              </select>
            </div>
          </div>
        </div>

        <div className="map-section card">
          <h3 className="card-title">World Map</h3>
          <MomentumMap
            includeStructural={includeStructural}
            onCountryClick={handleCountryClick}
          />
        </div>

        <div className="leaderboard-section">
          <h3 className="section-title">Top Movers</h3>
          <Leaderboard period={period} limit={10} />
        </div>

        <div className="info-section card">
          <h3 className="card-title">About the Country Momentum Index</h3>
          <div className="info-content">
            <p>
              The Country Momentum Index (CMI) measures economic momentum, not static levels.
              It captures the <strong>direction and acceleration</strong> of economies across
              five key pillars:
            </p>
            <div className="pillars-grid">
              <div className="pillar">
                <h4>🌐 External Sector (25%)</h4>
                <p>FX momentum, reserves, export growth</p>
              </div>
              <div className="pillar">
                <h4>💰 Inflation & Prices (20%)</h4>
                <p>CPI and core CPI acceleration</p>
              </div>
              <div className="pillar">
                <h4>🏭 Real Activity (20%)</h4>
                <p>Industrial production, PMI</p>
              </div>
              <div className="pillar">
                <h4>🏦 Monetary & Financial (20%)</h4>
                <p>Policy rates, credit growth</p>
              </div>
              <div className="pillar">
                <h4>📚 Structural (15%)</h4>
                <p>Education, industry, diversification</p>
              </div>
            </div>
            <p className="info-note">
              Data sources: IMF, World Bank, OECD, BIS, FRED, UNDP. Updated monthly.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
