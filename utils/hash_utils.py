"""
Hash Utilities Module

Provides functions for password hashing, verification, and synthetic hash generation.
"""

import hashlib
import secrets
import string
from typing import Optional


def hash_password(password: str, algorithm: str = 'sha256') -> str:
    """
    Hash a password using the specified algorithm.
    
    Args:
        password: Plain text password to hash
        algorithm: Hashing algorithm to use (default: sha256)
        
    Returns:
        Hashed password string
    """
    if algorithm == 'sha256':
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(password.encode('utf-8')).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(password.encode('utf-8')).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def verify_hash(password: str, target_hash: str, algorithm: str = 'sha256') -> bool:
    """
    Verify if a password matches a given hash.
    
    Args:
        password: Plain text password to check
        target_hash: Hash to compare against
        algorithm: Hashing algorithm used (default: sha256)
        
    Returns:
        True if password matches hash, False otherwise
    """
    password_hash = hash_password(password, algorithm)
    return password_hash == target_hash


def generate_synthetic_hash(password: str = None, algorithm: str = 'sha256') -> str:
    """
    Generate a synthetic hash for educational purposes.
    
    Args:
        password: Optional password to hash. If None, generates random password.
        algorithm: Hashing algorithm to use (default: sha256)
        
    Returns:
        Synthetic hash string
    """
    if password is None:
        # Generate a random password
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    
    return hash_password(password, algorithm)


def generate_fake_password_data(count: int = 10) -> list:
    """
    Generate fake password data for simulation.
    
    Args:
        count: Number of fake passwords to generate
        
    Returns:
        List of dictionaries with password and hash
    """
    fake_data = []
    
    # Common weak passwords
    common_passwords = [
        'password', '123456', 'qwerty', 'admin', 'letmein',
        'welcome', 'monkey', 'dragon', 'master', 'freedom',
        'hello', 'world', 'test', 'demo', 'guest'
    ]
    
    for i in range(min(count, len(common_passwords))):
        password = common_passwords[i]
        hash_value = hash_password(password)
        
        fake_data.append({
            'password': password,
            'hash': hash_value,
            'description': f'Common password #{i+1}',
            'difficulty': 'easy'
        })
    
    # Generate some random passwords
    remaining = count - len(common_passwords)
    for i in range(remaining):
        password = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        hash_value = hash_password(password)
        
        fake_data.append({
            'password': password,
            'hash': hash_value,
            'description': f'Random password #{i+1}',
            'difficulty': 'medium'
        })
    
    return fake_data


def validate_hash_format(hash_string: str) -> bool:
    """
    Validate if a hash string has the correct format.
    
    Args:
        hash_string: Hash string to validate
        
    Returns:
        True if format is valid, False otherwise
    """
    # Check if it's a hex string
    try:
        int(hash_string, 16)
    except ValueError:
        return False
    
    # Check length (SHA-256 = 64 chars, MD5 = 32 chars, SHA-1 = 40 chars)
    valid_lengths = [32, 40, 64]
    if len(hash_string) not in valid_lengths:
        return False
    
    return True


def get_hash_info(hash_string: str) -> dict:
    """
    Get information about a hash string.
    
    Args:
        hash_string: Hash string to analyze
        
    Returns:
        Dictionary with hash information
    """
    info = {
        'length': len(hash_string),
        'format': 'hex',
        'algorithm': 'unknown',
        'valid': validate_hash_format(hash_string)
    }
    
    # Determine algorithm based on length
    if len(hash_string) == 32:
        info['algorithm'] = 'MD5'
    elif len(hash_string) == 40:
        info['algorithm'] = 'SHA-1'
    elif len(hash_string) == 64:
        info['algorithm'] = 'SHA-256'
    
    return info
