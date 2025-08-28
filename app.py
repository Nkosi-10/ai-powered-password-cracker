#!/usr/bin/env python3
"""
AI-Powered Password Cracker Simulator - Web Application

Flask-based web backend for the password cracking simulator.
This provides a robust web interface that can run in any browser.

🔑 IMPORTANT: Google Gemini API key is directly set in initialize_ai()
"""

import os
import sys
import json
import time
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Import our simulator modules
from core import (
    BruteForceAttack, DictionaryAttack, RuleBasedAttack
)
from ai import AIGuesser
from utils.config import Config
from utils.hash_utils import hash_password, generate_synthetic_hash, generate_fake_password_data

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate random secret key
CORS(app)  # Enable CORS for cross-origin requests

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['JSON_SORT_KEYS'] = False

# Global variables
simulator = None
fake_passwords = []

def initialize_simulator():
    """Initialize the simulator and load fake data."""
    global simulator, fake_passwords
    
    try:
        # Load fake password data
        fake_passwords = load_fake_passwords()
        
        # Initialize attack methods
        simulator = {
            'brute_force': BruteForceAttack(),
            'dictionary': DictionaryAttack(),
            'rule_based': RuleBasedAttack(),
            'ai': None  # Will be initialized when needed
        }
        
        print("Simulator initialized successfully")
        return True
        
    except Exception as e:
        print(f"Failed to initialize simulator: {e}")
        traceback.print_exc()
        return False

def load_fake_passwords():
    """Load fake password data from file."""
    try:
        with open('data/fake_passwords.json', 'r') as f:
            data = json.load(f)
            # Do not expose plaintext passwords to the UI
            sanitized = []
            for item in data:
                sanitized.append({
                    'hash': item.get('hash'),
                    'description': item.get('description', ''),
                    'length': len(item.get('password', '')) if item.get('password') else None
                })
            return sanitized
    except FileNotFoundError:
        # Generate fake data if file doesn't exist
        fake_data = generate_fake_password_data(20)
        os.makedirs('data', exist_ok=True)
        with open('data/fake_passwords.json', 'w') as f:
            json.dump(fake_data, f, indent=2)
        # Return sanitized version
        sanitized = []
        for item in fake_data:
            sanitized.append({
                'hash': item.get('hash'),
                'description': item.get('description', ''),
                'length': len(item.get('password', '')) if item.get('password') else None
            })
        return sanitized

def initialize_ai():
    """Initialize AI guesser using API key from environment variable."""
    try:
        # 🔑 Read API key from environment variable for security
        api_key = os.environ.get('MY_API_KEY')
        if not api_key:
            print("❌ MY_API_KEY environment variable not set")
            return False
            
        simulator['ai'] = AIGuesser(api_key)
        print("✅ AI module initialized successfully")
        return True
            
    except Exception as e:
        print(f"AI initialization failed: {e}")
        return False

def run_attack(target_hash: str, method: str, **kwargs) -> Dict[str, Any]:
    """Run the selected attack method."""
    try:
        if method == 'ai':
            # Initialize AI if not already done
            if simulator['ai'] is None:
                if not initialize_ai():
                    return {
                        'success': False,
                        'error': 'AI module not available. Please configure your API key.',
                        'method': method,
                        'attempts': 0,
                        'time_taken': 0
                    }
            
            attacker = simulator['ai']
            password, attempts, time_taken = attacker.crack(target_hash, **kwargs)
            
        else:
            attacker = simulator[method]
            if method == 'brute_force':
                max_length = kwargs.get('max_length', 6)  # Reduced for web safety
                password, attempts, time_taken = attacker.crack(target_hash, max_length)
            else:
                password, attempts, time_taken = attacker.crack(target_hash)
        
        # Get attack statistics
        stats = attacker.get_stats()
        
        return {
            'success': password is not None,
            # Do not expose plaintext password
            'password_masked': ('*' * len(password)) if password else None,
            'method': method,
            'attempts': attempts,
            'time_taken': time_taken,
            'stats': stats
        }
        
    except Exception as e:
        print(f"Attack failed: {e}")
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'method': method,
            'attempts': 0,
            'time_taken': 0
        }

# Error handlers
@app.errorhandler(HTTPException)
def handle_http_error(error):
    """Handle HTTP errors."""
    return jsonify({
        'error': True,
        'message': error.description,
        'code': error.code
    }), error.code

@app.errorhandler(Exception)
def handle_generic_error(error):
    """Handle generic errors."""
    print(f"Unhandled error: {error}")
    traceback.print_exc()
    return jsonify({
        'error': True,
        'message': 'Internal server error',
        'code': 500
    }), 500

# Routes
@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Get application status."""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'ai_available': simulator['ai'] is not None if simulator else False,
        'fake_passwords_count': len(fake_passwords)
    })

@app.route('/api/fake-passwords')
def api_fake_passwords():
    """Get list of fake passwords."""
    return jsonify({'passwords': fake_passwords})

@app.route('/api/attack', methods=['POST'])
def api_attack():
    """Run a password attack."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': True, 'message': 'No data provided'}), 400
        
        target_hash = data.get('target_hash', '').strip()
        method = data.get('method', 'dictionary').strip()
        context = data.get('context', '').strip()
        max_length = data.get('max_length', 6)
        
        # Validation
        if not target_hash:
            return jsonify({'error': True, 'message': 'Target hash is required'}), 400
        
        if method not in ['brute_force', 'dictionary', 'rule_based', 'ai']:
            return jsonify({'error': True, 'message': 'Invalid attack method'}), 400
        
        if method == 'brute_force' and (max_length < 1 or max_length > 6):
            return jsonify({'error': True, 'message': 'Max length must be between 1 and 6'}), 400
        
        # Run attack
        kwargs = {}
        if method == 'brute_force':
            kwargs['max_length'] = max_length
        if method == 'ai' and context:
            kwargs['context'] = context
        
        result = run_attack(target_hash, method, **kwargs)
        result['timestamp'] = datetime.now().isoformat()
        result['target_hash'] = target_hash
        
        return jsonify(result)
        
    except Exception as e:
        print(f" API attack error: {e}")
        traceback.print_exc()
        return jsonify({'error': True, 'message': f'Attack failed: {str(e)}'}), 500

@app.route('/api/generate-hash', methods=['POST'])
def api_generate_hash():
    """Generate a hash from a password."""
    try:
        data = request.get_json()
        password = data.get('password', '').strip()
        
        if not password:
            return jsonify({'error': True, 'message': 'Password is required'}), 400
        
        hash_value = hash_password(password)
        
        return jsonify({
            'hash': hash_value,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f" Hash generation error: {e}")
        return jsonify({'error': True, 'message': f'Hash generation failed: {str(e)}'}), 500

@app.route('/data')
def get_data():
    """Secure endpoint that fetches data from third-party API using hidden API key."""
    try:
        # Get API key from environment variable (never exposed to frontend)
        api_key = os.environ.get('MY_API_KEY')
        if not api_key:
            return jsonify({
                'error': True, 
                'message': 'API key not configured'
            }), 500
        
        # Example: Make request to third-party API
        # Replace this with your actual API endpoint and logic
        import requests
        
        # Simulated API call (replace with your actual API endpoint)
        # headers = {'Authorization': f'Bearer {api_key}'}
        # response = requests.get('https://api.example.com/data', headers=headers)
        
        # For demonstration, returning mock data that would come from your API
        mock_data = {
            'success': True,
            'data': {
                'ai_status': 'operational',
                'api_version': '2.0',
                'features': ['password_analysis', 'security_assessment', 'threat_detection'],
                'last_updated': datetime.now().isoformat(),
                'usage_stats': {
                    'requests_today': 42,
                    'success_rate': 98.5
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(mock_data)
        
    except Exception as e:
        print(f"Data fetch error: {e}")
        return jsonify({
            'error': True, 
            'message': 'Failed to fetch data from API'
        }), 500

# USB functionality removed for simplicity

# Initialize on startup
if __name__ == '__main__':
    print("🚀 Starting AI-Powered Password Cracker Simulator...")
    
    if initialize_simulator():
        print("Simulator ready")
        initialize_ai()
        
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=False,
            threaded=True
        )
    else:
        print(" Failed to initialize simulator")
        sys.exit(1)
