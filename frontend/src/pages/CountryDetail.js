import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getCountryDetail, getCountryHistory, getCountryIndicators } from '../services/api';
import './CountryDetail.css';

function CountryDetail() {
  const { countryCode } = useParams();
  const navigate = useNavigate();

  const [country, setCountry] = useState(null);
  const [history, setHistory] = useState(null);
  const [indicators, setIndicators] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCountryData();
  }, [countryCode]);

  const loadCountryData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [countryData, historyData, indicatorsData] = await Promise.all([
        getCountryDetail(countryCode),
        getCountryHistory(countryCode, 12),
        getCountryIndicators(countryCode)
      ]);

      setCountry(countryData);
      setHistory(historyData);
      setIndicators(indicatorsData);
    } catch (err) {
      setError('Failed to load country data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="country-detail">
        <div className="container">
          <div className="loading">Loading country data...</div>
        </div>
      </div>
    );
  }

  if (error || !country) {
    return (
      <div className="country-detail">
        <div className="container">
          <div className="error">{error || 'Country not found'}</div>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const timeSeriesData = history?.history?.map(item => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }),
    momentum: item.momentum_score,
    structural: item.structural_score,
    combined: item.combined_score
  })) || [];

  // Prepare radar data (pillar breakdown)
  const radarData = indicators?.indicators ? Object.entries(indicators.indicators).map(([code, data]) => ({
    indicator: data.indicator_name.substring(0, 20),
    value: data.percentile_rank || 0,
    pillar: data.pillar
  })) : [];

  // Group by pillar for simplified radar
  const pillarRadarData = radarData.reduce((acc, item) => {
    const existing = acc.find(p => p.pillar === item.pillar);
    if (existing) {
      existing.value = (existing.value + item.value) / 2;
      existing.count++;
    } else {
      acc.push({ pillar: item.pillar, value: item.value, count: 1 });
    }
    return acc;
  }, []);

  const classificationClass = country.latest_classification?.toLowerCase().replace(' ', '-') || '';

  return (
    <div className="country-detail">
      <div className="container">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Dashboard
        </button>

        <div className="country-header">
          <div className="country-title-section">
            <h1>{country.name}</h1>
            <div className="country-meta">
              <span className="country-code-badge">{country.code}</span>
              {country.region && <span className="meta-item">{country.region}</span>}
              {country.income_group && <span className="meta-item">{country.income_group}</span>}
            </div>
          </div>

          <div className="country-stats">
            <div className="stat-card">
              <div className="stat-label">Momentum Score</div>
              <div className="stat-value">{country.latest_momentum_score?.toFixed(1) || 'N/A'}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Global Rank</div>
              <div className="stat-value">#{country.global_rank || 'N/A'}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Classification</div>
              <div className={`stat-badge ${classificationClass}`}>
                {country.latest_classification || 'N/A'}
              </div>
            </div>
          </div>
        </div>

        <div className="charts-grid">
          <div className="card chart-card">
            <h3 className="card-title">Momentum Score History (12 Months)</h3>
            {timeSeriesData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="momentum" stroke="#1976d2" strokeWidth={2} name="Momentum Score" />
                  {timeSeriesData[0]?.structural && (
                    <Line type="monotone" dataKey="structural" stroke="#66bb6a" strokeWidth={2} name="Structural Score" />
                  )}
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="no-data">No historical data available</div>
            )}
          </div>

          <div className="card chart-card">
            <h3 className="card-title">Pillar Breakdown</h3>
            {pillarRadarData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={pillarRadarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="pillar" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name="Percentile Score" dataKey="value" stroke="#1976d2" fill="#1976d2" fillOpacity={0.6} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <div className="no-data">No indicator data available</div>
            )}
          </div>
        </div>

        <div className="card indicators-card">
          <h3 className="card-title">Latest Indicator Values</h3>
          {indicators?.indicators && Object.keys(indicators.indicators).length > 0 ? (
            <div className="indicators-table">
              <div className="indicators-header">
                <div>Indicator</div>
                <div>Pillar</div>
                <div>Value</div>
                <div>Percentile</div>
              </div>
              {Object.entries(indicators.indicators).map(([code, data]) => (
                <div key={code} className="indicator-row">
                  <div className="indicator-name">{data.indicator_name}</div>
                  <div className="indicator-pillar">{data.pillar.replace('_', ' ')}</div>
                  <div className="indicator-value">
                    {data.raw_value?.toFixed(2)} {data.unit}
                  </div>
                  <div className="indicator-percentile">
                    <div className="percentile-bar">
                      <div
                        className="percentile-fill"
                        style={{ width: `${data.percentile_rank || 0}%` }}
                      />
                    </div>
                    <span>{data.percentile_rank?.toFixed(0) || 0}%</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No indicator data available</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CountryDetail;
