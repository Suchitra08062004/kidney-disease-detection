#!/usr/bin/env python3
"""
Setup script for Kidney Anomaly Detection System
This script automates the initial setup process
"""

import os
import sys
import subprocess
import platform
import shutil

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Error: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'backend/models',
        'backend/data/kidney_ct_scans/Normal',
        'backend/data/kidney_ct_scans/Cyst',
        'backend/data/kidney_ct_scans/Stone',
        'backend/data/kidney_ct_scans/Tumor',
        'backend/uploads'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def setup_backend():
    """Setup the backend environment"""
    print("\n=== Setting up Backend ===")
    
    # Check if Python is installed
    if not run_command("python --version"):
        print("Error: Python is not installed or not in PATH")
        return False
    
    # Try different methods to create virtual environment
    venv_created = False
    
    # Method 1: Try standard venv
    print("Attempting to create virtual environment (Method 1)...")
    if run_command("python -m venv backend/venv"):
        venv_created = True
        print("✅ Virtual environment created successfully!")
    
    # Method 2: Try with --without-pip flag
    if not venv_created:
        print("Attempting to create virtual environment (Method 2)...")
        if run_command("python -m venv backend/venv --without-pip"):
            venv_created = True
            print("✅ Virtual environment created successfully!")
    
    # Method 3: Try using virtualenv if available
    if not venv_created:
        print("Attempting to create virtual environment (Method 3)...")
        if run_command("pip install virtualenv"):
            if run_command("virtualenv backend/venv"):
                venv_created = True
                print("✅ Virtual environment created successfully!")
    
    if not venv_created:
        print("❌ Failed to create virtual environment")
        print("Please try manual setup or install virtualenv:")
        print("pip install virtualenv")
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "backend\\venv\\Scripts\\activate"
        pip_cmd = "backend\\venv\\Scripts\\pip"
        python_cmd = "backend\\venv\\Scripts\\python"
    else:
        activate_cmd = "source backend/venv/bin/activate"
        pip_cmd = "backend/venv/bin/pip"
        python_cmd = "backend/venv/bin/python"
    
    # Upgrade pip first
    print("Upgrading pip...")
    run_command(f"{pip_cmd} install --upgrade pip")
    
    print("Installing Python dependencies...")
    if not run_command(f"{pip_cmd} install -r backend/requirements.txt"):
        print("Error: Failed to install Python dependencies")
        return False
    
    # Create demo model
    print("Creating demo model...")
    if not run_command(f"{python_cmd} backend/create_demo_model.py"):
        print("Error: Failed to create demo model")
        return False
    
    print("Backend setup completed successfully!")
    return True

def setup_frontend():
    """Setup the frontend environment"""
    print("\n=== Setting up Frontend ===")
    
    # Check if Node.js is installed
    if not run_command("node --version"):
        print("Error: Node.js is not installed or not in PATH")
        return False
    
    # Check if npm is installed
    if not run_command("npm --version"):
        print("Error: npm is not installed or not in PATH")
        return False
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd="frontend"):
        print("Error: Failed to install Node.js dependencies")
        return False
    
    print("Frontend setup completed successfully!")
    return True

def main():
    """Main setup function"""
    print("🚀 Kidney Anomaly Detection System Setup")
    print("=" * 50)
    
    # Create directories
    print("Creating project directories...")
    create_directories()
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed!")
        print("\n🔧 Manual Setup Instructions:")
        print("1. cd backend")
        print("2. python -m venv venv --without-pip")
        print("3. venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)")
        print("4. pip install --upgrade pip")
        print("5. pip install -r requirements.txt")
        print("6. python create_demo_model.py")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed!")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\n🎉 Next steps:")
    print("1. Start the backend server:")
    if platform.system() == "Windows":
        print("   cd backend")
        print("   venv\\Scripts\\activate")
        print("   python app.py")
    else:
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   python app.py")
    
    print("\n2. Start the frontend server:")
    print("   cd frontend")
    print("   npm start")
    
    print("\n3. Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:5000")
    
    print("\n4. Login with demo credentials:")
    print("   Email: demo@example.com")
    print("   Password: password123")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
