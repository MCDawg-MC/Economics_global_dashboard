import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Countries API
export const getCountries = async () => {
  const response = await api.get('/countries');
  return response.data;
};

export const getCountryDetail = async (countryCode) => {
  const response = await api.get(`/countries/${countryCode}`);
  return response.data;
};

export const getCountryHistory = async (countryCode, months = 12) => {
  const response = await api.get(`/countries/${countryCode}/momentum-history`, {
    params: { months }
  });
  return response.data;
};

// Momentum API
export const getLatestScores = async () => {
  const response = await api.get('/momentum/latest');
  return response.data;
};

export const getLeaderboard = async (period = '1m', limit = 10) => {
  const response = await api.get('/momentum/leaderboard', {
    params: { period, limit }
  });
  return response.data;
};

export const getMapData = async (includeStructural = false) => {
  const response = await api.get('/momentum/map-data', {
    params: { include_structural: includeStructural }
  });
  return response.data;
};

// Indicators API
export const getIndicators = async () => {
  const response = await api.get('/indicators');
  return response.data;
};

export const getCountryIndicators = async (countryCode) => {
  const response = await api.get(`/indicators/${countryCode}/latest`);
  return response.data;
};

export const refreshData = async () => {
  const response = await api.post('/indicators/refresh');
  return response.data;
};

export default api;
