#!/usr/bin/env python3
"""
USB Device Simulator Demo

This script demonstrates the USB simulator functionality
with interactive examples and real-time feedback.
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.usb_simulator import (
    USBDeviceSimulator, 
    DeviceType, 
    SecurityLevel
)

def print_header():
    """Print the demo header."""
    print("🔐 USB Device Simulator Demo")
    print("=" * 50)
    print("This demo showcases the USB device simulation capabilities")
    print("for educational purposes. All data is synthetic.")
    print()

def print_menu():
    """Print the main menu."""
    print("📋 Available Options:")
    print("1. Create a USB Flash Drive")
    print("2. Create an External HDD")
    print("3. Create an Encrypted Device")
    print("4. Create a Smart Card")
    print("5. Quick Setup (Multiple Devices)")
    print("6. Test Device Unlocking")
    print("7. View Statistics")
    print("8. Reset All Devices")
    print("9. Exit")
    print()

def create_device_demo(simulator):
    """Demonstrate device creation."""
    print("🔧 Device Creation Demo")
    print("-" * 30)
    
    # Show device types
    print("Available device types:")
    for i, device_type in enumerate(DeviceType, 1):
        print(f"  {i}. {device_type.value.replace('_', ' ').title()}")
    
    print("\nAvailable security levels:")
    for i, security_level in enumerate(SecurityLevel, 1):
        print(f"  {i}. {security_level.value.title()}")
    
    print()
    
    try:
        # Get user choice
        device_choice = input("Select device type (1-5): ").strip()
        security_choice = input("Select security level (1-4): ").strip()
        custom_password = input("Custom password (or press Enter for random): ").strip()
        
        # Convert choices to enums
        device_type = list(DeviceType)[int(device_choice) - 1]
        security_level = list(SecurityLevel)[int(security_level) - 1]
        
        # Create device
        print(f"\n🔧 Creating {device_type.value} with {security_level.value} security...")
        device = simulator.create_simulated_device(
            device_type, 
            security_level,
            custom_password if custom_password else None
        )
        
        print(f"✅ Device created successfully!")
        print(f"   ID: {device.device_id}")
        print(f"   Type: {device.device_type.value}")
        print(f"   Security: {device.security_level.value}")
        print(f"   Algorithm: {device.encryption_algorithm}")
        print(f"   Max Attempts: {device.max_attempts}")
        print(f"   Lockout Threshold: {device.lockout_threshold}")
        
        if custom_password:
            print(f"   Password: {custom_password}")
        else:
            print(f"   Password: {device.password}")
        
        return device
        
    except (ValueError, IndexError):
        print("❌ Invalid choice. Please try again.")
        return None
    except Exception as e:
        print(f"❌ Error creating device: {e}")
        return None

def quick_setup_demo(simulator):
    """Demonstrate quick setup with multiple devices."""
    print("🚀 Quick Setup Demo")
    print("-" * 30)
    
    print("Creating pre-configured devices...")
    
    devices = []
    
    # Flash drive (easy)
    flash_drive = simulator.create_simulated_device(
        DeviceType.FLASH_DRIVE,
        SecurityLevel.BASIC,
        "password"
    )
    devices.append(flash_drive)
    print(f"✅ Flash Drive: {flash_drive.device_id} (password: password)")
    
    # External HDD (medium)
    external_hdd = simulator.create_simulated_device(
        DeviceType.EXTERNAL_HDD,
        SecurityLevel.STANDARD,
        "backup123"
    )
    devices.append(external_hdd)
    print(f"✅ External HDD: {external_hdd.device_id} (password: backup123)")
    
    # Encrypted device (hard)
    encrypted_device = simulator.create_simulated_device(
        DeviceType.ENCRYPTED_DEVICE,
        SecurityLevel.ADVANCED,
        "secret2024"
    )
    devices.append(encrypted_device)
    print(f"✅ Encrypted Device: {encrypted_device.device_id} (password: secret2024)")
    
    print(f"\n🎯 Created {len(devices)} devices for testing!")
    return devices

def unlock_demo(simulator):
    """Demonstrate device unlocking."""
    print("🔓 Device Unlocking Demo")
    print("-" * 30)
    
    # List available devices
    devices = simulator.list_devices()
    if not devices:
        print("❌ No devices available. Create some devices first.")
        return
    
    print("Available devices:")
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device.device_type.value} - {device.device_id[:12]}...")
    
    try:
        device_choice = input("\nSelect device (1-{}): ".format(len(devices))).strip()
        device = devices[int(device_choice) - 1]
        
        print(f"\n🔍 Attempting to unlock: {device.device_type.value}")
        print(f"   Device ID: {device.device_id}")
        print(f"   Security Level: {device.security_level.value}")
        print(f"   Algorithm: {device.encryption_algorithm}")
        
        # Try wrong passwords first
        wrong_passwords = ["wrong", "incorrect", "bad", "fail"]
        print(f"\n❌ Trying wrong passwords...")
        
        for password in wrong_passwords:
            result = simulator.attempt_unlock(device.device_id, password, "demo")
            print(f"   '{password}': {result['error']}")
            
            if result.get('device_locked'):
                print(f"   🔒 Device locked after {len(wrong_passwords)} attempts!")
                break
        
        # Try correct password
        print(f"\n✅ Trying correct password...")
        result = simulator.attempt_unlock(device.device_id, device.password, "demo")
        
        if result['success']:
            print(f"   🎉 Success! {result['message']}")
            print(f"   Attempts made: {result['details']['attempts_made']}")
        else:
            print(f"   ❌ Failed: {result['error']}")
        
    except (ValueError, IndexError):
        print("❌ Invalid choice. Please try again.")
    except Exception as e:
        print(f"❌ Error during unlock demo: {e}")

def statistics_demo(simulator):
    """Demonstrate statistics collection."""
    print("📊 Statistics Demo")
    print("-" * 30)
    
    stats = simulator.get_attack_statistics()
    
    print("Attack Statistics:")
    print(f"   Total Attempts: {stats['total_attempts']}")
    print(f"   Successful: {stats['successful_attempts']}")
    print(f"   Failed: {stats['failed_attempts']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    print(f"   Devices Targeted: {stats['devices_targeted']}")
    
    if stats['method_statistics']:
        print("\nMethod Statistics:")
        for method, data in stats['method_statistics'].items():
            success_rate = (data['successful'] / data['total'] * 100) if data['total'] > 0 else 0
            print(f"   {method}: {data['successful']}/{data['total']} ({success_rate:.1f}%)")

def reset_devices_demo(simulator):
    """Demonstrate device reset functionality."""
    print("🔄 Device Reset Demo")
    print("-" * 30)
    
    devices = simulator.list_devices()
    if not devices:
        print("❌ No devices to reset.")
        return
    
    print(f"Found {len(devices)} devices.")
    confirm = input("Are you sure you want to reset all devices? (y/N): ").strip().lower()
    
    if confirm == 'y':
        print("🔄 Resetting all devices...")
        
        for device in devices:
            success = simulator.reset_device(device.device_id)
            if success:
                print(f"   ✅ Reset {device.device_type.value}")
            else:
                print(f"   ❌ Failed to reset {device.device_type.value}")
        
        print("🎯 Reset complete!")
    else:
        print("Reset cancelled.")

def main():
    """Main demo function."""
    print_header()
    
    # Initialize simulator
    simulator = USBDeviceSimulator()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == '1':
                create_device_demo(simulator)
            elif choice == '2':
                create_device_demo(simulator)
            elif choice == '3':
                create_device_demo(simulator)
            elif choice == '4':
                create_device_demo(simulator)
            elif choice == '5':
                quick_setup_demo(simulator)
            elif choice == '6':
                unlock_demo(simulator)
            elif choice == '7':
                statistics_demo(simulator)
            elif choice == '8':
                reset_devices_demo(simulator)
            elif choice == '9':
                print("\n👋 Thanks for trying the USB Device Simulator!")
                print("Remember: This is for educational purposes only.")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
