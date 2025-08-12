@echo off
echo 🚀 Starting Kidney Anomaly Detection System (Simple Version)
echo ===========================================================

echo.
echo 📦 Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo 🐍 Starting Backend...
start "Backend" cmd /k "python simple_backend.py"

echo.
echo ✅ Both servers are starting...
echo.
echo 🌐 Frontend will be available at: http://localhost:3000
echo 🔧 Backend will be available at: http://localhost:5000
echo.
echo 🔑 Login credentials: demo@example.com / password123
echo.
echo ⏹️  Press any key to close this window...
pause > nul

