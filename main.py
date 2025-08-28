#!/usr/bin/env python3
"""
AI-Powered Password Cracker Simulator

Main application entry point for the educational password cracking simulator.
This tool is for educational purposes only and only works with synthetic data.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Optional, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import BruteForceAttack, DictionaryAttack, RuleBasedAttack
from ai import AIGuesser
from utils import Config, hash_password, generate_synthetic_hash
from utils.hash_utils import generate_fake_password_data


class PasswordCrackerSimulator:
    """
    Main simulator class that orchestrates password cracking attempts.
    
    This class manages different attack methods, tracks performance,
    and provides a user-friendly interface for the simulation.
    """
    
    def __init__(self):
        """Initialize the password cracker simulator."""
        self.config = Config()
        self.results = []
        self.current_session = None
        
        # Initialize attack methods
        self.attack_methods = {
            'brute_force': BruteForceAttack(),
            'dictionary': DictionaryAttack(),
            'rule_based': RuleBasedAttack(),
            'ai': None  # Will be initialized when needed
        }
        
        # Create necessary directories
        self._ensure_directories()
        
        # Load fake password data
        self.fake_passwords = self._load_fake_passwords()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        os.makedirs(self.config.RESULTS_DIR, exist_ok=True)
    
    def _load_fake_passwords(self) -> list:
        """Load fake password data from file."""
        try:
            with open(self.config.FAKE_PASSWORDS_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Generate fake data if file doesn't exist
            fake_data = generate_fake_password_data(20)
            with open(self.config.FAKE_PASSWORDS_PATH, 'w') as f:
                json.dump(fake_data, f, indent=2)
            return fake_data
    
    def display_banner(self):
        """Display the application banner."""
        print("🔐 AI-Powered Password Cracker Simulator")
        print("=" * 50)
        print(f"📋 Version: {self.config.VERSION}")
        print(f"👨‍💻 Author: {self.config.AUTHOR}")
        print("🎓 Educational Purpose Only - Synthetic Data Only")
        print("=" * 50)
        print()
    
    def display_ethical_warning(self):
        """Display ethical warning and disclaimer."""
        print("🚨 ETHICAL DISCLAIMER")
        print("-" * 30)
        print("This tool is for EDUCATIONAL PURPOSES ONLY.")
        print("It ONLY works with synthetic/fake password hashes.")
        print("It CANNOT crack real passwords or real systems.")
        print("Use only in controlled, educational environments.")
        print("-" * 30)
        print()
    
    def select_target_hash(self) -> str:
        """Let user select a target hash from fake data or enter custom."""
        print("🎯 Select Target Hash:")
        print("1. Use pre-generated fake hash")
        print("2. Enter custom hash (synthetic only)")
        print("3. Generate new fake hash")
        
        while True:
            choice = input("Enter choice (1-3): ").strip()
            
            if choice == '1':
                return self._select_from_fake_data()
            elif choice == '2':
                return self._enter_custom_hash()
            elif choice == '3':
                return self._generate_new_hash()
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    def _select_from_fake_data(self) -> str:
        """Select hash from pre-generated fake data."""
        print("\n📚 Available fake passwords:")
        for i, item in enumerate(self.fake_passwords, 1):
            print(f"{i:2d}. {item['password']} - {item['description']}")
        
        while True:
            try:
                choice = int(input(f"\nSelect password (1-{len(self.fake_passwords)}): "))
                if 1 <= choice <= len(self.fake_passwords):
                    selected = self.fake_passwords[choice - 1]
                    print(f"✅ Selected: {selected['password']}")
                    return selected['hash']
                else:
                    print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def _enter_custom_hash(self) -> str:
        """Let user enter a custom hash (with validation)."""
        while True:
            hash_input = input("Enter hash (64 characters for SHA-256): ").strip()
            
            if len(hash_input) == 64 and all(c in '0123456789abcdef' for c in hash_input.lower()):
                # Check for suspicious patterns
                if not self._is_suspicious_hash(hash_input):
                    return hash_input
                else:
                    print("⚠️ Warning: This hash pattern may be suspicious.")
                    confirm = input("Continue anyway? (y/N): ").strip().lower()
                    if confirm == 'y':
                        return hash_input
            else:
                print("❌ Invalid hash format. Expected 64 hex characters.")
    
    def _generate_new_hash(self) -> str:
        """Generate a new fake hash."""
        password = input("Enter password to hash (or press Enter for random): ").strip()
        if not password:
            password = None
        
        hash_value = generate_synthetic_hash(password)
        print(f"✅ Generated hash: {hash_value}")
        return hash_value
    
    def _is_suspicious_hash(self, hash_string: str) -> bool:
        """Check if hash has suspicious patterns."""
        suspicious_patterns = self.config.get_suspicious_patterns()
        return any(hash_string.startswith(pattern) for pattern in suspicious_patterns)
    
    def select_attack_method(self) -> str:
        """Let user select an attack method."""
        print("\n⚔️ Select Attack Method:")
        for key, info in self.config.ATTACK_METHODS.items():
            print(f"• {key}: {info['description']}")
        
        while True:
            method = input("\nEnter method name: ").strip().lower()
            if method in self.config.ATTACK_METHODS:
                return method
            else:
                print("❌ Invalid method. Please choose from the list above.")
    
    def run_attack(self, target_hash: str, method: str, **kwargs) -> Dict[str, Any]:
        """Run the selected attack method."""
        print(f"\n🚀 Starting {method.upper()} attack...")
        print(f"🎯 Target hash: {target_hash}")
        
        start_time = time.time()
        
        try:
            if method == 'ai':
                # Initialize AI guesser if not already done
                if self.attack_methods['ai'] is None:
                    try:
                        self.attack_methods['ai'] = AIGuesser()
                    except ValueError as e:
                        print(f"❌ AI initialization failed: {e}")
                        print("🔄 Falling back to dictionary attack...")
                        method = 'dictionary'
                        return self.run_attack(target_hash, method, **kwargs)
                
                attacker = self.attack_methods['ai']
                password, attempts, time_taken = attacker.crack(target_hash, **kwargs)
            else:
                attacker = self.attack_methods[method]
                if method == 'brute_force':
                    max_length = kwargs.get('max_length', 8)
                    password, attempts, time_taken = attacker.crack(target_hash, max_length)
                else:
                    password, attempts, time_taken = attacker.crack(target_hash)
            
            # Get attack statistics
            stats = attacker.get_stats()
            
            # Record results
            result = {
                'timestamp': datetime.now().isoformat(),
                'method': method,
                'target_hash': target_hash,
                'success': password is not None,
                'cracked_password': password,
                'attempts': attempts,
                'time_taken': time_taken,
                'stats': stats
            }
            
            self.results.append(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Attack failed: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'method': method,
                'target_hash': target_hash,
                'success': False,
                'error': str(e),
                'attempts': 0,
                'time_taken': time.time() - start_time
            }
    
    def display_results(self, result: Dict[str, Any]):
        """Display attack results."""
        print("\n📊 Attack Results:")
        print("-" * 30)
        print(f"🎯 Method: {result['method'].upper()}")
        print(f"⏱️ Time: {result.get('time_taken', 0):.2f} seconds")
        print(f"📊 Attempts: {result.get('attempts', 0):,}")
        
        if result.get('success'):
            print(f"✅ Password: {result['cracked_password']}")
        else:
            print("❌ Password not found")
            if 'error' in result:
                print(f"💥 Error: {result['error']}")
        
        # Display AI insights if available
        if result['method'] == 'ai' and 'stats' in result:
            ai_stats = result['stats']
            if 'ai_analysis' in ai_stats and ai_stats['ai_analysis']:
                analysis = ai_stats['ai_analysis']
                print(f"\n🤖 AI Insights:")
                print(f"   Recommendation: {analysis.get('recommendation', 'N/A')}")
                print(f"   Reasoning: {analysis.get('reasoning', 'N/A')}")
                print(f"   Probability: {analysis.get('probability', 'N/A')}")
    
    def save_results(self):
        """Save results to log file."""
        if not self.results:
            return
        
        log_file = self.config.LOG_PATH
        
        # Load existing logs
        existing_logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_logs = []
        
        # Add new results
        existing_logs.extend(self.results)
        
        # Save updated logs
        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)
        
        print(f"\n💾 Results saved to: {log_file}")
    
    def display_summary(self):
        """Display session summary."""
        if not self.results:
            print("\n📋 No attacks performed in this session.")
            return
        
        print("\n📈 Session Summary:")
        print("-" * 30)
        
        total_attempts = sum(r.get('attempts', 0) for r in self.results)
        total_time = sum(r.get('time_taken', 0) for r in self.results)
        successful_attacks = sum(1 for r in self.results if r.get('success'))
        
        print(f"🎯 Total attacks: {len(self.results)}")
        print(f"✅ Successful: {successful_attacks}")
        print(f"❌ Failed: {len(self.results) - successful_attacks}")
        print(f"📊 Total attempts: {total_attempts:,}")
        print(f"⏱️ Total time: {total_time:.2f} seconds")
        
        if total_attempts > 0:
            attempts_per_second = total_attempts / total_time
            print(f"🚀 Rate: {attempts_per_second:,.0f} attempts/second")
    
    def interactive_mode(self):
        """Run the simulator in interactive mode."""
        self.display_banner()
        self.display_ethical_warning()
        
        try:
            while True:
                print("\n" + "="*50)
                print("🎮 INTERACTIVE MODE")
                print("="*50)
                
                # Select target hash
                target_hash = self.select_target_hash()
                
                # Select attack method
                method = self.select_attack_method()
                
                # Get additional parameters
                kwargs = {}
                if method == 'brute_force':
                    try:
                        max_length = int(input("Enter max password length (1-8): "))
                        max_length = max(1, min(8, max_length))
                        kwargs['max_length'] = max_length
                    except ValueError:
                        kwargs['max_length'] = 8
                
                if method == 'ai':
                    context = input("Enter password context (optional): ").strip()
                    if context:
                        kwargs['context'] = context
                
                # Run attack
                result = self.run_attack(target_hash, method, **kwargs)
                
                # Display results
                self.display_results(result)
                
                # Ask if user wants to continue
                continue_choice = input("\n🔁 Run another attack? (y/N): ").strip().lower()
                if continue_choice != 'y':
                    break
            
            # Save results and display summary
            self.save_results()
            self.display_summary()
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Session interrupted by user.")
            self.save_results()
            self.display_summary()
    
    def run_from_args(self, args):
        """Run the simulator with command line arguments."""
        self.display_banner()
        self.display_ethical_warning()
        
        # Validate target hash
        target_hash = args.target
        if not target_hash:
            print("❌ Target hash is required.")
            return
        
        # Validate method
        method = args.method
        if not self.config.is_method_allowed(method):
            print(f"❌ Invalid attack method: {method}")
            return
        
        # Prepare kwargs
        kwargs = {}
        if method == 'brute_force' and args.length:
            kwargs['max_length'] = args.length
        
        if method == 'ai' and args.context:
            kwargs['context'] = args.context
        
        # Run attack
        result = self.run_attack(target_hash, method, **kwargs)
        
        # Display results
        self.display_results(result)
        
        # Save results
        self.save_results()
        
        # Display summary
        self.display_summary()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Password Cracker Simulator (Educational Only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive
  python main.py --method dictionary --target "fake_hash_here"
  python main.py --method ai --target "fake_hash_here" --context "user's birthday"
        """
    )
    
    parser.add_argument(
        '--method',
        choices=['brute_force', 'dictionary', 'rule_based', 'ai'],
        default='ai',
        help='Attack method to use (default: ai)'
    )
    
    parser.add_argument(
        '--target',
        help='Target hash to crack (synthetic only)'
    )
    
    parser.add_argument(
        '--length',
        type=int,
        help='Maximum password length for brute force (1-8)'
    )
    
    parser.add_argument(
        '--context',
        help='Context information for AI-powered attacks'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # Create simulator instance
    simulator = PasswordCrackerSimulator()
    
    try:
        if args.interactive or (not args.target and not args.interactive):
            simulator.interactive_mode()
        else:
            simulator.run_from_args(args)
    
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
