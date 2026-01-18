# Country Momentum Index - Architecture Documentation

## System Overview

The Country Momentum Index (CMI) is a full-stack web application that tracks and visualizes economic momentum across countries worldwide.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Map View    │  │  Dashboard   │  │  Country     │  │
│  │  (Mapbox)    │  │  (Charts)    │  │  Detail      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP/REST
┌───────────────────────────┴─────────────────────────────┐
│                   Backend API (FastAPI)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Countries   │  │  Momentum    │  │  Indicators  │  │
│  │  Endpoints   │  │  Endpoints   │  │  Endpoints   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │ SQLAlchemy ORM
┌───────────────────────────┴─────────────────────────────┐
│                  Database (PostgreSQL)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Countries   │  │  Indicators  │  │  Momentum    │  │
│  │  Table       │  │  & Values    │  │  Scores      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 Data Sources (External)                  │
│   IMF   │  World Bank  │  OECD  │  BIS  │  FRED  │ UNDP │
└─────────────────────────────────────────────────────────┘
                            ▲
                            │ HTTP APIs
┌───────────────────────────┴─────────────────────────────┐
│                  Data Fetching Pipeline                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Fetchers    │  │  Calculators │  │  Scheduler   │  │
│  │  (APIs)      │  │  (Momentum)  │  │  (Monthly)   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Mapbox GL JS**: Interactive map visualization
- **Chart.js / Recharts**: Time series and radar charts
- **Axios**: HTTP client
- **React Router**: Navigation

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Pydantic**: Data validation and serialization
- **APScheduler**: Task scheduling

### Database
- **PostgreSQL 15**: Relational database
- Time-series data storage
- JSON support for flexible fields

### Data Processing
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **scipy**: Statistical functions

### Data Sources
- **IMF API**: CPI, FX, policy rates
- **World Bank API**: GDP, exports, education
- **FRED API**: Supplemental macro data
- **OECD API**: Industrial production, PMI
- **BIS**: Credit data
- **UNDP**: Human development indices

## Data Flow

### 1. Data Collection

```
External APIs → Data Fetchers → Raw Time Series → Database
```

1. Scheduled job triggers data fetchers
2. Fetchers retrieve data from external APIs
3. Raw values stored in `indicator_values` table

### 2. Momentum Calculation

```
Raw Values → Momentum Calculator → Calculated Values → Database
```

1. Apply momentum formulas (YoY acceleration, % change, etc.)
2. Store calculated momentum values
3. Calculate cross-country z-scores and percentile ranks

### 3. Score Aggregation

```
Indicator Percentiles → Pillar Scores → Final Momentum Score
```

1. Weight indicators within each pillar
2. Calculate pillar scores (0-100)
3. Weight pillars to get final momentum score
4. Classify (Strongly Improving, Improving, etc.)

### 4. Frontend Display

```
Database → API Endpoints → React Components → User Interface
```

1. Frontend requests latest scores
2. API queries database
3. Format data for visualization
4. Render maps, charts, and tables

## Database Schema

### Countries Table
```sql
countries (
    code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100),
    region VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### Indicators Table
```sql
indicators (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE,
    name VARCHAR(200),
    pillar VARCHAR(50),
    weight_in_pillar FLOAT,
    source VARCHAR(50),
    calculation_method VARCHAR(50),
    frequency VARCHAR(20)
)
```

### Indicator Values Table
```sql
indicator_values (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) FK,
    indicator_id INTEGER FK,
    date TIMESTAMP,
    raw_value FLOAT,
    calculated_value FLOAT,
    percentile_rank FLOAT,
    z_score FLOAT
)
```

### Momentum Scores Table
```sql
momentum_scores (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) FK,
    date TIMESTAMP,
    momentum_score FLOAT,
    structural_score FLOAT,
    combined_score FLOAT,
    classification VARCHAR(50),
    global_rank INTEGER,
    score_change_1m FLOAT,
    score_change_3m FLOAT,
    score_change_6m FLOAT
)
```

## Calculation Engine

### Momentum Formulas

1. **YoY Acceleration**: `YoY(t) - YoY(t-6m)`
2. **Percentage Change**: `(Value(t) - Value(t-n)) / Value(t-n) × 100`
3. **Absolute Change**: `Value(t) - Value(t-n)`
4. **Z-Score**: `(Value - Mean) / StdDev`
5. **Percentile Rank**: `rank(value) / count(values) × 100`

### Pillar Aggregation

```
Pillar Score = Σ (Indicator_Percentile × Weight)
```

### Final Score

```
Momentum Score = Σ (Pillar_Score × Pillar_Weight)
```

Where momentum pillars exclude structural (or include based on toggle).

## API Design

### RESTful Principles
- Resource-based URLs
- Standard HTTP methods
- JSON response format
- Consistent error handling

### Endpoint Structure
```
/api/v1/
  /countries
    GET / - List all
    GET /{code} - Get details
    GET /{code}/momentum-history - Historical scores
  /momentum
    GET /latest - Latest scores
    GET /leaderboard - Top movers
    GET /map-data - GeoJSON for map
  /indicators
    GET / - List all
    GET /{country}/latest - Latest values
    POST /refresh - Trigger update
```

## Security Considerations

### Current (Development)
- Open API
- No authentication
- CORS enabled for localhost

### Production Requirements
- API key authentication
- Rate limiting
- HTTPS only
- CORS restricted to production domain
- Input validation
- SQL injection protection (via ORM)
- Environment variable secrets

## Scalability

### Database
- Indexes on country_code, date
- Partitioning by date for large datasets
- Connection pooling

### API
- Caching frequent queries
- Pagination for large result sets
- Async database queries

### Frontend
- Code splitting
- Lazy loading components
- CDN for static assets

## Monitoring & Logging

### Logging
- Application logs (FastAPI)
- Data fetch logs
- Error tracking

### Metrics
- API response times
- Database query performance
- Data freshness

## Deployment Architecture

### Development
- Local PostgreSQL
- Local FastAPI server
- React dev server

### Production (Future)
```
Frontend: Vercel/Netlify
Backend: Heroku/Railway/AWS
Database: Managed PostgreSQL (AWS RDS/Heroku)
Scheduler: Background worker dyno
```

## Future Enhancements

1. **Real-time Updates**: WebSocket support
2. **User Accounts**: Save preferences, custom dashboards
3. **Alerts**: Email/SMS for score changes
4. **More Indicators**: Expand to 20+ indicators
5. **More Countries**: Scale to 100+ countries
6. **Historical Analysis**: Compare periods
7. **Forecasting**: ML-based predictions
8. **API Documentation**: Interactive Swagger UI
9. **Mobile App**: React Native
10. **Export**: PDF/Excel reports
