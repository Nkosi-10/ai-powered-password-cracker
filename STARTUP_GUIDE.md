# 🚀 AI-Powered Password Cracker Simulator - Startup Guide

## 📋 **Prerequisites**

### **Python Installation**
- **Python 3.8+** required
- Download from: https://python.org
- **IMPORTANT**: Check "Add Python to PATH" during installation

### **System Requirements**
- **Windows**: Windows 10/11 (PowerShell 5.1+)
- **Linux/Mac**: Python 3.8+ with pip
- **Memory**: Minimum 2GB RAM
- **Storage**: 100MB free space

## 🔧 **Installation Steps**

### **Step 1: Clone/Download Project**
```bash
# Navigate to project directory
cd C:\Users\HP\Desktop\new
```

### **Step 2: Install Dependencies**
```bash
# Windows (Command Prompt)
python -m pip install -r requirements.txt

# Windows (PowerShell)
py -m pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

### **Step 3: Configure API Key (Optional)**
```bash
# Copy environment template
copy config.env.example .env

# Edit .env file and add your Google Gemini API key
# Get free API key from: https://makersuite.google.com/app/apikey
```

## 🚀 **Starting the Application**

### **Method 1: Windows Batch File (Recommended)**
```bash
# Double-click start.bat
# OR run from command line:
start.bat
```

### **Method 2: Windows PowerShell**
```bash
# Right-click start.ps1 → "Run with PowerShell"
# OR run from PowerShell:
.\start.ps1
```

### **Method 3: Python Direct**
```bash
# Windows
python start.py

# Linux/Mac
python3 start.py
```

### **Method 4: Direct Flask**
```bash
# Windows
python app.py

# Linux/Mac
python3 app.py
```

## 🌐 **Accessing the Application**

1. **Open your web browser**
2. **Navigate to**: `http://localhost:5000`
3. **You should see**: Hacker-themed interface with:
   - Password cracking tools
   - USB device simulator
   - Matrix background effects

## 🧪 **Testing the Application**

### **Quick Test Script**
```bash
# Test all modules
python debug.py

# Test USB simulator only
python test_usb_simulator.py

# Interactive demo
python demo_usb.py
```

### **Manual Testing**
1. **USB Quick Setup**: Click "Quick Setup" button
2. **Create Device**: Select device type and security level
3. **Test Unlock**: Try wrong password, then correct password
4. **View Statistics**: Click "View Statistics" button

## 🐛 **Troubleshooting**

### **Issue 1: Python Not Found**
```
❌ Python was not found; run without arguments to install from the Microsoft Store
```
**Solution**:
- Install Python from https://python.org
- Check "Add Python to PATH" during installation
- Restart command prompt/PowerShell

### **Issue 2: Module Import Errors**
```
❌ ImportError: No module named 'flask'
```
**Solution**:
```bash
# Install dependencies
python -m pip install -r requirements.txt
```

### **Issue 3: Port Already in Use**
```
❌ Address already in use
```
**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID_NUMBER>
```

### **Issue 4: Permission Denied**
```
❌ Permission denied
```
**Solution**:
- Run as Administrator (Windows)
- Use `sudo` (Linux/Mac)
- Check file permissions

### **Issue 5: Browser Shows Nothing**
**Solution**:
- Check if Flask is running (should show "Running on http://0.0.0.0:5000")
- Try different browser
- Check browser console for errors (F12)

## 📱 **API Endpoints**

The application provides these REST API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main page |
| `/api/status` | GET | System status |
| `/api/fake-passwords` | GET | Sample passwords |
| `/api/attack` | POST | Run password attack |
| `/api/usb/devices` | GET/POST | USB device management |
| `/api/usb/devices/{id}/unlock` | POST | Unlock USB device |
| `/api/usb/statistics` | GET | Attack statistics |

## 🔒 **Security Features**

- **Synthetic Data Only**: Works only with fake passwords
- **Input Validation**: Checks for suspicious hash patterns
- **Rate Limiting**: Prevents abuse
- **Ethical Safeguards**: Built-in warnings and disclaimers

## 🎯 **Expected Behavior**

### **Successful Startup**
```
🚀 Starting AI-Powered Password Cracker Simulator...
✅ Simulator initialized successfully
✅ Flask app created successfully
🌐 Application will be available at: http://localhost:5000
📱 AI Features: ✅ Enabled (if API key configured)
 * Running on http://0.0.0.0:5000
```

### **Frontend Features**
- ✅ Matrix background animation
- ✅ Hacker-themed styling
- ✅ USB device simulator
- ✅ Password cracking tools
- ✅ Real-time statistics
- ✅ Responsive design

## 📞 **Getting Help**

### **Check Logs**
- **Backend**: Console output when running Python
- **Frontend**: Browser console (F12 → Console)

### **Common Commands**
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test specific module
python -c "import flask; print('Flask OK')"

# Run debug mode
python debug.py
```

### **File Structure**
```
project_root/
├── app.py              # Main Flask application
├── start.py            # Startup script
├── start.bat           # Windows batch file
├── start.ps1           # Windows PowerShell script
├── debug.py            # Debug script
├── requirements.txt    # Python dependencies
├── core/               # Core modules
├── ai/                 # AI integration
├── utils/              # Utility functions
├── static/             # Frontend assets
├── templates/          # HTML templates
└── data/               # Sample data
```

## 🎉 **Success Indicators**

When everything is working correctly:

1. **Backend**: Flask server running on port 5000
2. **Frontend**: Beautiful interface at http://localhost:5000
3. **USB Simulator**: Can create and unlock devices
4. **Password Tools**: Can generate and validate hashes
5. **No Errors**: Clean console output and browser console

## 🚨 **Important Notes**

- **Educational Use Only**: This is a simulation tool
- **No Real Data**: Works only with synthetic passwords
- **API Key**: Google Gemini API key is optional but recommended
- **Browser Support**: Modern browsers (Chrome, Firefox, Edge, Safari)
- **Network**: Application runs locally, no internet required (except for AI features)

---

**Happy Learning! 🚀🔐**
