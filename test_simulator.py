#!/usr/bin/env python3
"""
Test script for AI-Powered Password Cracker Simulator

This script demonstrates the basic functionality without requiring
Google Gemini API access.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.hash_utils import hash_password, verify_hash
from core.dictionary_attack import DictionaryAttack
from core.rule_based import RuleBasedAttack


def test_basic_functionality():
    """Test basic hash functionality."""
    print("🧪 Testing Basic Functionality")
    print("=" * 40)
    
    # Test password hashing
    test_password = "test123"
    hash_value = hash_password(test_password)
    print(f"Password length: {len(test_password)}")
    print(f"Hash: {hash_value[:16]}...")
    
    # Test verification
    is_valid = verify_hash(test_password, hash_value)
    print(f"Verification: {'✅ PASS' if is_valid else '❌ FAIL'}")
    
    # Test wrong password
    is_valid = verify_hash("wrong", hash_value)
    print(f"Wrong password test: {'✅ PASS' if not is_valid else '❌ FAIL'}")
    
    print()


def test_dictionary_attack():
    """Test dictionary attack functionality."""
    print("📚 Testing Dictionary Attack")
    print("=" * 40)
    
    # Create a test hash
    target_password = "password"
    target_hash = hash_password(target_password)
    print(f"Target password length: {len(target_password)}")
    print(f"Target hash: {target_hash[:16]}...")
    
    # Run dictionary attack
    attacker = DictionaryAttack()
    try:
        password, attempts, time_taken = attacker.crack(target_hash)
        
        if password:
            print(f"✅ Password found (masked): {'*' * len(password)}")
        else:
            print("❌ Password not found")
        
        print(f"Attempts: {attempts}")
        print(f"Time: {time_taken:.2f} seconds")
        
        # Get stats
        stats = attacker.get_stats()
        print(f"Method: {stats.get('method', 'Unknown')}")
        print(f"Words loaded: {stats.get('words_loaded', 0)}")
        
    except Exception as e:
        print(f"❌ Dictionary attack failed: {e}")
    
    print()


def test_rule_based_attack():
    """Test rule-based attack functionality."""
    print("🎯 Testing Rule-Based Attack")
    print("=" * 40)
    
    # Create a test hash
    target_password = "qwerty"
    target_hash = hash_password(target_password)
    print(f"Target password length: {len(target_password)}")
    print(f"Target hash: {target_hash[:16]}...")
    
    # Run rule-based attack
    attacker = RuleBasedAttack()
    try:
        password, attempts, time_taken = attacker.crack(target_hash)
        
        if password:
            print(f"✅ Password found (masked): {'*' * len(password)}")
        else:
            print("❌ Password not found")
        
        print(f"Attempts: {attempts}")
        print(f"Time: {time_taken:.2f} seconds")
        
        # Get stats
        stats = attacker.get_stats()
        print(f"Method: {stats.get('method', 'Unknown')}")
        print(f"Rules used: {stats.get('rules_used', 0)}")
        
    except Exception as e:
        print(f"❌ Rule-based attack failed: {e}")
    
    print()


def test_synthetic_data():
    """Test synthetic data generation."""
    print("🎭 Testing Synthetic Data Generation")
    print("=" * 40)
    
    from utils.hash_utils import generate_fake_password_data
    
    # Generate fake data
    fake_data = generate_fake_password_data(5)
    
    print("Generated fake passwords (masked):")
    for i, item in enumerate(fake_data, 1):
        print(f"{i}. {'*' * len(item['password'])} -> {item['hash'][:16]}...")
        print(f"   Description: {item['description']}")
        print(f"   Difficulty: {item['difficulty']}")
    
    print()


def main():
    """Run all tests."""
    print("🔐 AI-Powered Password Cracker Simulator - Test Suite")
    print("=" * 60)
    print("This test suite demonstrates the basic functionality")
    print("without requiring external API access.")
    print("=" * 60)
    print()
    
    try:
        test_basic_functionality()
        test_dictionary_attack()
        test_rule_based_attack()
        test_synthetic_data()
        
        print("🎉 All tests completed!")
        print("\nTo run the full simulator:")
        print("  python main.py --interactive")
        print("\nTo test with a specific hash:")
        print("  python main.py --method dictionary --target <hash>")
        
    except Exception as e:
        print(f"💥 Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
