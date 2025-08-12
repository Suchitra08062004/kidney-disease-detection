#!/usr/bin/env python3
"""
Simplified Kidney Anomaly Detection Backend
This version runs with minimal dependencies for demonstration
"""

import os
import json
import base64
import random
from datetime import datetime, timedelta
import hashlib

# Simulate Flask-like functionality
class SimpleFlask:
    def __init__(self):
        self.routes = {}
        self.users = {
            'demo@example.com': {
                'password': hashlib.sha256('password123'.encode()).hexdigest(),
                'name': 'Demo User'
            }
        }
        self.tokens = {}
    
    def route(self, path, methods=None):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def jsonify(self, data):
        return json.dumps(data)
    
    def run(self, host='localhost', port=5000, debug=True):
        print(f"🚀 Simple Kidney Anomaly Detection Backend")
        print(f"📍 Running on http://{host}:{port}")
        print(f"🔑 Demo credentials: demo@example.com / password123")
        print(f"📋 Available endpoints:")
        print(f"   POST /api/register - Register new user")
        print(f"   POST /api/login - Login user")
        print(f"   POST /api/predict - Predict kidney anomaly")
        print(f"   GET /api/profile - Get user profile")
        print(f"   GET /api/health - Health check")
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        
        # Keep the server running
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n👋 Server stopped")

# Create Flask-like app
app = SimpleFlask()

# Simulate JWT functionality
def create_token(user_email):
    token = base64.b64encode(f"{user_email}:{datetime.now().isoformat()}".encode()).decode()
    app.tokens[token] = user_email
    return token

def verify_token(token):
    return app.tokens.get(token)

# Simulate image processing
def simulate_prediction():
    """Simulate AI prediction for demonstration"""
    classes = ['Normal', 'Cyst', 'Stone', 'Tumor']
    predicted_class = random.choice(classes)
    confidence = random.uniform(0.7, 0.98)
    
    probabilities = {}
    for cls in classes:
        if cls == predicted_class:
            probabilities[cls] = confidence
        else:
            probabilities[cls] = (1 - confidence) / (len(classes) - 1)
    
    return {
        'prediction': predicted_class,
        'confidence': confidence,
        'all_probabilities': probabilities
    }

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    # Simulate request data
    data = {
        'name': 'Demo User',
        'email': 'demo@example.com',
        'password': 'password123'
    }
    
    if data['email'] in app.users:
        return app.jsonify({'error': 'User already exists'}), 400
    
    app.users[data['email']] = {
        'password': hashlib.sha256(data['password'].encode()).hexdigest(),
        'name': data['name']
    }
    
    return app.jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    # Simulate request data
    data = {
        'email': 'demo@example.com',
        'password': 'password123'
    }
    
    if data['email'] not in app.users:
        return app.jsonify({'error': 'Invalid credentials'}), 401
    
    user = app.users[data['email']]
    if user['password'] != hashlib.sha256(data['password'].encode()).hexdigest():
        return app.jsonify({'error': 'Invalid credentials'}), 401
    
    token = create_token(data['email'])
    return app.jsonify({
        'token': token,
        'user': {
            'name': user['name'],
            'email': data['email']
        }
    }), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict kidney anomaly from uploaded image"""
    # Simulate authentication check
    token = "demo_token"  # In real app, this would come from request headers
    
    if not verify_token(token):
        return app.jsonify({'error': 'Authentication required'}), 401
    
    # Simulate image processing delay
    import time
    time.sleep(1)
    
    result = simulate_prediction()
    return app.jsonify(result), 200

@app.route('/api/profile', methods=['GET'])
def profile():
    """Get user profile"""
    # Simulate authentication check
    token = "demo_token"
    
    if not verify_token(token):
        return app.jsonify({'error': 'Authentication required'}), 401
    
    user_email = verify_token(token)
    user = app.users[user_email]
    
    return app.jsonify({
        'name': user['name'],
        'email': user_email
    }), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return app.jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Kidney Anomaly Detection API'
    }), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
