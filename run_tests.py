"""
TrucksUp Automation - Test Runner
==================================
Simple script to run tests with one command.
"""

import subprocess
import sys
import os
from datetime import datetime


def run_new_user_test():
    """New user onboarding test run karo"""
    print("Running: New User Onboarding Test")
    cmd = "pytest tests/test_onboarding.py::TestTrucksUpOnboarding::test_new_user_onboarding -v --html=reports/new_user_report.html"
    subprocess.run(cmd, shell=True)


def run_existing_user_test():
    """Existing user login test run karo"""
    print("Running: Existing User Login Test")
    cmd = "pytest tests/test_onboarding.py::TestTrucksUpOnboarding::test_existing_user_login -v --html=reports/existing_user_report.html"
    subprocess.run(cmd, shell=True)


def run_all_tests():
    """Saare tests run karo"""
    print("Running: All Tests")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd = f"pytest tests/ -v --html=reports/report_{timestamp}.html"
    subprocess.run(cmd, shell=True)


def main():
    print("=" * 60)
    print("TRUCKSUP AUTOMATION - TEST RUNNER")
    print("=" * 60)
    print("\n1. New User Onboarding")
    print("2. Existing User Login")
    print("3. Run All Tests")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ").strip()

    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    if choice == "1":
        run_new_user_test()
    elif choice == "2":
        run_existing_user_test()
    elif choice == "3":
        run_all_tests()
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
