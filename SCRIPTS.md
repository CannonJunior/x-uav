# X-UAV Management Scripts

This directory contains convenience scripts for managing the X-UAV application stack.

## Quick Start

```bash
# Start the entire application
./start.sh

# Check application status
./status.sh

# Stop the application
./stop.sh
```

---

## Scripts Overview

### 🚀 start.sh - Application Startup

Manages the complete startup sequence for the X-UAV application.

**Features:**
- Checks if services are already running
- Stops existing services gracefully
- Starts all required services in the correct order
- Waits for databases to be ready
- Initializes database schema and data
- Shows service status and URLs

**Usage:**

```bash
# Start all services (default)
./start.sh

# Start only database services
./start.sh --db-only

# Skip database initialization
./start.sh --no-init

# Rebuild Docker images before starting
./start.sh --rebuild

# Clean environment (removes volumes and data)
./start.sh --clean
```

**What it starts:**
- **ArangoDB** - Graph database (port 8529)
- **PostgreSQL** - Relational database (port 5432)
- **Redis** - Cache and streams (port 6379)
- **Backend** - FastAPI application (port 8000)
- **Frontend** - Vue.js application (port 7676)

---

### 🛑 stop.sh - Application Shutdown

Gracefully stops all X-UAV services.

**Usage:**

```bash
# Stop services (containers remain)
./stop.sh

# Stop and remove containers
./stop.sh --remove

# Stop, remove containers, and delete all data
./stop.sh --volumes
```

**Options:**
- `--remove` - Remove containers after stopping
- `--volumes` - Also remove volumes (⚠️ deletes all data)

---

### 📊 status.sh - Service Status

Shows detailed status information for all services.

**Usage:**

```bash
# Show service status
./status.sh

# Show health checks
./status.sh --health

# View logs for all services
./status.sh --logs

# View logs for a specific service
./status.sh --logs backend
./status.sh --logs arangodb
```

**Information displayed:**
- Container running status
- Service URLs and credentials
- Resource usage (CPU, memory, network)
- Health check results

---

## Service URLs

After starting the application with `./start.sh`, access services at:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:7676 | - |
| **Backend API** | http://localhost:8000 | - |
| **API Documentation** | http://localhost:8000/docs | - |
| **ArangoDB Web UI** | http://localhost:8529 | root / development |
| **PostgreSQL** | localhost:5434 | xuav / development |
| **Redis** | localhost:6379 | - |

---

## Common Workflows

### First Time Setup

```bash
# Start everything (includes database initialization)
./start.sh

# Verify all services are running
./status.sh --health
```

### Daily Development

```bash
# Start application
./start.sh

# Work on your code...

# Check status
./status.sh

# View backend logs
./status.sh --logs backend

# Stop when done
./stop.sh
```

### Troubleshooting

```bash
# Check service health
./status.sh --health

# View all logs
./status.sh --logs

# Restart services
./stop.sh
./start.sh --rebuild

# Clean restart (removes all data)
./start.sh --clean
```

### Rebuild After Changes

```bash
# Rebuild Docker images
./start.sh --rebuild

# Or manually
docker compose build
./start.sh
```

### Database Management

```bash
# Start only databases
./start.sh --db-only

# Initialize database manually
cd backend
uv run python scripts/init_db.py
```

---

## Environment Variables

The application uses environment variables defined in `docker-compose.yml`:

**Backend:**
- `ENVIRONMENT=development`
- `PORT=8000`
- `DATABASE_URL=postgresql://xuav:development@postgres:5432/xuav`
- `GRAPH_DB_URL=http://arangodb:8529`
- `REDIS_URL=redis://redis:6379`

**Frontend:**
- `NODE_ENV=development`
- `VITE_API_URL=http://localhost:8000`

**Databases:**
- ArangoDB: `ARANGO_ROOT_PASSWORD=development`
- PostgreSQL: `POSTGRES_USER=xuav`, `POSTGRES_PASSWORD=development`

---

## Data Persistence

Application data is stored in Docker volumes and local directories:

```
data/
├── arangodb/     # Graph database data
├── postgres/     # Relational database data
└── redis/        # Cache data
```

**⚠️ Warning:** Using `./stop.sh --volumes` will delete all data in these directories!

---

## Docker Compose Commands

For more advanced control, use Docker Compose directly:

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d backend

# View logs
docker compose logs -f backend

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild images
docker compose build

# View running containers
docker compose ps

# Execute command in container
docker compose exec backend bash
docker compose exec arangodb arangosh
```

---

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker info

# Check for port conflicts
lsof -i :7676  # Frontend
lsof -i :8000  # Backend
lsof -i :8529  # ArangoDB
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# View container logs
./status.sh --logs
```

### Database initialization fails

```bash
# Check ArangoDB is ready
./status.sh --health

# Manually initialize
cd backend
uv run python scripts/init_db.py
```

### Out of disk space

```bash
# Check Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a

# Remove old volumes
docker volume ls
docker volume rm <volume-name>
```

### Permission errors

```bash
# Fix script permissions
chmod +x start.sh stop.sh status.sh

# Fix data directory permissions
sudo chown -R $USER:$USER data/
```

---

## Contributing

When modifying these scripts:

1. Test changes thoroughly
2. Update this documentation
3. Maintain backward compatibility
4. Add helpful error messages
5. Follow the existing code style

---

## Support

For issues or questions:
- Check service logs: `./status.sh --logs`
- Review Docker logs: `docker compose logs`
- Verify health: `./status.sh --health`
- Restart services: `./stop.sh && ./start.sh`

---

**Last Updated:** 2025-11-16
**Version:** 1.0.0
