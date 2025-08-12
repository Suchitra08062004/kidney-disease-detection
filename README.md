# Kidney Anomaly Detection System

A full-stack AI-powered web application for detecting kidney anomalies from CT scan images using deep learning and computer vision techniques.

## 🏥 Project Overview

This application uses a MobileNetV2-based deep learning model to classify kidney CT scan images into four categories:
- **Normal**: Healthy kidney tissue
- **Cyst**: Fluid-filled sacs in kidney tissue
- **Stone**: Hard mineral deposits
- **Tumor**: Abnormal cell growth

## 🚀 Features

### AI Model
- **MobileNetV2** with transfer learning for efficient image classification
- Pre-trained on ImageNet and fine-tuned for medical imaging
- Real-time prediction with confidence scores
- Support for multiple image formats (JPG, PNG, JPEG)

### Backend (Flask API)
- RESTful API endpoints for image processing
- JWT-based authentication system
- Secure file upload handling
- Image preprocessing and normalization
- Model inference with confidence scoring

### Frontend (React.js)
- Modern, responsive UI with drag-and-drop file upload
- Real-time image preview and analysis
- Interactive charts and visualizations
- User authentication and session management
- Results history and comparison

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep learning framework
- **MobileNetV2** - Pre-trained CNN model
- **Pillow** - Image processing
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React.js 18** - Frontend framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **React Dropzone** - File upload
- **Chart.js** - Data visualization
- **React Toastify** - Notifications

## 📁 Project Structure

```
kidney-anomaly-detection/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── train_model.py         # Model training script
│   ├── requirements.txt       # Python dependencies
│   ├── models/               # Trained model storage
│   ├── data/                 # Training data directory
│   └── uploads/              # Temporary upload storage
├── frontend/
│   ├── public/
│   │   └── index.html        # Main HTML file
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # Authentication context
│   │   ├── App.js           # Main app component
│   │   └── index.js         # App entry point
│   ├── package.json         # Node.js dependencies
│   └── README.md           # Frontend documentation
└── README.md               # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm** or **yarn**
- **Git**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kidney-anomaly-detection
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir models data uploads
mkdir data/kidney_ct_scans
mkdir data/kidney_ct_scans/Normal
mkdir data/kidney_ct_scans/Cyst
mkdir data/kidney_ct_scans/Stone
mkdir data/kidney_ct_scans/Tumor
```

### 3. Model Training (Optional)

If you have training data, you can train the model:

```bash
# Place your CT scan images in the appropriate folders:
# data/kidney_ct_scans/Normal/ - for normal kidney images
# data/kidney_ct_scans/Cyst/ - for cyst images
# data/kidney_ct_scans/Stone/ - for kidney stone images
# data/kidney_ct_scans/Tumor/ - for tumor images

# Run training script
python train_model.py
```

**Note**: If you don't have training data, the application will work with a pre-trained model or you can use the demo mode.

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 5. Start Backend Server

```bash
# In a new terminal, navigate to backend directory
cd backend

# Activate virtual environment (if not already activated)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start Flask server
python app.py
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 🔐 Authentication

The application includes a demo account for testing:

- **Email**: admin@example.com
- **Password**: admin123

You can also register new accounts through the registration page.

## 📊 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile (requires authentication)

### Image Analysis
- `POST /api/predict` - Upload and analyze CT scan image (requires authentication)
- `GET /api/health` - Health check endpoint

## 🎯 Usage Guide

### 1. Login/Register
- Access the application at http://localhost:3000
- Use the demo credentials or register a new account

### 2. Upload CT Scan
- Navigate to the "Upload Scan" page
- Drag and drop or click to select a CT scan image
- Supported formats: JPG, PNG, JPEG (max 16MB)
- Click "Analyze Image" to process

### 3. View Results
- Results are displayed immediately after analysis
- View confidence scores for all classes
- Interactive charts show probability distribution
- Results are saved locally for future reference

### 4. Results History
- Access previous analyses from the "Results" page
- Compare different scans and their predictions
- View detailed confidence breakdowns

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
```

### Model Configuration

The model can be configured in `backend/train_model.py`:

- **Input size**: 224x224 pixels
- **Classes**: 4 (Normal, Cyst, Stone, Tumor)
- **Model**: MobileNetV2 with transfer learning
- **Optimizer**: Adam with learning rate scheduling

## 🧪 Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 📈 Model Performance

The MobileNetV2 model typically achieves:
- **Accuracy**: 85-95% (depending on data quality)
- **Inference Time**: < 2 seconds per image
- **Model Size**: ~14MB (compressed)

## 🔒 Security Features

- JWT-based authentication
- Secure file upload validation
- CORS protection
- Input sanitization
- Temporary file storage (no permanent storage)

## 🚀 Deployment

### Backend Deployment (Heroku)

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

### Frontend Deployment (Netlify)

```bash
# Build the application
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and research purposes only. The AI predictions should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for medical decisions.

## 🆘 Support

If you encounter any issues:

1. Check the console for error messages
2. Ensure all dependencies are installed correctly
3. Verify that both backend and frontend servers are running
4. Check that the model file exists in the `backend/models/` directory

For additional support, please open an issue on the GitHub repository.

## 📚 Additional Resources

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)
