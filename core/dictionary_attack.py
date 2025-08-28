"""
Dictionary Attack Module

Simulates a dictionary attack using common passwords and variations.
"""

import time
import os
from typing import Optional, Tuple, List
from utils.hash_utils import verify_hash


class DictionaryAttack:
    """Dictionary-based password cracking simulation."""
    
    def __init__(self, wordlist_path: str = "data/wordlist.txt"):
        self.wordlist_path = wordlist_path
        self.attempts = 0
        self.start_time = None
        self.end_time = None
        self.words = self._load_wordlist()
    
    def _load_wordlist(self) -> List[str]:
        """Load words from the wordlist file."""
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            # Fallback to common passwords if wordlist not found
            return ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome']
    
    def crack(self, target_hash: str) -> Tuple[Optional[str], int, float]:
        """Attempt to crack password using dictionary attack."""
        if not self._validate_input(target_hash):
            raise ValueError("Invalid input detected. Only synthetic hashes allowed.")
        
        self.attempts = 0
        self.start_time = time.time()
        
        print(f"📚 Starting Dictionary Attack...")
        print(f"📖 Loaded {len(self.words)} words from dictionary")
        
        for word in self.words:
            self.attempts += 1
            
            # Try the word as-is
            if verify_hash(word, target_hash):
                return self._success(word)
            
            # Try common variations
            variations = self._generate_variations(word)
            for variation in variations:
                self.attempts += 1
                if verify_hash(variation, target_hash):
                    return self._success(variation)
        
        return self._failure()
    
    def _generate_variations(self, word: str) -> List[str]:
        """Generate common password variations."""
        variations = []
        
        # Capitalize first letter
        variations.append(word.capitalize())
        
        # Add common numbers
        for num in ['123', '1234', '12345', '123456', '1', '2', '3']:
            variations.append(word + num)
            variations.append(num + word)
        
        # Add common symbols
        for symbol in ['!', '@', '#', '$', '%', '&', '*']:
            variations.append(word + symbol)
            variations.append(symbol + word)
        
        return variations
    
    def _success(self, password: str) -> Tuple[str, int, float]:
        """Handle successful password crack."""
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        print(f"✅ Password Found: {password}")
        print(f"⏱️ Time taken: {time_taken:.2f} seconds")
        print(f"📊 Attempts made: {self.attempts}")
        
        return password, self.attempts, time_taken
    
    def _failure(self) -> Tuple[None, int, float]:
        """Handle failed password crack."""
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        print(f"❌ Password not found in dictionary")
        print(f"⏱️ Time taken: {time_taken:.2f} seconds")
        print(f"📊 Total attempts: {self.attempts}")
        
        return None, self.attempts, time_taken
    
    def _validate_input(self, target_hash: str) -> bool:
        """Validate input is safe for simulation."""
        suspicious_patterns = ['$2b$', '$2a$', '$1$', '$6$', '$5$']
        for pattern in suspicious_patterns:
            if target_hash.startswith(pattern):
                print(f"⚠️ Warning: Hash pattern '{pattern}' detected!")
                return False
        return True
    
    def get_stats(self) -> dict:
        """Get attack statistics."""
        if self.start_time is None:
            return {}
        
        time_taken = (self.end_time or time.time()) - self.start_time
        return {
            'method': 'Dictionary Attack',
            'attempts': self.attempts,
            'time_taken': time_taken,
            'words_loaded': len(self.words),
            'success': self.attempts > 0 and self.end_time is not None
        }
