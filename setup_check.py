"""
TrucksUp Automation - Setup Verification
=========================================
Run karo aur check karo sab kuch sahi hai ya nahi.
"""

import subprocess
import sys
import os


def check_command(cmd, name):
    """Command available hai ya nahi check karo"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] {name} is installed")
            return True
        else:
            print(f"[FAIL] {name} is NOT installed or not in PATH")
            return False
    except Exception as e:
        print(f"[FAIL] {name} check failed: {e}")
        return False


def main():
    print("=" * 60)
    print("TRUCKSUP AUTOMATION - SETUP VERIFICATION")
    print("=" * 60)

    checks = {
        "Python": "python --version",
        "pip": "pip --version",
        "Node.js": "node --version",
        "Appium": "appium --version",
        "ADB": "adb --version",
    }

    results = {}
    for name, cmd in checks.items():
        results[name] = check_command(cmd, name)

    print("\n" + "=" * 60)
    print("DEVICE CHECK")
    print("=" * 60)

    device_result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    if "device" in device_result.stdout and len(device_result.stdout.strip().split("\n")) > 1:
        print("[OK] Device(s) found:")
        print(device_result.stdout)
    else:
        print("[FAIL] No device connected! Please connect your phone/emulator.")
        results["Device"] = False

    print("\n" + "=" * 60)
    print("PYTHON LIBRARIES CHECK")
    print("=" * 60)

    libs = ["appium", "selenium", "pytest"]
    for lib in libs:
        try:
            __import__(lib)
            print(f"[OK] {lib} is installed")
            results[lib] = True
        except ImportError:
            print(f"[FAIL] {lib} is NOT installed. Run: pip install -r requirements.txt")
            results[lib] = False

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if all(results.values()):
        print("[SUCCESS] All checks passed! You are ready to run tests.")
        print("\nRun: pytest tests/test_onboarding.py -v")
    else:
        print("[WARNING] Some checks failed. Please fix the issues above.")
        print("\nInstall missing libraries:")
        print("  pip install -r requirements.txt")
        print("\nInstall Appium globally:")
        print("  npm install -g appium")
        print("  appium driver install uiautomator2")


if __name__ == "__main__":
    main()
