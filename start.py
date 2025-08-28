#!/usr/bin/env python3
"""
AI-Powered Password Cracker Simulator - Startup Script

This script provides easy startup and configuration options for the web application.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies found")
        return True
    except ImportError:
        print("❌ Flask dependencies not found")
        print("   Run: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if Google Gemini API key is configured."""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("⚠️  Google Gemini API key not configured")
        print("   To enable AI features:")
        print("   1. Visit: https://makersuite.google.com/app/apikey")
        print("   2. Create a free API key")
        print("   3. Set environment variable: export GOOGLE_API_KEY='your_key'")
        print("   Note: AI features will be disabled without the key")
        return False
    else:
        print("✅ Google Gemini API key configured")
        return True

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("# AI-Powered Password Cracker Simulator Environment\n")
            f.write("# Copy this file to .env and fill in your actual values\n\n")
            f.write("# Google Gemini API Key (required for AI-powered attacks)\n")
            f.write("# Get your free API key from: https://makersuite.google.com/app/apikey\n")
            f.write("GOOGLE_API_KEY=your_gemini_api_key_here\n\n")
            f.write("# Optional: Custom configuration\n")
            f.write("# MAX_PASSWORD_LENGTH=12\n")
            f.write("# MAX_BRUTE_FORCE_LENGTH=6\n")
            f.write("# AI_TIMEOUT=30\n")
            f.write("# LOG_LEVEL=INFO\n")
        print("✅ .env file created")
        print("   Edit .env file and add your actual API key")
    else:
        print("✅ .env file already exists")

def start_development():
    """Start the application in development mode."""
    print("🚀 Starting in development mode...")
    
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    os.environ['DEBUG'] = 'True'
    
    # Import and run app
    try:
        from app import app
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=True,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

def start_production():
    """Start the application in production mode."""
    print("🚀 Starting in production mode...")
    
    # Check if gunicorn is available
    try:
        import gunicorn
        print("✅ Gunicorn found, starting production server...")
        
        # Start with gunicorn
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            'app:app',
            '--bind', '0.0.0.0:5000',
            '--workers', '4',
            '--timeout', '120',
            '--max-requests', '1000',
            '--max-requests-jitter', '100'
        ])
        
    except ImportError:
        print("⚠️  Gunicorn not found, falling back to Flask development server")
        print("   Install with: pip install gunicorn")
        start_development()

def run_tests():
    """Run the test suite."""
    print("🧪 Running test suite...")
    
    try:
        # Try pytest first
        subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'])
    except FileNotFoundError:
        print("⚠️  Pytest not found, running basic tests...")
        
        # Run basic tests
        try:
            print("Testing core modules...")
            import core.brute_force
            import core.dictionary_attack
            import core.rule_based
            import core.usb_simulator
            print("✅ Core modules imported successfully")
            
            # Test AI module
            print("Testing AI module...")
            import ai.ai_guesser
            print("✅ AI module imported successfully")
            
            # Test utilities
            print("Testing utilities...")
            import utils.hash_utils
            import utils.config
            print("✅ Utility modules imported successfully")
            
            # Test USB simulator specifically
            print("Testing USB simulator...")
            from core.usb_simulator import USBDeviceSimulator, DeviceType, SecurityLevel
            
            # Create a test device
            simulator = USBDeviceSimulator()
            device = simulator.create_simulated_device(
                DeviceType.FLASH_DRIVE, 
                SecurityLevel.BASIC, 
                "test123"
            )
            
            # Test device info
            info = simulator.get_device_info(device.device_id)
            if info:
                print(f"✅ USB simulator working - Created device: {info['device_type']}")
            else:
                print("❌ USB simulator device info failed")
                return False
                
            print("✅ All basic tests passed!")
            return True
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False

def main():
    """Main startup function."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Password Cracker Simulator - Startup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start.py                    # Start in development mode
  python start.py --production      # Start in production mode
  python start.py --test            # Run tests
  python start.py --setup           # Setup environment
        """
    )
    
    parser.add_argument(
        '--production',
        action='store_true',
        help='Start in production mode with Gunicorn'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run the test suite'
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Setup environment and dependencies'
    )
    
    args = parser.parse_args()
    
    print("🔐 AI-Powered Password Cracker Simulator - Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check API key
    api_configured = check_api_key()
    
    # Setup mode
    if args.setup:
        print("\n🔧 Setting up environment...")
        create_env_file()
        print("\n✅ Setup complete!")
        print("   Next steps:")
        print("   1. Edit .env file with your API key")
        print("   2. Run: python start.py")
        return
    
    # Test mode
    if args.test:
        print("\n🧪 Running tests...")
        run_tests()
        return
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    print(f"\n🌐 Application will be available at: http://localhost:5000")
    print(f"📱 AI Features: {'✅ Enabled' if api_configured else '❌ Disabled (API key required)'}")
    
    # Start application
    if args.production:
        start_production()
    else:
        start_development()

if __name__ == "__main__":
    main()
