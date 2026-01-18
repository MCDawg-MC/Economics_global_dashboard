# Country Momentum Index - Setup Guide

Complete setup instructions for the Country Momentum Index application.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 15+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads)

## Step 1: Database Setup

### Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE country_momentum_index;
CREATE USER cmi_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE country_momentum_index TO cmi_user;

# Exit psql
\q
```

## Step 2: Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your configuration
```

Edit `.env` and update the following:

```env
DATABASE_URL=postgresql://cmi_user:your_secure_password@localhost:5432/country_momentum_index
DATABASE_URL_ASYNC=postgresql+asyncpg://cmi_user:your_secure_password@localhost:5432/country_momentum_index

# Get FRED API key from https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY=your_fred_api_key_here
```

### 5. Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Seed initial data
python scripts/seed_data.py
```

### 6. Start Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/api/v1/docs`

## Step 3: Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
```

Edit `.env` and add your Mapbox token:

```env
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
REACT_APP_API_URL=http://localhost:8000/api/v1
```

Get a Mapbox token from: https://www.mapbox.com/

### 4. Start Frontend Development Server

```bash
npm start
```

The application will open at `http://localhost:3000`

## Step 4: Fetch Initial Data (Optional)

To populate the database with real economic data:

```bash
cd backend
python scripts/fetch_data.py
```

**Note**: This requires:
- Valid API keys configured
- Proper indicator series IDs mapped in the code
- Internet connection

## Verification

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Database Connection**:
   ```bash
   psql -U cmi_user -d country_momentum_index -c "\dt"
   ```

3. **Frontend**:
   Open browser to `http://localhost:3000`

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
# Windows
pg_ctl status

# macOS/Linux
sudo systemctl status postgresql
```

### Python Dependencies

```bash
# Clear cache and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### Node Modules

```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. **Configure API Keys**: Get real API keys for data sources
2. **Map Indicator Series**: Update indicator source_series_id in seed_data.py
3. **Fetch Data**: Run fetch_data.py to populate database
4. **Calculate Scores**: Implement score calculation pipeline
5. **Customize Frontend**: Adjust styling and features

## Production Deployment

See `docs/DEPLOYMENT.md` for production deployment instructions.

## Development Tips

### Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
black app/
flake8 app/

# Frontend
npm run lint
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```
