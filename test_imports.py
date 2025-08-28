#!/usr/bin/env python3
"""
Test script to check if all modules can be imported without errors.
"""

import sys
import os

def test_imports():
    """Test importing all required modules."""
    print("🧪 Testing module imports...")
    print("=" * 40)
    
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        print("Testing core modules...")
        from core import (
            BruteForceAttack, DictionaryAttack, RuleBasedAttack,
            USBDeviceSimulator, DeviceType, SecurityLevel
        )
        print("✅ Core modules imported successfully")
        
        print("\nTesting AI module...")
        from ai import AIGuesser
        print("✅ AI module imported successfully")
        
        print("\nTesting utility modules...")
        from utils.config import Config
        from utils.hash_utils import hash_password, verify_hash, generate_synthetic_hash
        print("✅ Utility modules imported successfully")
        
        print("\nTesting Flask...")
        import flask
        import flask_cors
        print("✅ Flask modules imported successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of imported modules."""
    print("\n🔧 Testing basic functionality...")
    print("=" * 40)
    
    try:
        # Test hash utilities
        test_password = "test123"
        hash_value = hash_password(test_password)
        print(f"✅ Hash generation: {hash_value[:16]}...")
        
        # Test hash verification
        is_valid = verify_hash(test_password, hash_value)
        print(f"✅ Hash verification: {is_valid}")
        
        # Test USB simulator
        from core import USBDeviceSimulator, DeviceType, SecurityLevel
        simulator = USBDeviceSimulator()
        device = simulator.create_simulated_device(
            DeviceType.FLASH_DRIVE,
            SecurityLevel.BASIC,
            "test123"
        )
        print(f"✅ USB device creation: {device.device_id}")
        
        # Test attack classes
        from core import BruteForceAttack
        attacker = BruteForceAttack()
        print(f"✅ Attack class initialization: {type(attacker).__name__}")
        
        print("\n✅ All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Module Import Test Suite")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test functionality
    if not test_basic_functionality():
        print("\n❌ Functionality tests failed!")
        return False
    
    print("\n🎉 All tests passed! The application should work correctly.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
