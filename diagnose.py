"""
TrucksUp Automation - Diagnostic Tool
=====================================
Yeh script check karega:
1. Kya app installed hai?
2. Kya app open ho rahi hai?
3. Current screen kya hai?
4. Screenshot lo
"""

import subprocess
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import Config


def check_app_installed():
    """Check karo app installed hai ya nahi"""
    print("\n" + "=" * 60)
    print("CHECK 1: Is App Installed?")
    print("=" * 60)

    cmd = f'adb shell pm list packages | findstr "{Config.APP_PACKAGE}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if Config.APP_PACKAGE in result.stdout:
        print(f"[PASS] App is installed: {Config.APP_PACKAGE}")
        return True
    else:
        print(f"[FAIL] App NOT installed: {Config.APP_PACKAGE}")
        print("Please install the app first!")
        return False


def get_current_activity():
    """Current activity nikaalo"""
    print("\n" + "=" * 60)
    print("CHECK 2: Current Activity")
    print("=" * 60)

    cmd = 'adb shell dumpsys window | findstr "mCurrentFocus"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    return result.stdout


def launch_app_and_diagnose():
    """App launch karo aur diagnose karo"""
    print("\n" + "=" * 60)
    print("CHECK 3: Launching App via Appium")
    print("=" * 60)

    try:
        options = UiAutomator2Options()
        options.platform_name = Config.PLATFORM_NAME
        options.platform_version = Config.PLATFORM_VERSION
        options.device_name = Config.DEVICE_NAME
        options.app_package = Config.APP_PACKAGE
        options.app_activity = Config.APP_ACTIVITY
        options.automation_name = "UiAutomator2"
        options.no_reset = True
        options.unicode_keyboard = True
        options.reset_keyboard = True

        print("Creating driver...")
        driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
        print("[PASS] Driver created successfully!")
        print(f"Session ID: {driver.session_id}")

        # Wait for app to load
        print("Waiting 10 seconds for app to load...")
        time.sleep(10)

        # Take screenshot
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = "screenshots/diagnostic_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"[INFO] Screenshot saved: {screenshot_path}")

        # Get current activity
        print("\nGetting current activity...")
        current = get_current_activity()

        # Try to get page source
        print("\nGetting page source (XML)...")
        try:
            source = driver.page_source
            # Save to file for inspection
            with open("screenshots/page_source.xml", "w", encoding="utf-8") as f:
                f.write(source)
            print("[INFO] Page source saved to: screenshots/page_source.xml")
        except Exception as e:
            print(f"[WARNING] Could not get page source: {e}")

        # Check if mobile input is present
        print("\nChecking for mobile input field...")
        try:
            from appium.webdriver.common.appiumby import AppiumBy
            elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            print(f"[INFO] Found {len(elements)} EditText fields")

            for i, el in enumerate(elements):
                print(f"  EditText {i}: text='{el.text}', resource-id='{el.get_attribute('resource-id')}'")
        except Exception as e:
            print(f"[WARNING] Could not find EditText: {e}")

        driver.quit()
        print("\n[PASS] Diagnostic complete!")

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        print("\nPossible reasons:")
        print("1. Appium server not running")
        print("2. Wrong activity name")
        print("3. App not installed")
        print("4. Device not connected")


def main():
    print("=" * 60)
    print("TRUCKSUP AUTOMATION - DIAGNOSTIC TOOL")
    print("=" * 60)

    # Check device
    print("\nChecking device connection...")
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    print(result.stdout)

    if Config.DEVICE_NAME == "your_device_name":
        print("\n[WARNING] DEVICE_NAME not updated in config.py!")
        print("Please update DEVICE_NAME with your actual device name.")
        return

    if not check_app_installed():
        return

    launch_app_and_diagnose()

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Check screenshot: screenshots/diagnostic_screenshot.png")
    print("2. Check page source: screenshots/page_source.xml")
    print("3. If app didn't open, verify APP_ACTIVITY in config.py")
    print("4. Run: python activity_verifier.py to get correct activity")


if __name__ == "__main__":
    main()
