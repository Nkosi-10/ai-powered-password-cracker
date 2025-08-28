"""
Configuration Module

Contains project constants, settings, and configuration options.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for the password cracker simulator."""
    
    # Project information
    PROJECT_NAME = "AI-Powered Password Cracker Simulator"
    VERSION = "1.0.0"
    AUTHOR = "Educational Project"
    
    # Security settings
    MAX_PASSWORD_LENGTH = 12
    MIN_PASSWORD_LENGTH = 1
    MAX_BRUTE_FORCE_LENGTH = 8  # Limit brute force to prevent excessive runtime
    
    # Character sets
    CHARSETS = {
        'lowercase': 'abcdefghijklmnopqrstuvwxyz',
        'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'numbers': '0123456789',
        'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?',
        'alphanumeric': 'abcdefghijklmnopqrstuvwxyz0123456789',
        'full': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
    }
    
    # Attack method settings
    ATTACK_METHODS = {
        'brute_force': {
            'name': 'Brute Force',
            'description': 'Try all possible character combinations',
            'max_length': 8,
            'timeout': 300  # 5 minutes
        },
        'dictionary': {
            'name': 'Dictionary Attack',
            'description': 'Try common passwords and variations',
            'max_length': 20,
            'timeout': 60
        },
        'rule_based': {
            'name': 'Rule-Based',
            'description': 'Use common password patterns and rules',
            'max_length': 15,
            'timeout': 120
        },
        'ai': {
            'name': 'AI-Powered',
            'description': 'Use AI to select optimal attack strategy',
            'max_length': 20,
            'timeout': 180
        }
    }
    
    # File paths
    DATA_DIR = "data"
    RESULTS_DIR = "results"
    WORDLIST_PATH = os.path.join(DATA_DIR, "wordlist.txt")
    FAKE_PASSWORDS_PATH = os.path.join(DATA_DIR, "fake_passwords.json")
    LOG_PATH = os.path.join(RESULTS_DIR, "log.json")
    
    # AI settings
    AI_SETTINGS = {
        'max_retries': 3,
        'timeout': 30,
        'max_tokens': 1000,
        'temperature': 0.7
    }
    
    # Logging settings
    LOGGING = {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'backup_count': 5
    }
    
    # Performance settings
    PERFORMANCE = {
        'max_attempts_per_second': 10000,
        'progress_update_interval': 1000,
        'memory_limit_mb': 512
    }
    
    # Ethical safeguards
    SAFEGUARDS = {
        'check_real_hashes': True,
        'max_hash_length': 128,
        'suspicious_patterns': [
            '$2b$',  # bcrypt
            '$2a$',  # bcrypt
            '$1$',   # MD5 crypt
            '$6$',   # SHA-512 crypt
            '$5$',   # SHA-256 crypt
            'pbkdf2',  # PBKDF2
            'scrypt'   # scrypt
        ],
        'blocked_domains': [
            'admin', 'root', 'system', 'administrator'
        ]
    }
    
    @classmethod
    def get_attack_method_info(cls, method: str) -> Dict[str, Any]:
        """Get information about a specific attack method."""
        return cls.ATTACK_METHODS.get(method, {})
    
    @classmethod
    def get_charset(cls, charset_name: str) -> str:
        """Get a character set by name."""
        return cls.CHARSETS.get(charset_name, cls.CHARSETS['alphanumeric'])
    
    @classmethod
    def is_method_allowed(cls, method: str) -> bool:
        """Check if an attack method is allowed."""
        return method in cls.ATTACK_METHODS
    
    @classmethod
    def get_max_length_for_method(cls, method: str) -> int:
        """Get maximum password length for a specific method."""
        method_info = cls.get_attack_method_info(method)
        return method_info.get('max_length', cls.MAX_PASSWORD_LENGTH)
    
    @classmethod
    def get_timeout_for_method(cls, method: str) -> int:
        """Get timeout for a specific method."""
        method_info = cls.get_attack_method_info(method)
        return method_info.get('timeout', 60)
    
    @classmethod
    def validate_password_length(cls, length: int) -> bool:
        """Validate if a password length is within allowed range."""
        return cls.MIN_PASSWORD_LENGTH <= length <= cls.MAX_PASSWORD_LENGTH
    
    @classmethod
    def get_suspicious_patterns(cls) -> list:
        """Get list of suspicious hash patterns."""
        return cls.SAFEGUARDS['suspicious_patterns']
    
    @classmethod
    def should_check_real_hashes(cls) -> bool:
        """Check if real hash detection is enabled."""
        return cls.SAFEGUARDS['check_real_hashes']
    
    @classmethod
    def get_project_info(cls) -> Dict[str, str]:
        """Get basic project information."""
        return {
            'name': cls.PROJECT_NAME,
            'version': cls.VERSION,
            'author': cls.AUTHOR
        }
