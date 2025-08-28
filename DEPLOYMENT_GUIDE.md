# 🚀 Deployment Guide

This guide covers how to run your Flask application locally and deploy it to free hosting platforms with secure environment variable management.

## 🔐 Security Features Implemented

✅ **API Key Security**: Removed hardcoded API key, now reads from `MY_API_KEY` environment variable  
✅ **Backend-Only API Access**: API key never exposed to frontend  
✅ **Secure Data Endpoint**: `/data` route fetches from third-party API using hidden key  
✅ **Frontend Integration**: AJAX/fetch calls to secure backend endpoints  

## 📁 Project Structure

```
AI-PSSWD-CRACKER/
├── app.py                 # Main Flask application (API key now secure)
├── templates/
│   └── index.html        # Frontend with API data fetching
├── static/
│   └── js/
│       └── app.js        # Updated with /data endpoint calls
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── Procfile             # For deployment platforms
└── runtime.txt          # Python version specification
```

## 🏠 Local Development Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

**Option A: Using .env file (Recommended)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your API key
MY_API_KEY=AIzaSyD5L0po7bBIKcexd9VovE5L9rUCVrVH3xY
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

**Option B: Export directly (Windows)**
```cmd
set MY_API_KEY=AIzaSyD5L0po7bBIKcexd9VovE5L9rUCVrVH3xY
set FLASK_ENV=development
```

**Option B: Export directly (Linux/Mac)**
```bash
export MY_API_KEY=AIzaSyD5L0po7bBIKcexd9VovE5L9rUCVrVH3xY
export FLASK_ENV=development
```

### 3. Run the Application
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## ☁️ Deployment to Render

### 1. Create Account
- Sign up at [render.com](https://render.com)
- Connect your GitHub repository

### 2. Create Web Service
- Click "New" → "Web Service"
- Connect your repository
- Configure:
  - **Name**: `ai-password-cracker`
  - **Environment**: `Python 3`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python app.py`

### 3. Set Environment Variables
In Render dashboard → Environment:
```
MY_API_KEY = AIzaSyD5L0po7bBIKcexd9VovE5L9rUCVrVH3xY
FLASK_ENV = production
SECRET_KEY = your-random-secret-key-here
```

### 4. Deploy
- Click "Create Web Service"
- Render will automatically deploy from your repository

## 🚂 Deployment to Railway

### 1. Create Account
- Sign up at [railway.app](https://railway.app)
- Connect your GitHub account

### 2. Deploy Project
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### 3. Set Environment Variables
```bash
railway variables set MY_API_KEY=AIzaSyD5L0po7bBIKcexd9VovE5L9rUCVrVH3xY
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-random-secret-key-here
```

## 🔧 Configuration Files

### Procfile (for deployment platforms)
```
web: python app.py
```

### runtime.txt (specify Python version)
```
python-3.11.0
```

### requirements.txt (ensure these dependencies are included)
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
# ... your other dependencies
```

## 🧪 Testing the Secure Implementation

### 1. Test API Key Security
```bash
# This should fail (no API key exposed)
curl http://localhost:5000/data

# Check browser dev tools - API key should never appear in:
# - Network requests
# - JavaScript source
# - HTML source
```

### 2. Test Data Endpoint
- Open your app in browser
- Click "Fetch API Data" button
- Verify data is fetched from backend
- Check that API key is not visible in browser dev tools

### 3. Test Environment Variable Loading
```bash
# Remove environment variable
unset MY_API_KEY

# Start app - should show error about missing API key
python app.py
```

## 🛡️ Security Best Practices Implemented

1. **Environment Variables**: API key stored in environment, not code
2. **Backend Proxy**: Frontend never directly accesses third-party API
3. **No Client-Side Secrets**: API key never sent to browser
4. **Error Handling**: Graceful handling when API key is missing
5. **HTTPS Ready**: Works with HTTPS in production

## 🔍 Troubleshooting

### API Key Not Working
```bash
# Check if environment variable is set
echo $MY_API_KEY  # Linux/Mac
echo %MY_API_KEY% # Windows

# Check app logs for initialization messages
```

### Deployment Issues
- Ensure all environment variables are set in hosting platform
- Check build logs for missing dependencies
- Verify Python version compatibility

### Frontend Not Fetching Data
- Check browser console for JavaScript errors
- Verify `/data` endpoint is accessible
- Check network tab in browser dev tools

## 📞 Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify environment variables are properly set
3. Ensure all dependencies are installed
4. Test locally before deploying

---

🎉 **Your Flask application is now secure and ready for production!**
