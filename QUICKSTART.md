# X-UAV Quick Start Guide

## Prerequisites

Before starting, ensure you have:
- Docker and Docker Compose installed
- Git (for version control)
- (Optional) Node.js 20+ for local frontend development
- (Optional) Python 3.11+ with `uv` for local backend development

## Starting the Application

### Option 1: Docker Compose (Recommended)

The easiest way to run the entire application:

```bash
# From the project root directory
docker-compose up -d
```

This starts:
- ArangoDB on port 8529
- PostgreSQL on port 5432
- Redis on port 6379
- Backend API on port 8000
- Frontend on port 7676

### Access the Application

Once all services are running:

1. **Frontend Web Interface**: http://localhost:7676
2. **Backend API**: http://localhost:8000
3. **API Documentation**: http://localhost:8000/docs
4. **ArangoDB Web UI**: http://localhost:8529
   - Username: `root`
   - Password: `development`

### Check Service Status

```bash
# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Check running containers
docker-compose ps
```

### Stop the Application

```bash
# Stop all services
docker-compose down

# Stop and remove all data (WARNING: deletes database contents)
docker-compose down -v
```

## Option 2: Local Development

### Backend Development

```bash
cd backend

# Install dependencies
uv pip install -e ".[dev]"

# Run development server (requires databases to be running)
uv run uvicorn app.main:app --reload --port 8000
```

**Note**: You still need to start ArangoDB, PostgreSQL, and Redis:

```bash
docker-compose up -d arangodb postgres redis
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at http://localhost:7676

## First Time Setup

After starting the application for the first time:

1. **Check Health**: Visit http://localhost:7676 and verify the API status shows "healthy"

2. **Explore ArangoDB**:
   - Open http://localhost:8529
   - Login with root/development
   - The `xuav` database will be created automatically

3. **View API Docs**:
   - Open http://localhost:8000/docs
   - Explore available endpoints

## Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

```bash
# Check what's using the port (example for port 7676)
sudo lsof -i :7676

# Kill the process
sudo kill -9 <PID>
```

Or change the port in `.env`:

```env
PORT=7677  # Use a different port
```

### Database Connection Errors

1. Ensure Docker services are running:
```bash
docker-compose ps
```

2. Check service logs:
```bash
docker-compose logs arangodb
docker-compose logs postgres
```

3. Restart services:
```bash
docker-compose restart
```

### Frontend Can't Connect to Backend

1. Check backend is running: http://localhost:8000/health

2. Verify CORS settings in `backend/app/core/config.py`

3. Check browser console for errors

## Development Workflow

### Making Changes

1. **Backend Changes**:
   - Edit files in `backend/app/`
   - Uvicorn will auto-reload on file changes

2. **Frontend Changes**:
   - Edit files in `frontend/src/`
   - Vite will hot-reload in the browser

3. **Database Schema Changes**:
   - See `IMPLEMENTATION-STATUS.md` for schema setup

### Running Tests

```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests (when implemented)
cd frontend
npm run test
```

## Next Steps

After getting the application running:

1. Review the [PROJECT-PLAN.md](PROJECT-PLAN.md) for the full roadmap
2. Check [IMPLEMENTATION-STATUS.md](IMPLEMENTATION-STATUS.md) for current progress
3. See [README.md](README.md) for detailed documentation

## Getting Help

- Check logs: `docker-compose logs -f`
- Review configuration: `.env` file
- API documentation: http://localhost:8000/docs
- Project documentation: See `docs/` directory

---

**Quick Command Reference**

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart a service
docker-compose restart backend

# Rebuild a service
docker-compose up -d --build backend

# Access a container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```
