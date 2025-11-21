#!/bin/bash
# X-UAV Full Stack Stop Script

echo "🛑 Stopping X-UAV Platform..."

# Navigate to project root
cd "$(dirname "$0")"

# Kill backend
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    kill $BACKEND_PID 2>/dev/null
    rm .backend.pid
    echo "   ✓ Backend stopped"
fi

# Kill frontend
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    kill $FRONTEND_PID 2>/dev/null
    rm .frontend.pid
    echo "   ✓ Frontend stopped"
fi

# Kill any remaining processes
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "vite --port" 2>/dev/null

echo "✅ X-UAV Platform stopped"
