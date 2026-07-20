#!/usr/bin/env python3
"""
Reset Admin Password Script
"""

import sys
import json
from pathlib import Path
from getpass import getpass
import hashlib

def reset_admin():
    """Reset admin credentials"""
    config_path = Path('/opt/mediaauto/config/settings.json')
    
    if not config_path.exists():
        print("[✗] Configuration file not found")
        sys.exit(1)
    
    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("[INFO] Admin Password Reset")
    print("="*50)
    
    # Get new username
    username = input("Enter new admin username (default: admin): ").strip()
    if not username:
        username = 'admin'
    
    # Get new password
    while True:
        password = getpass("Enter new admin password: ")
        password_confirm = getpass("Confirm password: ")
        
        if password == password_confirm:
            break
        print("[✗] Passwords do not match. Try again.")
    
    # Hash password (simple example - use bcrypt in production)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Update configuration
    config['panel']['username'] = username
    config['panel']['password'] = password_hash  # Should be hashed properly
    
    # Save configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print("[✓] Admin credentials updated successfully")
    print(f"[✓] Username: {username}")
    print("[!] Please restart the bot: sudo systemctl restart mediaauto")

if __name__ == '__main__':
    try:
        reset_admin()
    except KeyboardInterrupt:
        print("\n[!] Cancelled")
        sys.exit(1)