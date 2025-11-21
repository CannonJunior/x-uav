#!/bin/bash
# X-UAV Backend Startup Script

echo "🚀 Starting X-UAV Backend Server..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if database exists
if [ ! -f "data_db/uavs.duckdb" ]; then
    echo "📋 Database not found. Initializing..."
    uv run python scripts/init_db.py
    echo ""
fi

# Start the server
echo "🌐 Starting FastAPI server on http://localhost:7676"
echo "📚 API Documentation: http://localhost:7676/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uv run uvicorn app.main:app --host 0.0.0.0 --port 7676 --reload
