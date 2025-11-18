#!/bin/bash

################################################################################
# X-UAV Application Status Script
#
# Shows the status of all X-UAV application services
#
# Usage: ./status.sh [options]
#   --logs [service]    Show logs for a specific service or all services
#   --health            Show detailed health information
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse command line arguments
SHOW_LOGS=false
LOG_SERVICE=""
SHOW_HEALTH=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --logs)
            SHOW_LOGS=true
            if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                LOG_SERVICE=$2
                shift
            fi
            shift
            ;;
        --health)
            SHOW_HEALTH=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --logs [service]    Show logs for a specific service or all services"
            echo "  --health            Show detailed health information"
            echo "  --help              Show this help message"
            echo ""
            echo "Available services: arangodb, postgres, redis, backend, frontend"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

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

print_service() {
    echo -e "${CYAN}● $1${NC}"
}

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running"
    exit 1
fi

cd "$SCRIPT_DIR"

print_header "X-UAV Application Status"

# Show container status
docker compose ps

echo ""

# Show individual service status
print_info "Service Details:"
echo ""

# ArangoDB
if docker ps --filter "name=x-uav-arangodb" --filter "status=running" --format '{{.Names}}' | grep -q "x-uav-arangodb"; then
    print_service "ArangoDB: ${GREEN}Running${NC}"
    echo "  URL: http://localhost:8529"
    echo "  User: root / Password: development"
else
    print_service "ArangoDB: ${RED}Stopped${NC}"
fi

# PostgreSQL
if docker ps --filter "name=x-uav-postgres" --filter "status=running" --format '{{.Names}}' | grep -q "x-uav-postgres"; then
    print_service "PostgreSQL: ${GREEN}Running${NC}"
    echo "  Host: localhost:5434"
    echo "  Database: xuav / User: xuav / Password: development"
else
    print_service "PostgreSQL: ${RED}Stopped${NC}"
fi

# Redis
if docker ps --filter "name=x-uav-redis" --filter "status=running" --format '{{.Names}}' | grep -q "x-uav-redis"; then
    print_service "Redis: ${GREEN}Running${NC}"
    echo "  Host: localhost:6379"
else
    print_service "Redis: ${RED}Stopped${NC}"
fi

# Backend
if docker ps --filter "name=x-uav-backend" --filter "status=running" --format '{{.Names}}' | grep -q "x-uav-backend"; then
    print_service "Backend API: ${GREEN}Running${NC}"
    echo "  API: http://localhost:8000"
    echo "  Docs: http://localhost:8000/docs"
else
    print_service "Backend API: ${RED}Stopped${NC}"
fi

# Frontend
if docker ps --filter "name=x-uav-frontend" --filter "status=running" --format '{{.Names}}' | grep -q "x-uav-frontend"; then
    print_service "Frontend: ${GREEN}Running${NC}"
    echo "  URL: http://localhost:7676"
else
    print_service "Frontend: ${RED}Stopped${NC}"
fi

echo ""

# Show health information if requested
if [ "$SHOW_HEALTH" = true ]; then
    print_header "Health Checks"

    # Check ArangoDB health
    if docker ps --filter "name=x-uav-arangodb" --filter "status=running" -q | grep -q .; then
        echo -n "ArangoDB: "
        if docker exec x-uav-arangodb arangosh --server.endpoint tcp://127.0.0.1:8529 --server.password development --javascript.execute-string "db._version()" >/dev/null 2>&1; then
            print_success "Healthy"
        else
            print_error "Unhealthy"
        fi
    fi

    # Check PostgreSQL health
    if docker ps --filter "name=x-uav-postgres" --filter "status=running" -q | grep -q .; then
        echo -n "PostgreSQL: "
        if docker exec x-uav-postgres pg_isready -U xuav >/dev/null 2>&1; then
            print_success "Healthy"
        else
            print_error "Unhealthy"
        fi
    fi

    # Check Redis health
    if docker ps --filter "name=x-uav-redis" --filter "status=running" -q | grep -q .; then
        echo -n "Redis: "
        if docker exec x-uav-redis redis-cli ping >/dev/null 2>&1; then
            print_success "Healthy"
        else
            print_error "Unhealthy"
        fi
    fi

    # Check Backend health
    if docker ps --filter "name=x-uav-backend" --filter "status=running" -q | grep -q .; then
        echo -n "Backend: "
        if curl -s http://localhost:8000/docs >/dev/null 2>&1; then
            print_success "Healthy"
        else
            print_warning "Starting or unhealthy"
        fi
    fi

    # Check Frontend health
    if docker ps --filter "name=x-uav-frontend" --filter "status=running" -q | grep -q .; then
        echo -n "Frontend: "
        if curl -s http://localhost:7676 >/dev/null 2>&1; then
            print_success "Healthy"
        else
            print_warning "Starting or unhealthy"
        fi
    fi

    echo ""
fi

# Show logs if requested
if [ "$SHOW_LOGS" = true ]; then
    print_header "Service Logs"

    if [ -n "$LOG_SERVICE" ]; then
        print_info "Showing logs for $LOG_SERVICE (Ctrl+C to exit)..."
        docker compose logs -f "$LOG_SERVICE"
    else
        print_info "Showing logs for all services (Ctrl+C to exit)..."
        docker compose logs -f
    fi
fi

# Show resource usage
print_header "Resource Usage"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" \
    x-uav-arangodb x-uav-postgres x-uav-redis x-uav-backend x-uav-frontend 2>/dev/null || \
    print_warning "No containers running"

echo ""

# Show helpful commands
print_info "Useful Commands:"
echo "  View logs:        ./status.sh --logs [service]"
echo "  Health check:     ./status.sh --health"
echo "  Restart services: ./start.sh"
echo "  Stop services:    ./stop.sh"
echo ""
