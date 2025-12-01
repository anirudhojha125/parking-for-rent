#!/usr/bin/env python3
"""
Test script for Smart Park System
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from app import create_app
        from models.models import User, ParkingSpace, Booking, Feedback
        from forms.auth import RegistrationForm, LoginForm
        from forms.parking import ParkingSpaceForm, BookingForm
        from forms.feedback import FeedbackForm
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_app_creation():
    """Test that the app can be created"""
    try:
        from app import create_app
        app = create_app()
        print("✓ App creation successful")
        return True
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Smart Park System tests...\n")
    
    tests = [
        test_imports,
        test_app_creation
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())