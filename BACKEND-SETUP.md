# Backend Setup Guide

## Prerequisites

- Python 3.10+
- uv (Python package manager)

## Installation

```bash
cd backend

# Install dependencies
uv sync

# Optional: Install development dependencies
uv sync --dev
```

## Database Initialization

```bash
# Initialize the database (only needed once)
uv run python scripts/init_db.py
```

This will:
- Create the DuckDB database at `data_db/uavs.duckdb`
- Execute the schema from `db/schema.sql`
- Load 16 UAVs from `data/initial_uavs.json`

## Running the Server

### Option 1: Using the run script (recommended)

```bash
./run.sh
```

This automatically:
- Checks if database exists and initializes if needed
- Starts the FastAPI server on port 7676
- Enables auto-reload for development

### Option 2: Manual start

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 7676 --reload
```

## Access the API

- **Server**: http://localhost:7676
- **API Docs (Swagger)**: http://localhost:7676/docs
- **API Docs (ReDoc)**: http://localhost:7676/redoc
- **API Base**: http://localhost:7676/api

## API Endpoints

### Health & Stats
- `GET /` - Root endpoint with API info
- `GET /api/health` - Health check
- `GET /api/stats` - Database statistics

### UAV Data
- `GET /api/uavs` - List all UAVs
- `GET /api/uavs/{designation}` - Get specific UAV (e.g., `/api/uavs/MQ-9`)
- `POST /api/uavs/compare` - Compare multiple UAVs
- `POST /api/uavs/search` - Search with filters

### Filters
- `GET /api/filters/countries` - Get list of countries
- `GET /api/filters/types` - Get list of UAV types

## Example Requests

### Get all UAVs
```bash
curl http://localhost:7676/api/uavs
```

### Get specific UAV
```bash
curl http://localhost:7676/api/uavs/MQ-9
```

### Compare UAVs
```bash
curl -X POST http://localhost:7676/api/uavs/compare \
  -H "Content-Type: application/json" \
  -d '{"designations": ["MQ-9", "RQ-4", "TB2"]}'
```

### Search by country
```bash
curl -X POST http://localhost:7676/api/uavs/search \
  -H "Content-Type: application/json" \
  -d '{"country": "United States"}'
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_api.py
```

## Configuration

Configuration is managed via environment variables. Create a `.env` file:

```env
# Server Configuration
HOST=0.0.0.0
PORT=7676
DEBUG=true
RELOAD=true

# Database Configuration
DATABASE_PATH=./data_db/uavs.duckdb

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:7676,http://127.0.0.1:7676

# API Configuration
API_V1_PREFIX=/api
PROJECT_NAME=X-UAV API
VERSION=0.1.0
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # DuckDB connection
│   └── schemas/
│       ├── __init__.py
│       └── uav.py          # Pydantic models
├── scripts/
│   └── init_db.py          # Database initialization
├── tests/
│   ├── __init__.py
│   └── test_api.py         # API tests
├── db/
│   └── schema.sql          # Database schema
├── data/
│   └── initial_uavs.json   # Initial UAV data
├── data_db/
│   └── uavs.duckdb         # DuckDB database file
├── pyproject.toml          # Project dependencies
└── run.sh                  # Startup script
```

## Troubleshooting

### Port already in use

If you get "Address already in use" error:

```bash
# Find process using port 7676
lsof -i :7676

# Kill the process
kill -9 <PID>
```

Or use a different port by modifying `.env`:
```env
PORT=8000
```

### Database locked

If you get "database is locked" error, ensure no other processes are accessing the database:

```bash
fuser data_db/uavs.duckdb
```

### Permission errors

Ensure the database directory is writable:

```bash
chmod -R 755 data_db/
```

## Development

### Code formatting
```bash
uv run black app/ tests/
```

### Linting
```bash
uv run ruff app/ tests/
```

### Type checking
```bash
uv run mypy app/
```

## Database Management

### Rebuild database
```bash
rm -f data_db/uavs.duckdb
uv run python scripts/init_db.py
```

### Query database directly
```bash
uv run python

>>> import duckdb
>>> conn = duckdb.connect('data_db/uavs.duckdb')
>>> conn.execute("SELECT COUNT(*) FROM uavs").fetchone()
(16,)
```

### Export data
```bash
uv run python -c "import duckdb; conn = duckdb.connect('data_db/uavs.duckdb'); conn.execute(\"COPY uavs TO 'export.json' (FORMAT JSON)\")"
```

## Next Steps

- [ ] Deploy frontend application
- [ ] Add authentication
- [ ] Implement caching
- [ ] Add more UAVs to database
- [ ] Implement data update API endpoints
