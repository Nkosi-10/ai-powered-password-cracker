#!/usr/bin/env python3
"""
Debug script for AI-Powered Password Cracker Simulator.
Tests the application step by step to identify issues.
"""

import sys
import os
import json
import traceback

def debug_step(step_name, func, *args, **kwargs):
    """Execute a debug step and report results."""
    print(f"\n🔍 Step: {step_name}")
    print("-" * 50)
    
    try:
        result = func(*args, **kwargs)
        print(f"✅ {step_name} completed successfully")
        if result is not None:
            print(f"   Result: {result}")
        return True
    except Exception as e:
        print(f"❌ {step_name} failed: {e}")
        traceback.print_exc()
        return False

def test_imports():
    """Test importing all modules."""
    print("🧪 Testing module imports...")
    
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Test core modules
        from core import (
            BruteForceAttack, DictionaryAttack, RuleBasedAttack,
            USBDeviceSimulator, DeviceType, SecurityLevel
        )
        print("✅ Core modules imported")
        
        # Test AI module
        from ai import AIGuesser
        print("✅ AI module imported")
        
        # Test utility modules
        from utils.config import Config
        from utils.hash_utils import hash_password, verify_hash, generate_synthetic_hash
        print("✅ Utility modules imported")
        
        # Test Flask
        import flask
        import flask_cors
        print("✅ Flask modules imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_hash_utilities():
    """Test hash utility functions."""
    from utils.hash_utils import hash_password, verify_hash
    
    # Test basic hashing
    password = "test123"
    hash_value = hash_password(password)
    print(f"   Hash generated: {hash_value[:16]}...")
    
    # Test verification
    is_valid = verify_hash(password, hash_value)
    print(f"   Verification: {is_valid}")
    
    return True

def test_usb_simulator():
    """Test USB simulator functionality."""
    from core import USBDeviceSimulator, DeviceType, SecurityLevel
    
    simulator = USBDeviceSimulator()
    
    # Create a device
    device = simulator.create_simulated_device(
        DeviceType.FLASH_DRIVE,
        SecurityLevel.BASIC,
        "password123"
    )
    print(f"   Device created: {device.device_id}")
    
    # Get device info
    info = simulator.get_device_info(device.device_id)
    print(f"   Device info: {info['device_type']} - {info['security_level']}")
    
    # Test unlock with wrong password
    result = simulator.attempt_unlock(device.device_id, "wrong", "test")
    print(f"   Wrong password result: {result['success']}")
    
    # Test unlock with correct password
    result = simulator.attempt_unlock(device.device_id, "password123", "test")
    print(f"   Correct password result: {result['success']}")
    
    return True

def test_attack_classes():
    """Test attack class initialization."""
    from core import BruteForceAttack, DictionaryAttack, RuleBasedAttack
    
    # Test brute force
    brute_force = BruteForceAttack()
    print(f"   BruteForceAttack: {type(brute_force).__name__}")
    
    # Test dictionary attack
    dictionary = DictionaryAttack()
    print(f"   DictionaryAttack: {type(dictionary).__name__}")
    
    # Test rule based attack
    rule_based = RuleBasedAttack()
    print(f"   RuleBasedAttack: {type(rule_based).__name__}")
    
    return True

def test_flask_app():
    """Test Flask app creation."""
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    """Run all debug steps."""
    print("🚀 AI-Powered Password Cracker Simulator - Debug Mode")
    print("=" * 60)
    
    steps = [
        ("Module Imports", test_imports),
        ("Hash Utilities", test_hash_utilities),
        ("USB Simulator", test_usb_simulator),
        ("Attack Classes", test_attack_classes),
        ("Flask App", test_flask_app),
    ]
    
    results = []
    for step_name, step_func in steps:
        success = debug_step(step_name, step_func)
        results.append((step_name, success))
    
    # Summary
    print("\n📊 Debug Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for step_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {step_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} steps passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application should work correctly.")
        print("\nTo start the application:")
        print("   Windows: start.bat or start.ps1")
        print("   Linux/Mac: python start.py")
        print("   Or: python app.py")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
