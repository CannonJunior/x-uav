#!/bin/bash

################################################################################
# X-UAV Application Stop Script
#
# Gracefully stops all X-UAV application services
#
# Usage: ./stop.sh [options]
#   --remove       Remove containers after stopping
#   --volumes      Also remove volumes (WARNING: deletes all data)
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse command line arguments
REMOVE=false
VOLUMES=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --remove)
            REMOVE=true
            shift
            ;;
        --volumes)
            VOLUMES=true
            REMOVE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --remove       Remove containers after stopping"
            echo "  --volumes      Also remove volumes (WARNING: deletes all data)"
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

print_header "Stopping X-UAV Application"

cd "$SCRIPT_DIR"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running"
    exit 1
fi

# Stop services
if [ "$VOLUMES" = true ]; then
    print_warning "This will stop all services and DELETE ALL DATA!"
    read -p "Are you sure? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        print_info "Stopping services and removing volumes..."
        docker compose down -v
        print_success "Services stopped and volumes removed"
    else
        print_info "Operation cancelled"
        exit 0
    fi
elif [ "$REMOVE" = true ]; then
    print_info "Stopping and removing containers..."
    docker compose down
    print_success "Services stopped and containers removed"
else
    print_info "Stopping services..."
    docker compose stop
    print_success "Services stopped"
fi

echo ""
print_info "Service status:"
docker compose ps

echo ""
print_success "X-UAV application stopped"
echo ""
print_info "To start again, run: ./start.sh"

if [ "$REMOVE" = false ]; then
    print_info "To remove containers: ./stop.sh --remove"
    print_info "To remove everything: ./stop.sh --volumes"
fi
