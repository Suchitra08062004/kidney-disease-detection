from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# In-memory user storage (replace with database in production)
users = {
    'admin@example.com': {
        'password': generate_password_hash('admin123'),
        'name': 'Admin User'
    }
}

# Load the trained model
model = None
try:
    model = tf.keras.models.load_model('models/kidney_anomaly_model.h5')
    print("Model loaded successfully")
except:
    print("Model not found. Please train the model first.")

# Class labels
CLASS_LABELS = ['Normal', 'Cyst', 'Stone', 'Tumor']

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        # Load and resize image
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if email in users:
            return jsonify({'error': 'User already exists'}), 409
        
        users[email] = {
            'password': generate_password_hash(password),
            'name': name
        }
        
        return jsonify({'message': 'User registered successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = users.get(email)
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=email)
        return jsonify({
            'access_token': access_token,
            'user': {
                'email': email,
                'name': user['name']
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
@jwt_required()
def predict():
    """Predict kidney anomaly from uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        if model is None:
            return jsonify({'error': 'Model not loaded. Please contact administrator.'}), 500
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess image
        processed_image = preprocess_image(filepath)
        if processed_image is None:
            return jsonify({'error': 'Error processing image'}), 500
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Clean up uploaded file
        os.remove(filepath)
        
        result = {
            'prediction': CLASS_LABELS[predicted_class],
            'confidence': confidence,
            'all_probabilities': {
                CLASS_LABELS[i]: float(predictions[0][i]) 
                for i in range(len(CLASS_LABELS))
            }
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        current_user_email = get_jwt_identity()
        user = users.get(current_user_email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'email': current_user_email,
            'name': user['name']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
