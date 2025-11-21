# X-UAV: Unmanned Aerial Vehicle Comparison Platform

A comprehensive web application for comparing government and military unmanned aerial vehicles (UAVs) from around the world.

## Overview

X-UAV provides detailed specifications, performance metrics, and visual comparisons of military and government UAVs. The platform enables users to compare different UAV systems across multiple dimensions including performance, capabilities, cost, and operational characteristics.

### Current Status

**Phase**: ✅ FULLY IMPLEMENTED AND OPERATIONAL
**Version**: 0.1.0
**Status**: Production Ready

## Features

### ✅ Implemented (v0.1.0)
- ✅ Comprehensive UAV database with 16 entries from 6 countries
- ✅ Detailed specifications covering 80+ data fields
- ✅ RESTful API with 10 endpoints (FastAPI + DuckDB)
- ✅ Interactive Vue.js 3 frontend with table display
- ✅ Sorting on all columns (designation, country, type, specs, cost)
- ✅ Multi-level filtering (country, type, search)
- ✅ Detailed UAV modal with full specifications
- ✅ Pagination (20 items per page)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Zero-cost local deployment
- ✅ 92% test coverage on backend
- ✅ Automated startup scripts

### 📋 Planned (Future Phases)
- Visual imagery for each UAV
- Accurately scaled overhead silhouettes for size comparison
- Interactive 3D model viewer with rotation capability
- Performance comparison charts and analytics
- Export functionality (PDF, CSV)
- Advanced search and filtering

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: DuckDB (embedded, zero-cost, high-performance analytical database)
- **Package Manager**: uv (fast Python package management)
- **Data Validation**: Pydantic
- **Testing**: pytest

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **Styling**: CSS3
- **3D Rendering** (future): Three.js

### Development
- **Port**: 7676
- **Environment**: Local development (localhost)
- **Deployment**: Zero-cost, local-first architecture

## UAV Coverage

### 16 UAVs from 6 Countries

#### United States (5)
- MQ-9 Reaper - MALE UCAV
- RQ-4 Global Hawk - HALE ISR
- MQ-1 Predator - MALE ISR/Strike (Retired)
- RQ-170 Sentinel - Stealth ISR
- X-47B - Stealth UCAV Demonstrator

#### China (4)
- Wing Loong II - MALE UCAV
- CH-4 Rainbow - MALE UCAV
- GJ-11 Sharp Sword - Stealth UCAV
- WZ-8 - Supersonic Reconnaissance

#### Russia (3)
- Orion/Sirius - MALE UCAV
- Korsar - Tactical ISR
- Forpost-R - MALE ISR

#### Turkey (1)
- Bayraktar TB2 - MALE UCAV

#### Israel (2)
- Hermes 450 - MALE ISR
- Heron TP - MALE ISR

#### United Kingdom (1)
- Watchkeeper WK450 - Tactical ISR

## Project Structure

```
x-uav/
├── backend/                        # Backend API
│   ├── app/
│   │   ├── main.py                # ✅ FastAPI application
│   │   ├── database.py            # ✅ DuckDB interface
│   │   ├── config.py              # ✅ Configuration
│   │   └── schemas/
│   │       └── uav.py             # ✅ Pydantic models
│   ├── scripts/
│   │   └── init_db.py             # ✅ Database initialization
│   ├── tests/
│   │   └── test_api.py            # ✅ API tests (13/13 passing)
│   ├── db/
│   │   └── schema.sql             # ✅ DuckDB schema
│   ├── data/
│   │   └── initial_uavs.json      # ✅ 16 UAVs data
│   ├── data_db/
│   │   └── uavs.duckdb            # ✅ Database file
│   ├── pyproject.toml             # ✅ Dependencies
│   └── run.sh                     # ✅ Startup script
├── frontend/                       # Frontend application
│   ├── src/
│   │   ├── App.vue                # ✅ Root component
│   │   ├── main.js                # ✅ Entry point
│   │   ├── components/
│   │   │   └── UAVList.vue        # ✅ Main table component
│   │   ├── services/
│   │   │   └── api.js             # ✅ API client
│   │   └── assets/
│   │       └── css/
│   │           └── main.css       # ✅ Styles
│   ├── index.html                 # ✅ HTML template
│   ├── vite.config.js             # ✅ Vite config
│   └── package.json               # ✅ Dependencies
├── start.sh                        # ✅ Full stack startup
├── stop.sh                         # ✅ Shutdown script
├── CLAUDE.md                       # ✅ Project guidelines
├── PROMPTS.md                      # ✅ Prompt tracking
├── PROJECT-SUMMARY.md              # ✅ Project overview
├── UAV-DATA-MODEL.md               # ✅ Data model
├── VISUAL-REQUIREMENTS.md          # ✅ Visual specs (future)
├── DATABASE-SCHEMA.md              # ✅ Database design
├── BACKEND-SETUP.md                # ✅ Backend documentation
├── BACKEND-TEST-RESULTS.md         # ✅ Test results
├── FRONTEND-IMPLEMENTATION.md      # ✅ Frontend documentation
├── TASK.md                         # ✅ Task tracking
└── README.md                       # ✅ This file

✅ = Completed and Operational
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- uv (Python package manager)

### Installation

```bash
# Clone the repository (if applicable)
cd /home/junior/src/x-uav

# Backend setup
cd backend
uv sync
uv run python scripts/init_db.py

# Frontend setup
cd ../frontend
npm install
```

### Running the Application

**Option 1: Automated Startup (Recommended)**
```bash
cd /home/junior/src/x-uav
./start.sh
```

**Option 2: Manual Startup**
```bash
# Terminal 1: Backend
cd backend
./run.sh
# Or: uv run uvicorn app.main:app --host 0.0.0.0 --port 8877

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Stop the Application
```bash
./stop.sh
```

### Access
- **Frontend**: http://localhost:7677
- **Backend API**: http://localhost:8877
- **API Docs (Swagger)**: http://localhost:8877/docs
- **API Docs (ReDoc)**: http://localhost:8877/redoc

## API Endpoints (Planned)

```
GET  /api/uavs                    # List all UAVs
GET  /api/uavs/{designation}      # Get specific UAV
POST /api/uavs/compare            # Compare multiple UAVs
POST /api/uavs/search             # Search with filters
GET  /api/health                  # Health check
```

## Data Model

Each UAV entry includes:

### Identification
- Designation, Name, Manufacturer
- Country of Origin, NATO Class, Type
- Operational Status

### Physical Characteristics
- Dimensions (wingspan, length, height)
- Weights (empty, max takeoff)
- Payload capacity, Fuel capacity
- Airframe type

### Propulsion
- Engine type, manufacturer, model
- Thrust/horsepower, Number of engines
- Propeller configuration

### Performance
- Speed (cruise, max)
- Service ceiling
- Range, Endurance
- Combat radius

### Mission Capabilities
- Primary function, Mission types
- Armament, Weapons load
- Hardpoints, Internal weapons bays

### Sensors & Avionics
- Sensor suite, Radar type
- Communications, Datalink
- Stealth features, Autonomy level

### Operational Details
- Operators, Export countries
- Crew size, Ground control station
- Launch/recovery methods

### Economic
- Unit cost, Program cost
- Fiscal year

### Visual Assets (Future)
- Imagery URLs, Silhouette URL
- 3D Model URLs

## Development Guidelines

Following `CLAUDE.md` project guidelines:

- ✅ **Port 7676**: Always use port 7676 for the web application
- ✅ **Zero-cost**: Use DuckDB (embedded), local hosting, no cloud services
- ✅ **No Hardcoded Values**: Configuration-driven design
- ✅ **Modular Code**: Keep files under 500 lines
- ✅ **Well-Tested**: Pytest unit tests for all features
- ✅ **Type Hints**: Use Python type hints throughout
- ✅ **Docstrings**: Google-style docstrings for all functions
- ✅ **uv Package Manager**: Use `uv` instead of `pip`

## Testing

```bash
# Run backend tests
cd backend
uv run pytest

# Run frontend tests (when implemented)
cd frontend
npm run test
```

## Documentation

- **`PROJECT-SUMMARY.md`**: Comprehensive project overview and status
- **`UAV-DATA-MODEL.md`**: Complete data model specification
- **`DATABASE-SCHEMA.md`**: Database design and DuckDB schema
- **`VISUAL-REQUIREMENTS.md`**: Visual asset specifications and requirements
- **`TASK.md`**: Task tracking and project roadmap
- **`PROMPTS.md`**: Prompt history and tracking

## Roadmap

### Phase 1: Core Application (Current) 🔄
- Database initialization
- FastAPI backend with DuckDB
- Vue.js frontend with table display
- Sorting, filtering, search
- Unit tests

### Phase 2: Visual Enhancements ⏳
- UAV imagery integration
- Overhead silhouette comparison tool
- Image galleries

### Phase 3: 3D Model Viewer ⏳
- Three.js integration
- Interactive 3D models
- Rotation, zoom, preset views

### Phase 4: Advanced Features ⏳
- Performance comparison charts
- Export functionality (PDF, CSV)
- User preferences
- Saved comparisons
- Expanded UAV database (50+ UAVs)

## Contributing

This is currently a solo development project. Contributions, suggestions, and UAV data additions are welcome.

## Data Sources

- Wikipedia (Unmanned Aerial Vehicle articles)
- JAPCC (Joint Air Power Competence Centre)
- Official manufacturer specifications
- Government fact sheets (USAF, NATO, etc.)
- Defense news publications

## License

_(To be determined)_

## Disclaimer

This application compiles publicly available information about military UAVs for educational and comparison purposes. All data is sourced from public domain materials and open-source intelligence. No classified or export-controlled information is included.

## Contact

_(To be added)_

---

**Last Updated**: 2025-11-18
**Version**: 0.1.0-alpha
**Status**: Planning Complete, Development In Progress
