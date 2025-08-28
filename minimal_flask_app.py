#!/usr/bin/env python3
"""
Minimal Flask App with Google Generative AI
Works seamlessly locally (.env) and on Render (environment variables)
"""

import os
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load .env file only if it exists (local development)
if os.path.exists('.env'):
    load_dotenv()
    print("🔧 Local development mode: loaded .env file")
else:
    print("🚀 Production mode: using environment variables")

app = Flask(__name__)

def get_api_key():
    """
    Get Google Generative AI API key from environment.
    
    Tries multiple common variable names:
    - GOOGLE_API_KEY (recommended)
    - MY_API_KEY (legacy)
    - GEMINI_API_KEY (alternative)
    
    Returns:
        str or None: API key if found, None otherwise
    """
    api_key_names = ['GOOGLE_API_KEY', 'MY_API_KEY', 'GEMINI_API_KEY']
    
    for key_name in api_key_names:
        api_key = os.environ.get(key_name)
        if api_key:
            print(f"✅ Found API key in {key_name}")
            return api_key
    
    print("❌ No API key found. Checked: " + ", ".join(api_key_names))
    return None

def initialize_genai():
    """
    Initialize Google Generative AI with API key.
    
    Returns:
        tuple: (success: bool, model_or_error: GenerativeModel or str)
    """
    try:
        import google.generativeai as genai
        
        api_key = get_api_key()
        if not api_key:
            return False, "No API key found"
        
        # Configure and create model
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        print("✅ Google Generative AI initialized successfully")
        return True, model
        
    except ImportError:
        return False, "google-generativeai module not installed"
    except Exception as e:
        return False, f"Failed to initialize: {str(e)}"

# Initialize AI on startup
AI_INITIALIZED, AI_MODEL_OR_ERROR = initialize_genai()

@app.route('/')
def home():
    """Home route with basic info."""
    return jsonify({
        'message': 'Flask app with Google Generative AI',
        'ai_status': 'initialized' if AI_INITIALIZED else 'failed',
        'environment': 'local' if os.path.exists('.env') else 'production'
    })

@app.route('/test')
def test_api_key():
    """Test route to verify API key is loaded and working."""
    try:
        api_key = get_api_key()
        
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'No API key found',
                'environment': 'local' if os.path.exists('.env') else 'production',
                'checked_variables': ['GOOGLE_API_KEY', 'MY_API_KEY', 'GEMINI_API_KEY']
            }), 400
        
        if not AI_INITIALIZED:
            return jsonify({
                'success': False,
                'message': f'AI initialization failed: {AI_MODEL_OR_ERROR}',
                'api_key_found': True,
                'api_key_masked': f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***masked***",
                'environment': 'local' if os.path.exists('.env') else 'production'
            }), 500
        
        # Test actual API call
        try:
            response = AI_MODEL_OR_ERROR.generate_content("Say 'Hello from Gemini!' in exactly those words.")
            api_working = 'Hello from Gemini!' in response.text
            
            return jsonify({
                'success': True,
                'message': 'API key loaded and verified',
                'api_key_found': True,
                'api_key_masked': f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***masked***",
                'environment': 'local' if os.path.exists('.env') else 'production',
                'api_test_passed': api_working,
                'ai_response': response.text if api_working else 'Test failed'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'API key found but API call failed: {str(e)}',
                'api_key_found': True,
                'api_key_masked': f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***masked***",
                'environment': 'local' if os.path.exists('.env') else 'production'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Test failed: {str(e)}',
            'environment': 'local' if os.path.exists('.env') else 'production'
        }), 500

@app.route('/generate')
def generate_text():
    """Example route that uses the AI model."""
    if not AI_INITIALIZED:
        return jsonify({
            'error': f'AI not available: {AI_MODEL_OR_ERROR}'
        }), 500
    
    try:
        prompt = "Write a short poem about coding"
        response = AI_MODEL_OR_ERROR.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'response': response.text,
            'environment': 'local' if os.path.exists('.env') else 'production'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Generation failed: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'available_routes': ['/', '/test', '/generate']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Flask app with Google Generative AI...")
    print(f"🔧 Environment: {'Local' if os.path.exists('.env') else 'Production'}")
    print(f"🤖 AI Status: {'Ready' if AI_INITIALIZED else 'Failed'}")
    
    if not AI_INITIALIZED:
        print(f"❌ AI Error: {AI_MODEL_OR_ERROR}")
        print("💡 Make sure to set GOOGLE_API_KEY environment variable")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
