#!/usr/bin/env python3
"""
Installation script for Smart Park System
"""

import subprocess
import sys

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def main():
    """Main installation function"""
    print("Installing Smart Park System dependencies...\n")
    
    if install_requirements():
        print("\nInstallation completed successfully! ✓")
        print("You can now run the application with: python app.py")
        return 0
    else:
        print("\nInstallation failed! ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())