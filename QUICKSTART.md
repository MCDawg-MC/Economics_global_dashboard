# Country Momentum Index - Quick Start Guide

Get the full-stack application running in minutes with mock data.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Mapbox account (free tier works)

## Step 1: Database Setup (5 minutes)

### Create PostgreSQL Database

```bash
# Start PostgreSQL (if not running)
# Windows: Check Services
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
psql -U postgres
```

In PostgreSQL:
```sql
CREATE DATABASE country_momentum_index;
CREATE USER cmi_user WITH ENCRYPTED PASSWORD 'cmi_password_123';
GRANT ALL PRIVILEGES ON DATABASE country_momentum_index TO cmi_user;
\q
```

## Step 2: Backend Setup (10 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env` file:
```env
DATABASE_URL=postgresql://cmi_user:cmi_password_123@localhost:5432/country_momentum_index
DATABASE_URL_ASYNC=postgresql+asyncpg://cmi_user:cmi_password_123@localhost:5432/country_momentum_index

# Optional: Get free key from https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY=

# Other settings (defaults are fine for development)
DEBUG=True
LOG_LEVEL=INFO
```

### Initialize Database

```bash
# Create tables and seed initial data
python scripts/seed_data.py
```

You should see:
```
Seeding countries...
Seeded 28 countries
Seeding indicators...
Seeded 13 indicators
```

### Generate Mock Data (for testing)

```bash
python scripts/generate_mock_data.py
```

This creates 24 months of realistic mock data for all countries and indicators.

### Calculate Scores

```bash
python scripts/calculate_scores.py
```

This calculates momentum scores from the mock data.

### Start Backend Server

```bash
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

Test it: http://localhost:8000/api/v1/docs

## Step 3: Frontend Setup (5 minutes)

Open a NEW terminal:

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
```

Edit `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000/api/v1

# Get free token from https://www.mapbox.com/
# Create account → Account → Tokens → Create token
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
```

### Start Frontend Server

```bash
npm start
```

✅ Frontend opens automatically at: http://localhost:3000

## Step 4: Verify Everything Works

### Backend API Tests

Visit http://localhost:8000/api/v1/docs

Try these endpoints:
1. `GET /countries` - Should return 28 countries
2. `GET /momentum/latest` - Should return momentum scores
3. `GET /momentum/leaderboard?period=1m` - Should return top movers
4. `GET /momentum/map-data` - Should return GeoJSON data

### Frontend Tests

Visit http://localhost:3000

You should see:
1. ✅ Global map with colored country markers
2. ✅ Top Improvers and Decliners leaderboards
3. ✅ Click a country marker → popup appears
4. ✅ Click "View Details" → country detail page
5. ✅ Charts showing historical data

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
# Windows:
sc query postgresql

# Mac:
brew services list

# Linux:
sudo systemctl status postgresql
```

### Python Import Errors

```bash
# Ensure virtual environment is activated
# You should see (venv) in your terminal prompt

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Won't Start

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Mapbox Map Not Showing

- Verify `REACT_APP_MAPBOX_TOKEN` is set in `frontend/.env`
- Get a free token from https://www.mapbox.com/
- Restart the frontend server after adding the token

### No Data in Frontend

```bash
# Regenerate mock data
cd backend
python scripts/generate_mock_data.py
python scripts/calculate_scores.py

# Verify API is working
curl http://localhost:8000/api/v1/momentum/latest
```

## Next Steps

### Option 1: Use Real Data

1. Get API keys:
   - FRED: https://fred.stlouisfed.org/docs/api/api_key.html
   - IMF, World Bank, OECD: No key needed

2. Map indicator series IDs in `backend/app/utils/constants.py`

3. Run data fetcher:
   ```bash
   python scripts/fetch_data.py
   python scripts/calculate_scores.py
   ```

### Option 2: Customize the App

- Add more countries in `backend/app/utils/constants.py`
- Add more indicators
- Customize frontend styling
- Add authentication
- Deploy to production

### Option 3: Explore the Code

- **Backend API**: `backend/app/api/endpoints/`
- **Data Fetchers**: `backend/app/services/data_fetchers/`
- **Calculations**: `backend/app/services/calculators/`
- **Frontend Components**: `frontend/src/components/`
- **Pages**: `frontend/src/pages/`

## Development Workflow

### Daily Development

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate  # or source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm start
```

### Update Data

```bash
cd backend

# Option 1: Generate new mock data
python scripts/generate_mock_data.py
python scripts/calculate_scores.py

# Option 2: Fetch real data (requires API keys)
python scripts/fetch_data.py
python scripts/calculate_scores.py

# Option 3: Run complete pipeline
python scripts/update_all.py
```

### Database Migrations

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Complete Feature List

### ✅ Backend Features

- ✅ FastAPI REST API with automatic docs
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ 5-pillar momentum scoring system
- ✅ Cross-country percentile calculations
- ✅ 28 MVP countries
- ✅ 13 economic indicators
- ✅ Data fetchers for IMF, World Bank, FRED
- ✅ Mock data generator for testing
- ✅ Score calculation pipeline
- ✅ Historical tracking (1m, 3m, 6m)
- ✅ Global rankings

### ✅ Frontend Features

- ✅ Interactive Mapbox world map
- ✅ Color-coded country markers
- ✅ Top Improvers/Decliners leaderboards
- ✅ Country detail pages
- ✅ Time series charts (Recharts)
- ✅ Radar charts for pillar breakdown
- ✅ Momentum vs Combined score toggle
- ✅ Time period selector (1m/3m/6m)
- ✅ Responsive design
- ✅ Clean, modern UI

### ✅ Data Pipeline

- ✅ Automated data fetching
- ✅ Momentum calculation engine
- ✅ Cross-country standardization
- ✅ Pillar aggregation
- ✅ Score change tracking
- ✅ Classification system

## API Examples

### Get All Countries

```bash
curl http://localhost:8000/api/v1/countries
```

### Get Leaderboard

```bash
curl "http://localhost:8000/api/v1/momentum/leaderboard?period=1m&limit=5"
```

### Get Country Details

```bash
curl http://localhost:8000/api/v1/countries/USA
```

### Get Map Data

```bash
curl http://localhost:8000/api/v1/momentum/map-data
```

## Project Structure

```
Economics_global_dashboard/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/     # API routes
│   │   ├── core/             # Configuration
│   │   ├── db/               # Database
│   │   ├── models/           # ORM models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
│   ├── scripts/              # Data scripts
│   │   ├── seed_data.py
│   │   ├── generate_mock_data.py
│   │   ├── calculate_scores.py
│   │   ├── fetch_data.py
│   │   └── update_all.py
│   └── alembic/              # Migrations
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   └── styles/          # CSS
│   └── public/              # Static files
└── docs/                    # Documentation
```

## Support

- Documentation: See `docs/` folder
- GitHub Issues: https://github.com/MCDawg-MC/Economics_global_dashboard/issues
- API Docs: http://localhost:8000/api/v1/docs

---

**You're all set! 🎉**

The Country Momentum Index is now running with:
- 28 countries
- 13 economic indicators
- 24 months of mock data
- Interactive world map
- Real-time leaderboards
- Detailed country pages

Happy coding!
