#!/bin/bash

################################################################################
# X-UAV Application Startup Script
#
# This script manages the complete X-UAV application stack:
# - ArangoDB (graph database)
# - PostgreSQL (relational database)
# - Redis (cache/streams)
# - FastAPI Backend
# - Vue.js Frontend
#
# Usage: ./start.sh [options]
#   --clean        Stop all services and remove volumes
#   --db-only      Start only database services
#   --no-init      Skip database initialization
#   --rebuild      Rebuild Docker images before starting
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
BACKEND_DIR="$SCRIPT_DIR/backend"
INIT_SCRIPT="$BACKEND_DIR/scripts/init_db.py"

# Service names
SERVICES=(
    "x-uav-arangodb"
    "x-uav-postgres"
    "x-uav-redis"
    "x-uav-backend"
    "x-uav-frontend"
)

# Parse command line arguments
CLEAN=false
DB_ONLY=false
NO_INIT=false
REBUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --db-only)
            DB_ONLY=true
            shift
            ;;
        --no-init)
            NO_INIT=true
            shift
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --clean        Stop all services and remove volumes"
            echo "  --db-only      Start only database services"
            echo "  --no-init      Skip database initialization"
            echo "  --rebuild      Rebuild Docker images before starting"
            echo "  --help         Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

################################################################################
# Functions
################################################################################

print_header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if a container is running
is_container_running() {
    local container_name=$1
    docker ps --filter "name=$container_name" --filter "status=running" --format '{{.Names}}' | grep -q "^${container_name}$"
}

# Check if a container exists (running or stopped)
container_exists() {
    local container_name=$1
    docker ps -a --filter "name=$container_name" --format '{{.Names}}' | grep -q "^${container_name}$"
}

# Stop a single container
stop_container() {
    local container_name=$1

    if is_container_running "$container_name"; then
        print_info "Stopping $container_name..."
        docker stop "$container_name" >/dev/null 2>&1
        print_success "$container_name stopped"
        return 0
    elif container_exists "$container_name"; then
        print_info "$container_name already stopped"
        return 0
    else
        return 1
    fi
}

# Remove a single container
remove_container() {
    local container_name=$1

    if container_exists "$container_name"; then
        print_info "Removing $container_name..."
        docker rm -f "$container_name" >/dev/null 2>&1
        print_success "$container_name removed"
    fi
}

# Stop all application services
stop_all_services() {
    print_header "Stopping X-UAV Services"

    local stopped_any=false

    for service in "${SERVICES[@]}"; do
        if stop_container "$service"; then
            stopped_any=true
        fi
    done

    if [ "$stopped_any" = true ]; then
        print_success "All services stopped"
    else
        print_info "No services were running"
    fi
}

# Clean up containers and volumes
clean_all() {
    print_header "Cleaning X-UAV Environment"

    # Stop all services
    for service in "${SERVICES[@]}"; do
        remove_container "$service"
    done

    # Remove volumes if requested
    print_warning "Removing Docker volumes will delete all data!"
    read -p "Are you sure? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        cd "$SCRIPT_DIR"
        docker compose down -v 2>/dev/null || true
        print_success "Volumes removed"

        # Also remove local data directories
        if [ -d "$SCRIPT_DIR/data" ]; then
            print_info "Removing local data directories..."
            rm -rf "$SCRIPT_DIR/data"
            print_success "Local data removed"
        fi
    else
        print_info "Skipping volume removal"
    fi
}

# Wait for a service to be ready
wait_for_service() {
    local service_name=$1
    local max_attempts=$2
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if is_container_running "$service_name"; then
            return 0
        fi

        if [ $attempt -eq 1 ]; then
            echo -n "Waiting for $service_name"
        fi

        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done

    echo ""
    return 1
}

# Wait for ArangoDB to be ready
wait_for_arangodb() {
    print_info "Waiting for ArangoDB to be ready..."

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker exec x-uav-arangodb arangosh --server.endpoint tcp://127.0.0.1:8529 --server.password development --javascript.execute-string "db._version()" >/dev/null 2>&1; then
            echo ""
            print_success "ArangoDB is ready"
            return 0
        fi

        if [ $attempt -eq 1 ]; then
            echo -n "Checking ArangoDB"
        fi

        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo ""
    print_error "ArangoDB failed to start within timeout"
    return 1
}

# Wait for PostgreSQL to be ready
wait_for_postgres() {
    print_info "Waiting for PostgreSQL to be ready..."

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker exec x-uav-postgres pg_isready -U xuav >/dev/null 2>&1; then
            echo ""
            print_success "PostgreSQL is ready"
            return 0
        fi

        if [ $attempt -eq 1 ]; then
            echo -n "Checking PostgreSQL"
        fi

        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done

    echo ""
    print_error "PostgreSQL failed to start within timeout"
    return 1
}

# Wait for Redis to be ready
wait_for_redis() {
    print_info "Waiting for Redis to be ready..."

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker exec x-uav-redis redis-cli ping >/dev/null 2>&1; then
            echo ""
            print_success "Redis is ready"
            return 0
        fi

        if [ $attempt -eq 1 ]; then
            echo -n "Checking Redis"
        fi

        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done

    echo ""
    print_error "Redis failed to start within timeout"
    return 1
}

# Initialize databases
initialize_databases() {
    if [ "$NO_INIT" = true ]; then
        print_info "Skipping database initialization (--no-init flag)"
        return 0
    fi

    print_header "Initializing Databases"

    # Check if init script exists
    if [ ! -f "$INIT_SCRIPT" ]; then
        print_warning "Database initialization script not found: $INIT_SCRIPT"
        return 1
    fi

    # Initialize ArangoDB
    print_info "Initializing ArangoDB schema and data..."
    cd "$BACKEND_DIR"

    if uv run python "$INIT_SCRIPT"; then
        print_success "Database initialization completed"
    else
        print_error "Database initialization failed"
        return 1
    fi
}

# Start database services only
start_databases() {
    print_header "Starting Database Services"

    cd "$SCRIPT_DIR"

    # Start only database services
    print_info "Starting ArangoDB, PostgreSQL, and Redis..."

    docker compose up -d arangodb postgres redis

    # Wait for services to be ready
    wait_for_service "x-uav-arangodb" 30 && echo ""
    wait_for_arangodb

    wait_for_service "x-uav-postgres" 30 && echo ""
    wait_for_postgres

    wait_for_service "x-uav-redis" 30 && echo ""
    wait_for_redis

    print_success "Database services started"
}

# Start all services
start_all_services() {
    print_header "Starting X-UAV Application"

    cd "$SCRIPT_DIR"

    # Build images if requested
    if [ "$REBUILD" = true ]; then
        print_info "Rebuilding Docker images..."
        docker compose build
        print_success "Images rebuilt"
    fi

    # Start all services
    print_info "Starting all services..."
    docker compose up -d

    # Wait for databases to be ready
    wait_for_service "x-uav-arangodb" 30 && echo ""
    wait_for_arangodb

    wait_for_service "x-uav-postgres" 30 && echo ""
    wait_for_postgres

    wait_for_service "x-uav-redis" 30 && echo ""
    wait_for_redis

    # Wait for backend and frontend
    wait_for_service "x-uav-backend" 30 && echo ""
    print_success "Backend service started"

    wait_for_service "x-uav-frontend" 30 && echo ""
    print_success "Frontend service started"

    print_success "All services started"
}

# Show service status
show_status() {
    print_header "Service Status"

    docker compose ps

    echo ""
    print_info "Service URLs:"
    echo "  Frontend:  http://localhost:7676"
    echo "  Backend:   http://localhost:8000"
    echo "  API Docs:  http://localhost:8000/docs"
    echo "  ArangoDB:  http://localhost:8529 (root / development)"
    echo "  PostgreSQL: localhost:5432 (xuav / development)"
    echo "  Redis:     localhost:6379"
    echo ""
}

# Show logs
show_logs() {
    print_info "Showing service logs (Ctrl+C to exit)..."
    docker compose logs -f
}

################################################################################
# Main Script
################################################################################

print_header "X-UAV Application Manager"

# Check Docker
check_docker

# Handle clean mode
if [ "$CLEAN" = true ]; then
    clean_all
    exit 0
fi

# Stop any existing services
stop_all_services

# Start services based on mode
if [ "$DB_ONLY" = true ]; then
    start_databases
    initialize_databases
else
    start_all_services
    initialize_databases
fi

# Show status
show_status

# Ask if user wants to see logs
echo ""
read -p "Would you like to view service logs? (y/n): " view_logs

if [ "$view_logs" = "y" ] || [ "$view_logs" = "Y" ]; then
    show_logs
else
    print_success "X-UAV application started successfully!"
    print_info "Use 'docker compose logs -f' to view logs"
    print_info "Use 'docker compose down' to stop all services"
fi
