@echo off
echo 🚀 Kidney Anomaly Detection System - Manual Setup
echo ================================================

echo.
echo 📁 Creating directories...
if not exist "backend\models" mkdir backend\models
if not exist "backend\data\kidney_ct_scans\Normal" mkdir backend\data\kidney_ct_scans\Normal
if not exist "backend\data\kidney_ct_scans\Cyst" mkdir backend\data\kidney_ct_scans\Cyst
if not exist "backend\data\kidney_ct_scans\Stone" mkdir backend\data\kidney_ct_scans\Stone
if not exist "backend\data\kidney_ct_scans\Tumor" mkdir backend\data\kidney_ct_scans\Tumor
if not exist "backend\uploads" mkdir backend\uploads

echo.
echo 🐍 Setting up Python backend...
cd backend

echo Creating virtual environment...
python -m venv venv --without-pip

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m ensurepip --upgrade

echo Installing dependencies...
pip install -r requirements.txt

echo Creating demo model...
python create_demo_model.py

cd ..

echo.
echo 📦 Setting up Node.js frontend...
cd frontend

echo Installing dependencies...
npm install

cd ..

echo.
echo ✅ Setup completed successfully!
echo.
echo 🎉 To start the application:
echo.
echo 1. Start backend (in a new command prompt):
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. Start frontend (in another command prompt):
echo    cd frontend
echo    npm start
echo.
echo 3. Open browser and go to: http://localhost:3000
echo.
echo 4. Login with demo credentials:
echo    Email: demo@example.com
echo    Password: password123
echo.
pause
