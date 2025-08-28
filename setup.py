#!/usr/bin/env python3
"""
Setup script for AI-Powered Password Cracker Simulator

This script helps set up the environment and dependencies.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python version: {sys.version}")
    return True


def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = ["data", "results", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True


def check_api_key():
    """Check if Google Gemini API key is configured."""
    print("\n🔑 Checking API configuration...")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if api_key and api_key != 'your_gemini_api_key_here':
        print("✅ Google Gemini API key is configured")
        return True
    else:
        print("⚠️ Google Gemini API key not configured")
        print("   To use AI-powered attacks, set the GOOGLE_API_KEY environment variable")
        print("   Get your free API key from: https://makersuite.google.com/app/apikey")
        return False


def run_tests():
    """Run basic tests to verify installation."""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test basic imports
        from utils.hash_utils import hash_password, verify_hash
        from core.dictionary_attack import DictionaryAttack
        
        # Test basic functionality
        test_password = "test123"
        hash_value = hash_password(test_password)
        is_valid = verify_hash(test_password, hash_value)
        
        if is_valid:
            print("✅ Basic functionality test passed")
        else:
            print("❌ Basic functionality test failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def display_next_steps():
    """Display next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. To run the demo:")
    print("   python demo.py")
    print("\n2. To run tests:")
    print("   python test_simulator.py")
    print("\n3. To run the interactive simulator:")
    print("   python main.py --interactive")
    print("\n4. For command-line usage:")
    print("   python main.py --help")
    print("\n5. To configure AI features:")
    print("   - Get API key from: https://makersuite.google.com/app/apikey")
    print("   - Set environment variable: export GOOGLE_API_KEY='your_key'")
    print("\n📚 For more information, see README.md")


def main():
    """Main setup function."""
    print("🔐 AI-Powered Password Cracker Simulator - Setup")
    print("=" * 50)
    print("This script will set up your environment for the simulator.")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Failed to create directories.")
        sys.exit(1)
    
    # Check API configuration
    check_api_key()
    
    # Run tests
    if not run_tests():
        print("\n❌ Tests failed. Please check the installation.")
        sys.exit(1)
    
    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    main()
