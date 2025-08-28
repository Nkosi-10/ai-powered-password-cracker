#!/usr/bin/env python3
"""
Demo script for AI-Powered Password Cracker Simulator

This script demonstrates the simulator with pre-defined examples
to showcase different attack methods.
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.hash_utils import hash_password
from core.dictionary_attack import DictionaryAttack
from core.rule_based import RuleBasedAttack
from core.brute_force import BruteForceAttack


def demo_dictionary_attack():
    """Demonstrate dictionary attack."""
    print("📚 Dictionary Attack Demo")
    print("=" * 40)
    
    # Target password that should be in our wordlist
    target_password = "admin"
    target_hash = hash_password(target_password)
    
    print(f"🎯 Target: {target_password}")
    print(f"🔐 Hash: {target_hash}")
    print()
    
    # Run attack
    attacker = DictionaryAttack()
    start_time = time.time()
    
    password, attempts, time_taken = attacker.crack(target_hash)
    
    print(f"\n📊 Results:")
    print(f"   Success: {'✅ Yes' if password else '❌ No'}")
    if password:
        print(f"   Password: {password}")
    print(f"   Attempts: {attempts}")
    print(f"   Time: {time_taken:.3f} seconds")
    
    if attempts > 0:
        rate = attempts / time_taken
        print(f"   Rate: {rate:.0f} attempts/second")
    
    print()


def demo_rule_based_attack():
    """Demonstrate rule-based attack."""
    print("🎯 Rule-Based Attack Demo")
    print("=" * 40)
    
    # Target password that follows common patterns
    target_password = "qwerty"
    target_hash = hash_password(target_password)
    
    print(f"🎯 Target: {target_password}")
    print(f"🔐 Hash: {target_hash}")
    print()
    
    # Run attack
    attacker = RuleBasedAttack()
    start_time = time.time()
    
    password, attempts, time_taken = attacker.crack(target_hash)
    
    print(f"\n📊 Results:")
    print(f"   Success: {'✅ Yes' if password else '❌ No'}")
    if password:
        print(f"   Password: {password}")
    print(f"   Attempts: {attempts}")
    print(f"   Time: {time_taken:.3f} seconds")
    
    if attempts > 0:
        rate = attempts / time_taken
        print(f"   Rate: {rate:.0f} attempts/second")
    
    print()


def demo_brute_force_attack():
    """Demonstrate brute force attack (limited)."""
    print("🔨 Brute Force Attack Demo")
    print("=" * 40)
    
    # Target password that's short enough for brute force
    target_password = "abc"
    target_hash = hash_password(target_password)
    
    print(f"🎯 Target: {target_password}")
    print(f"🔐 Hash: {target_hash}")
    print(f"📏 Length: {len(target_password)}")
    print()
    
    # Run attack
    attacker = BruteForceAttack()
    start_time = time.time()
    
    password, attempts, time_taken = attacker.crack(target_hash, max_length=3)
    
    print(f"\n📊 Results:")
    print(f"   Success: {'✅ Yes' if password else '❌ No'}")
    if password:
        print(f"   Password: {password}")
    print(f"   Attempts: {attempts}")
    print(f"   Time: {time_taken:.3f} seconds")
    
    if attempts > 0:
        rate = attempts / time_taken
        print(f"   Rate: {rate:.0f} attempts/second")
    
    print()


def demo_performance_comparison():
    """Compare performance of different attack methods."""
    print("⚡ Performance Comparison Demo")
    print("=" * 40)
    
    # Use a password that all methods can find
    target_password = "password"
    target_hash = hash_password(target_password)
    
    print(f"🎯 Target: {target_password}")
    print(f"🔐 Hash: {target_hash}")
    print()
    
    methods = [
        ("Dictionary", DictionaryAttack()),
        ("Rule-Based", RuleBasedAttack()),
    ]
    
    results = []
    
    for method_name, attacker in methods:
        print(f"🔍 Testing {method_name} Attack...")
        
        start_time = time.time()
        password, attempts, time_taken = attacker.crack(target_hash)
        end_time = time.time()
        
        results.append({
            'method': method_name,
            'success': password is not None,
            'attempts': attempts,
            'time': time_taken,
            'rate': attempts / time_taken if time_taken > 0 else 0
        })
        
        print(f"   ✅ Completed in {time_taken:.3f}s")
    
    # Display comparison
    print(f"\n📊 Performance Comparison:")
    print("-" * 50)
    print(f"{'Method':<15} {'Success':<8} {'Attempts':<10} {'Time (s)':<10} {'Rate (att/s)':<12}")
    print("-" * 50)
    
    for result in results:
        success_str = "✅ Yes" if result['success'] else "❌ No"
        print(f"{result['method']:<15} {success_str:<8} {result['attempts']:<10} {result['time']:<10.3f} {result['rate']:<12.0f}")
    
    print()


def main():
    """Run all demos."""
    print("🔐 AI-Powered Password Cracker Simulator - Demo Suite")
    print("=" * 60)
    print("This demo showcases different attack methods with synthetic data.")
    print("All passwords and hashes are generated for demonstration purposes.")
    print("=" * 60)
    print()
    
    try:
        # Run demos
        demo_dictionary_attack()
        demo_rule_based_attack()
        demo_brute_force_attack()
        demo_performance_comparison()
        
        print("🎉 Demo completed successfully!")
        print("\nTo run the full interactive simulator:")
        print("  python main.py --interactive")
        print("\nTo run tests:")
        print("  python test_simulator.py")
        
    except Exception as e:
        print(f"💥 Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
