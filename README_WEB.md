# 🔐 AI-Powered Password Cracker Simulator - Web Application

A **professional-grade web application** that demonstrates AI-powered password cracking simulation in any modern browser. Built with Flask backend and a stunning hacker-themed UI.

## 🚨 ETHICAL DISCLAIMER

**This project is for EDUCATIONAL PURPOSES ONLY.**
- It ONLY works with synthetic/fake password hashes
- It CANNOT crack real passwords or real systems
- It is designed to teach cybersecurity concepts safely
- Use only in controlled, educational environments

## 🌟 Features

### 🎨 **Professional Hacker-Themed UI**
- **Matrix-style background effects** with animated characters
- **Glowing green accents** and cyberpunk aesthetics
- **Responsive design** that works on all devices
- **Smooth animations** and hover effects
- **Professional typography** using Orbitron and Share Tech Mono fonts

### 🚀 **Robust Backend**
- **Flask-based API** with comprehensive error handling
- **CORS support** for cross-origin requests
- **Rate limiting** and input validation
- **Automatic fallbacks** when AI is unavailable
- **Health monitoring** and status endpoints

### 🧠 **AI-Powered Features**
- **Google Gemini integration** for intelligent attack selection
- **Context-aware password guessing**
- **AI analysis and recommendations**
- **Fallback mechanisms** for reliability

### 🛡️ **Security & Safety**
- **Input validation** and sanitization
- **Suspicious hash detection**
- **Ethical safeguards** built-in
- **Audit logging** for all operations

## 🏗️ Architecture

```
Web Application Structure:
├── app.py                 # Flask backend server
├── templates/            # HTML templates
│   └── index.html       # Main application page
├── static/              # Static assets
│   └── js/             # JavaScript files
│       └── app.js      # Frontend application logic
├── core/                # Core cracking algorithms
├── ai/                  # AI-powered decision making
├── utils/               # Utility functions
└── data/                # Synthetic data files
```

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Configure API Key**
```bash
# TODO: ADD YOUR GOOGLE GEMINI API KEY HERE
# In app.py, replace 'your_api_key_here' with your actual API key
export GOOGLE_API_KEY="your_actual_gemini_api_key"
```

### 3. **Run the Application**
```bash
python app.py
```

### 4. **Open in Browser**
Navigate to: `http://localhost:5000`

## 🌐 Deployment

### **Local Development**
```bash
python app.py
```

### **Production with Gunicorn**
```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

### **Heroku Deployment**
```bash
# The Procfile and runtime.txt are already configured
git push heroku main
```

### **Docker Deployment**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Required for AI features
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional configuration
PORT=5000
FLASK_ENV=production
DEBUG=False
```

### **API Key Setup**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free API key
3. Set the environment variable:
   ```bash
   export GOOGLE_API_KEY="your_key_here"
   ```

## 📱 User Interface

### **Main Features**
- **Hash Input**: Enter target hashes or use pre-generated ones
- **Method Selection**: Choose from 4 attack strategies
- **Real-time Validation**: Instant hash format checking
- **Progress Tracking**: Visual attack progress indicators
- **Results Display**: Comprehensive attack statistics
- **System Status**: Live backend and AI module monitoring

### **Attack Methods**
1. **📚 Dictionary Attack**: Common passwords and variations
2. **🎯 Rule-Based Attack**: Pattern-based password generation
3. **🔨 Brute Force Attack**: Character combination testing (limited to 6 chars)
4. **🧠 AI-Powered Attack**: Intelligent strategy selection

### **User Experience**
- **One-click hash copying** from sample database
- **Quick hash generation** from plain text passwords
- **Real-time feedback** and notifications
- **Responsive design** for mobile and desktop
- **Keyboard shortcuts** (Enter key support)

## 🔌 API Endpoints

### **Status & Health**
- `GET /` - Main application page
- `GET /api/status` - System status and AI availability
- `GET /health` - Health check endpoint
- `GET /api/fake-passwords` - List of synthetic passwords

### **Core Operations**
- `POST /api/attack` - Execute password attack
- `POST /api/generate-hash` - Generate hash from password
- `POST /api/validate-hash` - Validate hash format

## 🧪 Testing

### **Run Tests**
```bash
python -m pytest tests/
```

### **Test Coverage**
```bash
python -m pytest --cov=. tests/
```

### **Manual Testing**
1. Start the application
2. Open browser to `http://localhost:5000`
3. Try different attack methods
4. Test with various hash formats
5. Verify AI functionality (if API key configured)

## 🚀 Performance Features

### **Optimizations**
- **Asynchronous operations** for better responsiveness
- **Progress simulation** for user engagement
- **Efficient hash validation** and processing
- **Memory management** for large operations
- **Rate limiting** to prevent abuse

### **Scalability**
- **Multi-threaded backend** with Gunicorn
- **Stateless API design** for horizontal scaling
- **Efficient data structures** for performance
- **Caching strategies** for repeated operations

## 🔒 Security Features

### **Input Validation**
- **Hash format verification** (length, characters)
- **Suspicious pattern detection** (bcrypt, scrypt, etc.)
- **Length restrictions** for brute force attacks
- **Content type validation** for API requests

### **Ethical Safeguards**
- **Real hash detection** and warnings
- **Educational purpose enforcement**
- **Audit logging** for accountability
- **Rate limiting** to prevent abuse

## 🎯 Use Cases

### **Educational**
- **Cybersecurity courses** and training
- **Password security awareness**
- **Attack methodology understanding**
- **Defensive programming practice**

### **Professional**
- **Security testing** in controlled environments
- **Penetration testing** training
- **Security research** and development
- **Portfolio demonstration**

### **Research**
- **AI applications** in cybersecurity
- **Password strength analysis**
- **Attack pattern research**
- **Security tool development**

## 🛠️ Troubleshooting

### **Common Issues**

#### **AI Module Not Available**
```
Error: AI module not available. Please configure your API key.
```
**Solution**: Set the `GOOGLE_API_KEY` environment variable

#### **Backend Connection Failed**
```
Error: Failed to check system status
```
**Solution**: Ensure the Flask server is running and accessible

#### **Hash Validation Errors**
```
Error: Invalid hash format
```
**Solution**: Use 64-character SHA-256 hashes or pre-generated samples

### **Debug Mode**
```bash
export FLASK_ENV=development
export DEBUG=True
python app.py
```

## 📊 Monitoring

### **Health Checks**
- **Backend status** monitoring
- **AI module availability** tracking
- **Fake data loading** verification
- **Response time** measurement

### **Logging**
- **Attack attempts** and results
- **Error tracking** and debugging
- **Performance metrics** collection
- **Security event** monitoring

## 🔮 Future Enhancements

### **Planned Features**
- **Real-time collaboration** between users
- **Advanced AI models** integration
- **Custom attack rule** creation
- **Performance benchmarking** tools
- **Export functionality** for results

### **Technical Improvements**
- **WebSocket support** for real-time updates
- **GraphQL API** for flexible queries
- **Microservices architecture** for scalability
- **Advanced caching** strategies
- **Machine learning** model training

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Add tests for new functionality
6. Submit a pull request

### **Code Standards**
- **PEP 8 compliance** for Python code
- **ESLint standards** for JavaScript
- **Comprehensive testing** coverage
- **Documentation updates** for changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Legal Notice

This software is provided "as is" without warranty. Users are responsible for ensuring compliance with local laws and regulations. The authors are not liable for any misuse of this software.

## 🆘 Support

### **Getting Help**
- **Documentation**: Check this README and inline code comments
- **Issues**: Create GitHub issues for bugs or feature requests
- **Discussions**: Use GitHub discussions for questions
- **Security**: Report security issues privately

### **Community**
- **GitHub**: [Repository Link]
- **Discussions**: [Community Forum]
- **Wiki**: [Documentation Wiki]
- **Examples**: [Code Examples]

---

## 🎉 Ready to Hack (Ethically)?

Your AI-Powered Password Cracker Simulator is now ready to run in any web browser! 

**Remember**: This tool is for education and portfolio demonstration only. Never use it on real systems or real data.

**Happy Learning! 🚀**
