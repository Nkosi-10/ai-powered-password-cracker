"""
Brute Force Attack Module

Simulates a brute force attack by trying all possible character combinations.
This is the most comprehensive but slowest attack method.
"""

import time
import string
import itertools
from typing import Optional, Tuple
from utils.hash_utils import verify_hash


class BruteForceAttack:
    """
    Implements a brute force password cracking simulation.
    
    This class simulates trying all possible character combinations
    up to a specified length. It's designed for educational purposes
    and only works with synthetic data.
    """
    
    def __init__(self, charset: str = None):
        """
        Initialize the brute force attack.
        
        Args:
            charset: Character set to use for password generation.
                    Defaults to lowercase letters + numbers.
        """
        self.charset = charset or (string.ascii_lowercase + string.digits)
        self.attempts = 0
        self.start_time = None
        self.end_time = None
    
    def crack(self, target_hash: str, max_length: int = 8) -> Tuple[Optional[str], int, float]:
        """
        Attempt to crack a password using brute force.
        
        Args:
            target_hash: The hash to crack (must be synthetic)
            max_length: Maximum password length to try
            
        Returns:
            Tuple of (cracked_password, attempts_made, time_taken)
        """
        if not self._validate_input(target_hash):
            raise ValueError("Invalid input detected. Only synthetic hashes allowed.")
        
        self.attempts = 0
        self.start_time = time.time()
        
        print(f"🔨 Starting Brute Force Attack...")
        print(f"📏 Max length: {max_length}")
        print(f"🔤 Character set: {len(self.charset)} characters")
        
        # Try passwords of increasing length
        for length in range(1, max_length + 1):
            print(f"🔍 Trying passwords of length {length}...")
            
            # Generate all combinations of current length
            for password in itertools.product(self.charset, repeat=length):
                self.attempts += 1
                password_str = ''.join(password)
                
                # Check every 1000 attempts to avoid overwhelming output
                if self.attempts % 1000 == 0:
                    print(f"   Attempts: {self.attempts:,} | Current: {password_str}")
                
                # Verify if this password matches the hash
                if verify_hash(password_str, target_hash):
                    self.end_time = time.time()
                    time_taken = self.end_time - self.start_time
                    
                    print(f"✅ Password Found: {password_str}")
                    print(f"⏱️ Time taken: {time_taken:.2f} seconds")
                    print(f"📊 Total attempts: {self.attempts:,}")
                    
                    return password_str, self.attempts, time_taken
        
        # If we get here, password wasn't found
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        print(f"❌ Password not found within {max_length} characters")
        print(f"⏱️ Time taken: {time_taken:.2f} seconds")
        print(f"📊 Total attempts: {self.attempts:,}")
        
        return None, self.attempts, time_taken
    
    def _validate_input(self, target_hash: str) -> bool:
        """
        Validate that the input is safe for simulation.
        
        Args:
            target_hash: Hash to validate
            
        Returns:
            True if input is safe, False otherwise
        """
        # Check for common real hash patterns
        suspicious_patterns = [
            '$2b$',  # bcrypt
            '$2a$',  # bcrypt
            '$1$',   # MD5 crypt
            '$6$',   # SHA-512 crypt
            '$5$',   # SHA-256 crypt
        ]
        
        for pattern in suspicious_patterns:
            if target_hash.startswith(pattern):
                print(f"⚠️ Warning: Hash pattern '{pattern}' detected!")
                print("   This appears to be a real hash. Only synthetic hashes allowed.")
                return False
        
        # Check hash length (most synthetic hashes are 64 chars for SHA-256)
        if len(target_hash) != 64:
            print(f"⚠️ Warning: Hash length {len(target_hash)} is unusual.")
            print("   Expected 64 characters for SHA-256 synthetic hashes.")
        
        return True
    
    def get_stats(self) -> dict:
        """
        Get statistics about the last cracking attempt.
        
        Returns:
            Dictionary containing attack statistics
        """
        if self.start_time is None:
            return {}
        
        time_taken = (self.end_time or time.time()) - self.start_time
        attempts_per_second = self.attempts / time_taken if time_taken > 0 else 0
        
        return {
            'method': 'Brute Force',
            'attempts': self.attempts,
            'time_taken': time_taken,
            'attempts_per_second': attempts_per_second,
            'charset_size': len(self.charset),
            'success': self.attempts > 0 and self.end_time is not None
        }
