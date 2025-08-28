# 🔐 AI-Powered Password Cracker Simulator

> **Educational Cybersecurity Tool - Synthetic Data Only**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![AI](https://img.shields.io/badge/AI-Gemini-orange.svg)](https://ai.google.dev/gemini)
[![Security](https://img.shields.io/badge/Security-Educational-brightgreen.svg)](https://en.wikipedia.org/wiki/Security)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚨 ETHICAL DISCLAIMER

**This project is for EDUCATIONAL PURPOSES ONLY.**
- It ONLY works with synthetic/fake password hashes
- It CANNOT crack real passwords or real systems
- It is designed to teach cybersecurity concepts safely
- Use only in controlled, educational environments
- **NEVER attempt to crack real passwords or real devices**

## 🌟 Project Overview

The AI-Powered Password Cracker Simulator is a comprehensive educational tool that demonstrates various password cracking techniques in a safe, controlled environment. Built with modern web technologies, it features a hacker-themed interface and AI-powered decision-making capabilities.

### 🎯 Key Features

- **🔒 Multiple Attack Methods**: Dictionary, Rule-based, Brute Force, and AI-powered attacks
- **🧠 AI Integration**: Google Gemini AI for intelligent attack strategy selection
- **💾 USB Device Simulation**: Simulate password-protected USB devices with different security levels
- **🎨 Hacker-Themed UI**: Matrix background effects and cyberpunk aesthetics
- **📊 Real-time Statistics**: Track attack success rates and performance metrics
- **🛡️ Ethical Safeguards**: Built-in protections against real password cracking
- **🌐 Web-Based Interface**: Accessible from any modern web browser
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface Layer                      │
├─────────────────────────────────────────────────────────────┤
│  HTML5 + CSS3 + JavaScript + Bootstrap + Font Awesome     │
│  Matrix Background Effects + Responsive Design            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend API                       │
├─────────────────────────────────────────────────────────────┤
│  RESTful Endpoints + Error Handling + Request Validation  │
│  CORS Support + JSON Response Format                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Simulation Engine                   │
├─────────────────────────────────────────────────────────────┤
│  Password Cracking Modules + USB Device Simulator         │
│  Hash Utilities + Configuration Management                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Decision Engine                      │
├─────────────────────────────────────────────────────────────┤
│  Google Gemini Integration + Attack Strategy Selection    │
│  Password Generation + Context Analysis                   │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
project_root/
├── app.py                          # Main Flask application
├── start.py                        # Startup script with CLI options
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment configuration
├── runtime.txt                     # Python version specification
├── .env.example                    # Environment variables template
├── README.md                       # This comprehensive documentation
│
├── core/                           # Core password cracking modules
│   ├── __init__.py                # Package initialization
│   ├── brute_force.py             # Brute force attack implementation
│   ├── dictionary_attack.py       # Dictionary-based attack
│   ├── rule_based.py              # Rule-based password generation
│   └── usb_simulator.py           # USB device simulation
│
├── ai/                             # AI-powered features
│   ├── __init__.py                # AI package initialization
│   └── ai_guesser.py              # Google Gemini integration
│
├── utils/                          # Utility functions
│   ├── __init__.py                # Utils package initialization
│   ├── hash_utils.py              # Password hashing utilities
│   └── config.py                  # Configuration constants
│
├── data/                           # Synthetic data storage
│   ├── fake_passwords.json        # Pre-generated fake passwords
│   └── wordlist.txt               # Common password dictionary
│
├── results/                        # Simulation results
│   └── log.json                   # Attack attempt logs
│
├── templates/                      # HTML templates
│   └── index.html                 # Main application interface
│
├── static/                         # Static assets
│   └── js/
│       └── app.js                 # Frontend JavaScript logic
│
└── tests/                          # Test files
    └── test_simulator.py          # Basic functionality tests
```

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+** (3.11 recommended)
- **pip** (Python package manager)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Google Gemini API key** (free tier available)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-password-cracker-simulator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Gemini API key
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

**Get your free API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run the Application

```bash
# Development mode
python start.py

# Or production mode
python start.py --production

# Run tests
python start.py --test
```

### 4. Access the Application

Open your browser and navigate to: **http://localhost:5000**

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | None | Yes |
| `PORT` | Server port | 5000 | No |
| `DEBUG` | Debug mode | False | No |
| `HOST` | Server host | 0.0.0.0 | No |

### Security Settings

The application includes multiple security layers:

- **Input Validation**: All user inputs are validated and sanitized
- **Hash Pattern Detection**: Automatically detects and blocks real password hashes
- **Rate Limiting**: Built-in protection against abuse
- **CORS Configuration**: Secure cross-origin resource sharing
- **Error Handling**: Comprehensive error handling without information leakage

## 🎮 Usage Guide

### Basic Password Cracking

1. **Enter Target Hash**: Use a 64-character SHA-256 hash (synthetic only)
2. **Select Attack Method**: Choose from available cracking strategies
3. **Configure Options**: Set method-specific parameters
4. **Launch Attack**: Click "Start Attack" and monitor progress
5. **View Results**: Analyze success/failure and performance metrics

### USB Device Simulation

1. **Create Devices**: Generate simulated USB devices with different security levels
2. **Quick Setup**: Use pre-configured devices for immediate testing
3. **Detect Devices**: Simulate device detection and analysis
4. **Attempt Unlock**: Try different passwords and observe lockout behavior
5. **Monitor Statistics**: Track success rates and attack patterns

### Attack Methods Explained

#### 📚 Dictionary Attack
- **Purpose**: Test common passwords and variations
- **Best For**: Weak passwords, common patterns
- **Speed**: Fastest method
- **Success Rate**: High for weak passwords

#### 🎯 Rule-Based Attack
- **Purpose**: Generate passwords based on common patterns
- **Best For**: Pattern-based passwords, user behavior
- **Speed**: Medium
- **Success Rate**: Medium to high

#### 🔨 Brute Force Attack
- **Purpose**: Try all possible character combinations
- **Best For**: Short passwords, unknown patterns
- **Speed**: Slowest (exponential growth)
- **Success Rate**: Guaranteed (given enough time)

#### 🧠 AI-Powered Attack
- **Purpose**: Intelligent password generation and strategy selection
- **Best For**: Complex passwords, context-aware cracking
- **Speed**: Variable (depends on AI response)
- **Success Rate**: Highest (when AI is available)

## 🔌 API Endpoints

### Core Password Cracking

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/attack` | POST | Launch password cracking attack |
| `/api/hash` | POST | Generate hash from password |
| `/api/validate` | POST | Validate hash format |
| `/api/status` | GET | Check system status |

### USB Device Simulation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/usb/devices` | GET | List all simulated devices |
| `/api/usb/devices` | POST | Create new simulated device |
| `/api/usb/devices/{id}/detect` | POST | Detect specific device |
| `/api/usb/devices/{id}/unlock` | POST | Attempt device unlock |
| `/api/usb/devices/{id}/info` | GET | Get device information |
| `/api/usb/devices/{id}/reset` | POST | Reset device lockout |
| `/api/usb/statistics` | GET | Get attack statistics |
| `/api/usb/quick-setup` | POST | Setup pre-configured devices |

### Response Format

All API endpoints return JSON responses with consistent structure:

```json
{
  "success": true/false,
  "message": "Human-readable message",
  "data": {}, // Optional data payload
  "error": "Error description if success=false"
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python start.py --test

# Run specific test file
python -m pytest tests/test_simulator.py

# Run with coverage
python -m pytest --cov=core --cov=ai --cov=utils tests/
```

### Test Coverage

The test suite covers:
- ✅ Hash utility functions
- ✅ Password cracking algorithms
- ✅ USB device simulation
- ✅ Input validation
- ✅ Error handling
- ✅ API endpoints

## 🚀 Deployment

### Local Development

```bash
python start.py
# Application available at http://localhost:5000
```

### Production Deployment

```bash
# Using Gunicorn
gunicorn app:app -w 4 -b 0.0.0.0:5000

# Using start script
python start.py --production
```

### Cloud Deployment

#### Heroku
```bash
# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

#### Docker
```bash
# Build and run with Docker
docker build -t password-simulator .
docker run -p 5000:5000 password-simulator
```

## 🔒 Security Features

### Built-in Protections

1. **Real Hash Detection**: Automatically identifies and blocks real password hashes
2. **Input Sanitization**: All user inputs are validated and sanitized
3. **Rate Limiting**: Prevents abuse and excessive API calls
4. **Error Handling**: Secure error messages without information leakage
5. **CORS Configuration**: Secure cross-origin resource sharing

### Ethical Safeguards

- **Synthetic Data Only**: Cannot process real passwords or hashes
- **Educational Purpose**: Designed for learning, not real attacks
- **Warning Messages**: Clear disclaimers about intended use
- **Audit Logging**: All activities are logged for review

## 📊 Performance Metrics

### Benchmarks

| Attack Method | Speed | Memory Usage | Success Rate |
|---------------|-------|--------------|--------------|
| Dictionary | ~1000 passwords/sec | Low | 60-80% |
| Rule-based | ~500 passwords/sec | Low | 40-70% |
| Brute Force | ~100 passwords/sec | Medium | 100% (given time) |
| AI-powered | Variable | Low | 70-90% |

### Optimization Tips

1. **Use appropriate attack methods** for your target
2. **Limit brute force length** to reasonable values
3. **Enable AI features** for complex scenarios
4. **Monitor system resources** during long attacks

## 🐛 Troubleshooting

### Common Issues

#### API Key Problems
```bash
# Check API key configuration
echo $GOOGLE_API_KEY

# Verify in .env file
cat .env
```

#### Port Conflicts
```bash
# Check if port is in use
netstat -an | grep :5000

# Use different port
export PORT=5001
python start.py
```

#### Dependencies Issues
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt

# Check Python version
python --version
```

#### Browser Compatibility
- Ensure JavaScript is enabled
- Use modern browser (Chrome 90+, Firefox 88+, Safari 14+)
- Clear browser cache if issues persist

### Debug Mode

```bash
# Enable debug mode
export FLASK_DEBUG=1
python start.py

# Check logs
tail -f app.log
```

## 🔮 Future Enhancements

### Planned Features

- [ ] **Multi-language Support**: Internationalization for global users
- [ ] **Advanced AI Models**: Integration with multiple AI providers
- [ ] **Real-time Collaboration**: Multi-user attack simulations
- [ ] **Mobile App**: Native mobile application
- [ ] **Cloud Integration**: AWS, Azure, GCP deployment options
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Custom Wordlists**: User-defined password dictionaries
- [ ] **API Rate Limiting**: Advanced abuse prevention

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📚 Learning Resources

### Cybersecurity Concepts

- **Password Security**: Understanding weak vs. strong passwords
- **Hash Functions**: How password hashing works
- **Attack Vectors**: Different methods of password compromise
- **Defense Strategies**: Protecting against password attacks

### Technical Skills

- **Python Programming**: Core language concepts
- **Web Development**: Flask, HTML, CSS, JavaScript
- **API Design**: RESTful endpoint development
- **Security Testing**: Ethical penetration testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

- **Educational Use Only**: This tool is designed for educational purposes
- **No Real Attacks**: Never use against real systems or real passwords
- **Compliance**: Ensure compliance with local laws and regulations
- **Responsibility**: Users are responsible for their actions

## 🤝 Support

### Getting Help

- **Documentation**: This README and inline code comments
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join community discussions
- **Email**: Contact maintainers for direct support

### Community

- **GitHub**: [Repository](https://github.com/yourusername/ai-password-cracker-simulator)
- **Discord**: [Community Server](https://discord.gg/your-server)
- **Reddit**: [r/cybersecurity](https://reddit.com/r/cybersecurity)

## 🙏 Acknowledgments

- **Google Gemini**: AI capabilities and API access
- **Flask Community**: Web framework and ecosystem
- **Bootstrap**: UI components and responsive design
- **Font Awesome**: Icons and visual elements
- **Open Source Community**: All contributors and maintainers

---

**Remember: This tool is for EDUCATIONAL PURPOSES ONLY. Use responsibly and ethically.**

**Happy Learning! 🚀🔐**
