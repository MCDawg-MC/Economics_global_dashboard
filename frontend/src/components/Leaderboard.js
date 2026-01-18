import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getLeaderboard } from '../services/api';
import './Leaderboard.css';

function Leaderboard({ period = '1m', limit = 10 }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadLeaderboard();
  }, [period, limit]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const result = await getLeaderboard(period, limit);
      setData(result);
      setError(null);
    } catch (err) {
      setError('Failed to load leaderboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCountryClick = (countryCode) => {
    navigate(`/country/${countryCode}`);
  };

  if (loading) {
    return <div className="loading">Loading leaderboard...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!data) {
    return null;
  }

  const periodLabel = {
    '1m': '1 Month',
    '3m': '3 Months',
    '6m': '6 Months'
  }[period];

  return (
    <div className="leaderboard">
      <div className="leaderboard-section">
        <h3 className="leaderboard-title">
          🚀 Top Improvers ({periodLabel})
        </h3>
        {data.improvers && data.improvers.length > 0 ? (
          <div className="leaderboard-list">
            {data.improvers.map((country, index) => (
              <div
                key={country.country_code}
                className="leaderboard-item improver"
                onClick={() => handleCountryClick(country.country_code)}
              >
                <div className="rank">#{index + 1}</div>
                <div className="country-info">
                  <div className="country-name">{country.country_name}</div>
                  <div className="country-code">{country.country_code}</div>
                </div>
                <div className="score-info">
                  <div className="score">{country.momentum_score.toFixed(1)}</div>
                  <div className="change positive">
                    +{country.score_change.toFixed(1)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-data">No data available</div>
        )}
      </div>

      <div className="leaderboard-section">
        <h3 className="leaderboard-title">
          📉 Top Decliners ({periodLabel})
        </h3>
        {data.decliners && data.decliners.length > 0 ? (
          <div className="leaderboard-list">
            {data.decliners.map((country, index) => (
              <div
                key={country.country_code}
                className="leaderboard-item decliner"
                onClick={() => handleCountryClick(country.country_code)}
              >
                <div className="rank">#{index + 1}</div>
                <div className="country-info">
                  <div className="country-name">{country.country_name}</div>
                  <div className="country-code">{country.country_code}</div>
                </div>
                <div className="score-info">
                  <div className="score">{country.momentum_score.toFixed(1)}</div>
                  <div className="change negative">
                    {country.score_change.toFixed(1)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-data">No data available</div>
        )}
      </div>
    </div>
  );
}

export default Leaderboard;
