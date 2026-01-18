# Country Momentum Index (CMI)

A data-driven web application that scores and maps countries based on economic momentum, not static development levels.

## Project Overview

The Country Momentum Index aggregates standardized momentum signals across 5 pillars to surface direction and acceleration across macro, education, and industry indicators.

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18+ with Mapbox GL JS
- **Database**: PostgreSQL 15+
- **Data Processing**: pandas, numpy, scipy
- **Charting**: Chart.js or Recharts

## Project Structure

```
Economics_global_dashboard/
├── backend/           # FastAPI backend and data pipeline
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration
│   │   ├── db/            # Database session
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utilities
│   ├── scripts/       # Data fetching scripts
│   └── tests/         # Backend tests
├── frontend/          # React frontend application
├── database/          # Database migrations and schemas
├── docs/             # Documentation
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Mapbox API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
alembic upgrade head  # Run database migrations
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env  # Add your Mapbox token
npm start
```

## Pillars & Indicators

### 1. External Sector Momentum (25%)
- FX momentum (40%)
- FX reserves change (30%)
- Export growth momentum (30%)

### 2. Inflation & Price Momentum (20%)
- CPI YoY acceleration (70%)
- Core CPI acceleration (30%)

### 3. Real Activity Momentum (20%)
- Industrial Production YoY acceleration (60%)
- Manufacturing PMI (40%)

### 4. Monetary & Financial Conditions (20%)
- Policy rate changes (40%)
- Balance sheet growth (30%)
- Credit growth (30%)

### 5. Structural / Capacity Score (15%)
- Education / human capital (40%)
- Industry composition (40%)
- Diversification proxy (20%)

## Data Sources

- IMF (IFS & MFS): CPI, FX reserves, policy rates, credit
- World Bank: GDP, exports, education, industry
- OECD: Industrial production, PMIs
- BIS: Credit cycles, banking exposure
- FRED: Supplemental international macro series
- UNDP: Human Development / education indices

## MVP Scope

- 20-30 countries
- Monthly updates
- 5 pillars
- Percentile-based scores

## Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Code Quality

```bash
# Backend
black app/
flake8 app/
mypy app/
```

## License

MIT
