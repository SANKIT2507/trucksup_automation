"""
TrucksUp Automation - XML Capture Helper
==========================================
Har screen ka XML capture karne ke liye helper script.

Kaise use karein:
1. Appium server start karo: appium
2. Is script ko run karo: python xml_capture.py
3. Phone par manually app navigate karo
4. Press Enter jab bhi new screen par pahunchein
5. XML files automatically save hongi
"""

import os
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import Config


def get_driver():
    """Driver create karo"""
    options = UiAutomator2Options()
    options.platform_name = Config.PLATFORM_NAME
    options.platform_version = Config.PLATFORM_VERSION
    options.device_name = Config.DEVICE_NAME
    options.app_package = Config.APP_PACKAGE
    options.app_activity = Config.APP_ACTIVITY
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    return driver


def capture_screen(driver, screen_name):
    """Screen ka XML capture karo"""
    os.makedirs("xml_screenshots", exist_ok=True)

    # XML save karo
    xml_path = f"xml_screenshots/{screen_name}.xml"
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"[SAVED] XML: {xml_path}")

    # Screenshot bhi lo
    screenshot_path = f"xml_screenshots/{screen_name}.png"
    driver.save_screenshot(screenshot_path)
    print(f"[SAVED] Screenshot: {screenshot_path}")


def main():
    print("=" * 60)
    print("TRUCKSUP XML CAPTURE HELPER")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Appium server should be running")
    print("2. Phone mein app navigate karo manually")
    print("3. Jab new screen aaye, yahan Enter press karo")
    print("4. XML + Screenshot automatically save hoga")
    print("5. Type 'exit' to quit")
    print("=" * 60)

    print("\nCreating driver...")
    driver = get_driver()
    print("[OK] Driver connected!")

    screen_count = 0

    while True:
        print("\n" + "-" * 60)
        user_input = input("Enter screen name (or 'exit' to quit): ").strip()

        if user_input.lower() == 'exit':
            break

        if not user_input:
            screen_count += 1
            user_input = f"screen_{screen_count}"

        print(f"Capturing: {user_input}")
        capture_screen(driver, user_input)
        print("[DONE] Capture complete!")

    driver.quit()
    print("\n[EXIT] Driver closed. XML files saved in xml_screenshots/ folder")


if __name__ == "__main__":
    main()
