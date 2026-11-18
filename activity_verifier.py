"""
TrucksUp Automation - Activity Verifier
========================================
Yeh script aapko correct app activity name batayega.

Kaise use karein:
1. Phone mein TrucksUp app open karo
2. Is script ko run karo: python activity_verifier.py
3. Jo output aaye woh config.py mein daalo
"""

import subprocess
import sys


def get_current_activity():
    """Current app activity nikaalo"""
    try:
        result = subprocess.run(
            "adb shell dumpsys window | findstr "mCurrentFocus"",
            shell=True, capture_output=True, text=True
        )
        output = result.stdout.strip()

        if output:
            print("=" * 60)
            print("CURRENT ACTIVITY FOUND:")
            print("=" * 60)
            print(output)
            print()

            # Extract activity name
            if "mCurrentFocus" in output:
                parts = output.split()
                for part in parts:
                    if "/" in part:
                        activity = part.strip("}"")
                        print(f"Full Activity: {activity}")

                        # Extract just the activity part after /
                        if "/" in activity:
                            pkg, act = activity.split("/", 1)
                            print(f"Package: {pkg}")
                            print(f"Activity: {act}")
                            print()
                            print("=" * 60)
                            print("CONFIG.PY MEIN DAALO:")
                            print("=" * 60)
                            print(f'APP_PACKAGE = "{pkg}"')
                            print(f'APP_ACTIVITY = "{act}"')
                            print("=" * 60)
                        return
        else:
            print("[ERROR] Kuch output nahi aaya. Kya app open hai?")
            print("Phone mein TrucksUp app open karo aur dobara try karo.")

    except Exception as e:
        print(f"[ERROR] {e}")
        print("Kya adb installed hai? 'adb devices' run karke check karo.")


def get_all_activities():
    """Saare activities nikaalo"""
    try:
        result = subprocess.run(
            "adb shell dumpsys package com.logistics.trucksup | findstr "Activity"",
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            print("\nAll Activities found:")
            print(result.stdout)
    except:
        pass


if __name__ == "__main__":
    print("TrucksUp Activity Verifier")
    print("=" * 60)
    print("Make sure TrucksUp app is OPEN on your phone!")
    print("=" * 60)
    print()

    get_current_activity()
