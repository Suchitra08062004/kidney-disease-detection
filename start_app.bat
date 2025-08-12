@echo off
echo Starting Kidney Anomaly Detection System...
echo.

echo Starting Backend Server...
cd backend
start "Backend Server" cmd /k "venv\Scripts\activate && python app.py"
cd ..

echo.
echo Starting Frontend Server...
cd frontend
start "Frontend Server" cmd /k "npm start"
cd ..

echo.
echo Servers are starting...
echo Backend: http://localhost:4000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
