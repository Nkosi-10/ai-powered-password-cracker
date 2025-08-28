"""
Rule-Based Attack Module

Simulates password cracking using common patterns and rules.
"""

import time
import string
from typing import Optional, Tuple, List
from utils.hash_utils import verify_hash


class RuleBasedAttack:
    """Rule-based password cracking simulation."""
    
    def __init__(self):
        self.attempts = 0
        self.start_time = None
        self.end_time = None
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[callable]:
        """Initialize password generation rules."""
        return [
            self._common_patterns,
            self._keyboard_patterns,
            self._date_patterns,
            self._name_patterns,
            self._leet_speak
        ]
    
    def crack(self, target_hash: str) -> Tuple[Optional[str], int, float]:
        """Attempt to crack password using rule-based approach."""
        if not self._validate_input(target_hash):
            raise ValueError("Invalid input detected. Only synthetic hashes allowed.")
        
        self.attempts = 0
        self.start_time = time.time()
        
        print(f"🎯 Starting Rule-Based Attack...")
        print(f"📋 Using {len(self.rules)} rule categories")
        
        for rule_func in self.rules:
            passwords = rule_func()
            for password in passwords:
                self.attempts += 1
                
                if self.attempts % 100 == 0:
                    print(f"   Attempts: {self.attempts} | Current: {password}")
                
                if verify_hash(password, target_hash):
                    return self._success(password)
        
        return self._failure()
    
    def _common_patterns(self) -> List[str]:
        """Generate common password patterns."""
        patterns = []
        
        # Sequential numbers
        for length in range(4, 10):
            for start in range(10):
                if start + length <= 10:
                    pattern = ''.join(str(i) for i in range(start, start + length))
                    patterns.append(pattern)
        
        # Repeated characters
        for char in ['1', '2', '3', 'a', 'b', 'c']:
            for length in range(4, 9):
                patterns.append(char * length)
        
        # Common words with numbers
        words = ['password', 'admin', 'user', 'test', 'demo']
        for word in words:
            for num in range(100):
                patterns.append(f"{word}{num}")
                patterns.append(f"{num}{word}")
        
        return patterns
    
    def _keyboard_patterns(self) -> List[str]:
        """Generate keyboard-based patterns."""
        patterns = []
        
        # QWERTY patterns
        qwerty_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]
        
        for row in qwerty_rows:
            for length in range(4, len(row) + 1):
                for start in range(len(row) - length + 1):
                    patterns.append(row[start:start + length])
                    patterns.append(row[start:start + length][::-1])  # Reverse
        
        # Number pad patterns
        numpad = '1234567890'
        for length in range(4, 7):
            for start in range(len(numpad) - length + 1):
                patterns.append(numpad[start:start + length])
        
        return patterns
    
    def _date_patterns(self) -> List[str]:
        """Generate date-based patterns."""
        patterns = []
        
        # Common years
        years = ['2024', '2023', '2022', '2021', '2020', '1990', '1980']
        
        # Month-day combinations
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        days = [f"{i:02d}" for i in range(1, 32)]
        
        for year in years:
            patterns.append(year)
            for month in months:
                patterns.append(f"{month}{year}")
                patterns.append(f"{year}{month}")
                for day in days:
                    patterns.append(f"{month}{day}{year}")
                    patterns.append(f"{year}{month}{day}")
        
        return patterns
    
    def _name_patterns(self) -> List[str]:
        """Generate name-based patterns."""
        patterns = []
        
        names = ['john', 'jane', 'admin', 'user', 'test', 'demo', 'guest']
        
        for name in names:
            patterns.append(name)
            patterns.append(name.capitalize())
            patterns.append(name.upper())
            
            # Add numbers
            for num in range(100):
                patterns.append(f"{name}{num}")
                patterns.append(f"{num}{name}")
            
            # Add symbols
            for symbol in ['!', '@', '#', '$', '%']:
                patterns.append(f"{name}{symbol}")
                patterns.append(f"{symbol}{name}")
        
        return patterns
    
    def _leet_speak(self) -> List[str]:
        """Generate leet speak variations."""
        patterns = []
        
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'
        }
        
        words = ['password', 'admin', 'user', 'test']
        
        for word in words:
            patterns.append(word)
            
            # Apply leet speak substitutions
            leet_word = word
            for char, replacement in leet_map.items():
                leet_word = leet_word.replace(char, replacement)
            patterns.append(leet_word)
        
        return patterns
    
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
        
        print(f"❌ Password not found using rules")
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
            'method': 'Rule-Based Attack',
            'attempts': self.attempts,
            'time_taken': time_taken,
            'rules_used': len(self.rules),
            'success': self.attempts > 0 and self.end_time is not None
        }
