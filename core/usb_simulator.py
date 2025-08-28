"""
USB Device Password Simulator Module

This module simulates password-protected USB devices for educational purposes.
It ONLY works with synthetic data and cannot crack real device passwords.
"""

import time
import random
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Types of USB devices that can be simulated."""
    FLASH_DRIVE = "flash_drive"
    EXTERNAL_HDD = "external_hdd"
    USB_SSD = "usb_ssd"
    ENCRYPTED_DEVICE = "encrypted_device"
    SMART_CARD = "smart_card"


class SecurityLevel(Enum):
    """Security levels for simulated devices."""
    BASIC = "basic"           # Simple password protection
    STANDARD = "standard"     # Standard encryption
    ADVANCED = "advanced"     # Advanced encryption with salt
    MILITARY = "military"     # Military-grade encryption


@dataclass
class SimulatedDevice:
    """Represents a simulated USB device."""
    device_id: str
    device_type: DeviceType
    security_level: SecurityLevel
    password_hash: str
    password: str
    description: str
    max_attempts: int
    lockout_threshold: int
    encryption_algorithm: str
    salt: Optional[str] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class USBDeviceSimulator:
    """
    Simulates password-protected USB devices for educational purposes.
    
    This simulator creates fake devices with synthetic passwords to teach
    about device security without any risk of real device damage.
    """
    
    def __init__(self):
        self.devices: Dict[str, SimulatedDevice] = {}
        self.attack_logs: List[Dict] = []
        self._initialize_device_templates()
    
    def _initialize_device_templates(self):
        """Initialize templates for different device types."""
        self.device_templates = {
            DeviceType.FLASH_DRIVE: {
                'max_attempts': 5,
                'lockout_threshold': 3,
                'encryption_algorithm': 'AES-256',
                'common_passwords': ['password', '123456', 'admin', 'usb', 'drive']
            },
            DeviceType.EXTERNAL_HDD: {
                'max_attempts': 10,
                'lockout_threshold': 5,
                'encryption_algorithm': 'AES-256-XTS',
                'common_passwords': ['harddrive', 'backup', 'storage', 'data', 'secure']
            },
            DeviceType.USB_SSD: {
                'max_attempts': 15,
                'lockout_threshold': 7,
                'encryption_algorithm': 'AES-256-GCM',
                'common_passwords': ['ssd', 'fast', 'performance', 'speed', 'reliable']
            },
            DeviceType.ENCRYPTED_DEVICE: {
                'max_attempts': 20,
                'lockout_threshold': 10,
                'encryption_algorithm': 'ChaCha20-Poly1305',
                'common_passwords': ['encrypted', 'secret', 'private', 'confidential', 'secure']
            },
            DeviceType.SMART_CARD: {
                'max_attempts': 3,
                'lockout_threshold': 2,
                'encryption_algorithm': 'RSA-2048',
                'common_passwords': ['pin', 'card', 'smart', 'access', 'identity']
            }
        }
    
    def generate_device_id(self) -> str:
        """Generate a unique device identifier."""
        timestamp = int(time.time() * 1000)
        random_part = random.randint(1000, 9999)
        return f"USB_{timestamp}_{random_part}"
    
    def create_simulated_device(
        self, 
        device_type: DeviceType, 
        security_level: SecurityLevel,
        custom_password: Optional[str] = None
    ) -> SimulatedDevice:
        """
        Create a new simulated USB device.
        
        Args:
            device_type: Type of device to simulate
            security_level: Security level of the device
            custom_password: Optional custom password (if None, generates random)
            
        Returns:
            SimulatedDevice instance
        """
        template = self.device_templates[device_type]
        
        # Generate or use custom password
        if custom_password:
            password = custom_password
        else:
            password = random.choice(template['common_passwords'])
        
        # Generate hash based on security level
        if security_level == SecurityLevel.BASIC:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            salt = None
        elif security_level == SecurityLevel.STANDARD:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            salt = None
        elif security_level == SecurityLevel.ADVANCED:
            salt = hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        else:  # MILITARY
            salt = hashlib.sha512(str(random.random()).encode()).hexdigest()[:32]
            password_hash = hashlib.sha512((password + salt + "military").encode()).hexdigest()
        
        device = SimulatedDevice(
            device_id=self.generate_device_id(),
            device_type=device_type,
            security_level=security_level,
            password_hash=password_hash,
            password=password,
            description=f"Simulated {device_type.value.replace('_', ' ').title()}",
            max_attempts=template['max_attempts'],
            lockout_threshold=template['lockout_threshold'],
            encryption_algorithm=template['encryption_algorithm'],
            salt=salt
        )
        
        self.devices[device.device_id] = device
        return device
    
    def detect_device(self, device_id: str) -> Optional[SimulatedDevice]:
        """
        Simulate detecting a USB device.
        
        Args:
            device_id: ID of the device to detect
            
        Returns:
            SimulatedDevice if found, None otherwise
        """
        return self.devices.get(device_id)
    
    def list_devices(self) -> List[SimulatedDevice]:
        """List all simulated devices."""
        return list(self.devices.values())
    
    def attempt_unlock(
        self, 
        device_id: str, 
        password_attempt: str,
        attack_method: str
    ) -> Dict:
        """
        Attempt to unlock a simulated device.
        
        Args:
            device_id: ID of the device to unlock
            password_attempt: Password to try
            attack_method: Method used for the attempt
            
        Returns:
            Dictionary with unlock attempt results
        """
        device = self.devices.get(device_id)
        if not device:
            return {
                'success': False,
                'error': 'Device not found',
                'device_locked': False
            }
        
        # Check if device is locked out
        failed_attempts = len([log for log in self.attack_logs 
                             if log['device_id'] == device_id and not log['success']])
        
        if failed_attempts >= device.lockout_threshold:
            return {
                'success': False,
                'error': 'Device is temporarily locked due to too many failed attempts',
                'device_locked': True,
                'remaining_lockout_time': 300  # 5 minutes
            }
        
        # Verify password
        if device.salt:
            attempt_hash = hashlib.sha256((password_attempt + device.salt).encode()).hexdigest()
        else:
            attempt_hash = hashlib.sha256(password_attempt.encode()).hexdigest()
        
        success = attempt_hash == device.password_hash
        
        # Log the attempt
        log_entry = {
            'timestamp': time.time(),
            'device_id': device_id,
            'password_attempt': password_attempt,
            'success': success,
            'attack_method': attack_method,
            'device_type': device.device_type.value,
            'security_level': device.security_level.value
        }
        self.attack_logs.append(log_entry)
        
        if success:
            return {
                'success': True,
                'message': f'Device {device_id} unlocked successfully!',
                'details': {
                    'device_type': device.device_type.value,
                    'security_level': device.security_level.value,
                    'encryption_algorithm': device.encryption_algorithm,
                    'attempts_made': failed_attempts + 1
                }
            }
        else:
            remaining_attempts = device.max_attempts - (failed_attempts + 1)
            return {
                'success': False,
                'error': f'Incorrect password. {remaining_attempts} attempts remaining.',
                'device_locked': False,
                'remaining_attempts': remaining_attempts
            }
    
    def get_device_info(self, device_id: str) -> Optional[Dict]:
        """Get detailed information about a device."""
        device = self.devices.get(device_id)
        if not device:
            return None
        
        failed_attempts = len([log for log in self.attack_logs 
                             if log['device_id'] == device_id and not log['success']])
        
        return {
            'device_id': device.device_id,
            'device_type': device.device_type.value,
            'security_level': device.security_level.value,
            'description': device.description,
            'encryption_algorithm': device.encryption_algorithm,
            'max_attempts': device.max_attempts,
            'lockout_threshold': device.lockout_threshold,
            'failed_attempts': failed_attempts,
            'is_locked': failed_attempts >= device.lockout_threshold,
            'created_at': device.created_at,
            'salt': device.salt
        }
    
    def reset_device(self, device_id: str) -> bool:
        """Reset a device's lockout status."""
        if device_id in self.devices:
            # Remove failed attempt logs for this device
            self.attack_logs = [log for log in self.attack_logs 
                               if log['device_id'] != device_id]
            return True
        return False
    
    def get_attack_statistics(self) -> Dict:
        """Get statistics about attack attempts."""
        total_attempts = len(self.attack_logs)
        successful_attempts = len([log for log in self.attack_logs if log['success']])
        failed_attempts = total_attempts - successful_attempts
        
        method_stats = {}
        for log in self.attack_logs:
            method = log['attack_method']
            if method not in method_stats:
                method_stats[method] = {'total': 0, 'successful': 0}
            method_stats[method]['total'] += 1
            if log['success']:
                method_stats[method]['successful'] += 1
        
        return {
            'total_attempts': total_attempts,
            'successful_attempts': successful_attempts,
            'failed_attempts': failed_attempts,
            'success_rate': (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0,
            'method_statistics': method_stats,
            'devices_targeted': len(set(log['device_id'] for log in self.attack_logs))
        }
    
    def clear_all_data(self):
        """Clear all simulated devices and logs (for testing)."""
        self.devices.clear()
        self.attack_logs.clear()


# Convenience functions for easy access
def create_flash_drive(password: str = None) -> SimulatedDevice:
    """Create a simulated USB flash drive."""
    simulator = USBDeviceSimulator()
    return simulator.create_simulated_device(
        DeviceType.FLASH_DRIVE, 
        SecurityLevel.STANDARD, 
        password
    )

def create_external_hdd(password: str = None) -> SimulatedDevice:
    """Create a simulated external hard drive."""
    simulator = USBDeviceSimulator()
    return simulator.create_simulated_device(
        DeviceType.EXTERNAL_HDD, 
        SecurityLevel.ADVANCED, 
        password
    )

def create_encrypted_device(password: str = None) -> SimulatedDevice:
    """Create a simulated encrypted device."""
    simulator = USBDeviceSimulator()
    return simulator.create_simulated_device(
        DeviceType.ENCRYPTED_DEVICE, 
        SecurityLevel.MILITARY, 
        password
    )
