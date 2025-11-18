# X-UAV Quick Start Guide

Get the X-UAV application up and running in under 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Port 8529 (ArangoDB) available
- Port 6379 (Redis) available
- Port 5434 (PostgreSQL) available (uses 5434 to avoid conflicts with 5432/5433)
- Port 8000 (Backend API) available
- Port 7676 (Frontend) available

## Start the Application

```bash
# Make scripts executable (first time only)
chmod +x start.sh stop.sh status.sh

# Start all services
./start.sh
```

The script will:
1. ✓ Check if Docker is running
2. ✓ Stop any existing X-UAV services
3. ✓ Start ArangoDB, PostgreSQL, and Redis
4. ✓ Wait for databases to be ready
5. ✓ Initialize the database schema
6. ✓ Import CCA platform data
7. ✓ Start the Backend API
8. ✓ Start the Frontend application
9. ✓ Show service status and URLs

## Access the Application

Once started, access services at:

- **Frontend**: http://localhost:7676
- **API Documentation**: http://localhost:8000/docs
- **ArangoDB Web UI**: http://localhost:8529
  - Username: `root`
  - Password: `development`

## Common Commands

```bash
# Check service status
./status.sh

# View logs for all services
./status.sh --logs

# View logs for specific service
./status.sh --logs backend

# Check health status
./status.sh --health

# Stop services
./stop.sh

# Stop and remove containers
./stop.sh --remove

# Restart services
./start.sh
```

## Troubleshooting

### Port Conflicts

If you see "port already allocated" errors:

```bash
# Check what's using the port
lsof -i :8529  # ArangoDB
lsof -i :5434  # PostgreSQL (Docker)
lsof -i :6379  # Redis

# Note: Docker PostgreSQL uses port 5434 to avoid conflicts
# with local PostgreSQL on ports 5432/5433
```

### Services Won't Start

```bash
# Check Docker is running
docker info

# View detailed logs
./status.sh --logs

# Clean restart
./stop.sh --remove
./start.sh --rebuild
```

### Database Issues

```bash
# Reinitialize database
cd backend
uv run python scripts/init_db.py

# Or clean start
./start.sh --clean
```

## Development Workflow

```bash
# 1. Start services
./start.sh

# 2. Make code changes...

# 3. Backend auto-reloads
# 4. Frontend auto-rebuilds

# 5. Check logs if needed
./status.sh --logs backend

# 6. Stop when done
./stop.sh
```

## Next Steps

- Explore the API at http://localhost:8000/docs
- Browse the graph database at http://localhost:8529
- Read the full documentation in SCRIPTS.md
- Check the ontology documentation in backend/docs/ONTOLOGY.md

## Need Help?

```bash
# Show help for any script
./start.sh --help
./stop.sh --help
./status.sh --help
```

For detailed information, see [SCRIPTS.md](SCRIPTS.md).
