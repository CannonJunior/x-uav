#!/bin/bash
# X-UAV Full Stack Startup Script

echo "======================================"
echo "🚀 Starting X-UAV Platform"
echo "======================================"
echo ""

# Navigate to project root
cd "$(dirname "$0")"

# Start backend
echo "📦 Starting Backend API..."
cd backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8877 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Backend API: http://localhost:8877"
echo ""

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
sleep 3
echo ""

echo "======================================"
echo "✅ X-UAV Platform Started"
echo "======================================"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:7677"
echo "   Backend API: http://localhost:8877"
echo "   API Docs: http://localhost:8877/docs"
echo ""
echo "📊 Database: 16 UAVs from 6 countries"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Save PIDs for cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for Ctrl+C
wait
