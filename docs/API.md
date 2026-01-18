## Country Momentum Index API Documentation

API endpoints for the Country Momentum Index application.

Base URL: `http://localhost:8000/api/v1`

## Authentication

Currently, the API is open. In production, implement authentication for protected endpoints.

## Endpoints

### Health Check

```
GET /health
```

Returns API health status.

**Response**:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### Countries

#### Get All Countries

```
GET /api/v1/countries
```

Returns list of all countries.

**Query Parameters**:
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum number of records (default: 100)

**Response**:
```json
[
  {
    "code": "USA",
    "name": "United States",
    "region": "North America",
    "income_group": "High income",
    "latitude": 37.09,
    "longitude": -95.71,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Country Detail

```
GET /api/v1/countries/{country_code}
```

Returns detailed information for a specific country.

**Response**:
```json
{
  "code": "USA",
  "name": "United States",
  "latest_momentum_score": 75.5,
  "latest_classification": "Improving",
  "global_rank": 5
}
```

#### Get Country Momentum History

```
GET /api/v1/countries/{country_code}/momentum-history
```

Returns historical momentum scores.

**Query Parameters**:
- `months` (int): Number of months of history (default: 12)

**Response**:
```json
{
  "country_code": "USA",
  "history": [
    {
      "date": "2024-01-01",
      "momentum_score": 75.5,
      "classification": "Improving"
    }
  ]
}
```

---

### Momentum Scores

#### Get Latest Scores

```
GET /api/v1/momentum/latest
```

Returns latest momentum scores for all countries.

**Response**:
```json
[
  {
    "country_code": "USA",
    "date": "2024-01-01",
    "momentum_score": 75.5,
    "structural_score": 85.0,
    "combined_score": 78.0,
    "classification": "Improving",
    "global_rank": 5
  }
]
```

#### Get Leaderboard

```
GET /api/v1/momentum/leaderboard
```

Returns top improvers and decliners.

**Query Parameters**:
- `period` (str): Time period - "1m", "3m", or "6m" (default: "1m")
- `limit` (int): Number of countries per list (default: 10)

**Response**:
```json
{
  "period": "1m",
  "improvers": [
    {
      "country_code": "IND",
      "country_name": "India",
      "momentum_score": 82.5,
      "score_change": 15.2,
      "classification": "Strongly Improving",
      "global_rank": 3
    }
  ],
  "decliners": [
    {
      "country_code": "ARG",
      "country_name": "Argentina",
      "momentum_score": 25.5,
      "score_change": -12.5,
      "classification": "Deteriorating",
      "global_rank": 25
    }
  ]
}
```

#### Get Map Data

```
GET /api/v1/momentum/map-data
```

Returns data formatted for Mapbox visualization.

**Query Parameters**:
- `include_structural` (bool): Include structural scores (default: false)

**Response**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "country_code": "USA",
        "country_name": "United States",
        "momentum_score": 75.5,
        "classification": "Improving",
        "color": "#4CAF50"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-95.71, 37.09]
      }
    }
  ]
}
```

---

### Indicators

#### Get All Indicators

```
GET /api/v1/indicators
```

Returns list of all indicators used in CMI.

**Response**:
```json
[
  {
    "id": 1,
    "code": "fx_momentum",
    "name": "FX Momentum",
    "pillar": "external_sector",
    "weight_in_pillar": 0.40,
    "source": "IMF",
    "calculation_method": "pct_change_6m",
    "frequency": "monthly"
  }
]
```

#### Get Country Indicators

```
GET /api/v1/indicators/{country_code}/latest
```

Returns latest indicator values for a country.

**Response**:
```json
{
  "country_code": "USA",
  "indicators": {
    "fx_momentum": {
      "value": 2.5,
      "percentile": 75.0,
      "date": "2024-01-01"
    }
  }
}
```

#### Refresh Data (Admin)

```
POST /api/v1/indicators/refresh
```

Triggers manual data refresh.

**Response**:
```json
{
  "status": "refresh_started",
  "message": "Data refresh job initiated"
}
```

---

## Error Responses

All endpoints return consistent error format:

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

- `200`: Success
- `404`: Resource not found
- `422`: Validation error
- `500`: Internal server error

---

## Rate Limiting

Not currently implemented. For production:
- Implement rate limiting
- Add API key authentication
- Monitor usage

---

## Data Freshness

- Indicator data: Updated monthly
- Momentum scores: Calculated after data updates
- Map data: Real-time from database

---

## WebSocket Support (Future)

Planned for real-time score updates:

```
ws://localhost:8000/ws/scores
```
