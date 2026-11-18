"""
OTP handoff: test chalte waqt OTP 'otp.txt' (project root) mein likh do,
test use padh kar khud bhar deta hai. File ek baar padhne ke baad hat jaati hai.
"""

import os

from config import Config

OTP_FILE = os.path.join(Config.BASE_DIR, "otp.txt")


def read_otp_file():
    try:
        with open(OTP_FILE, encoding="utf-8") as f:
            otp = f.read().strip()
    except FileNotFoundError:
        return ""
    remove_otp_file()
    return otp if otp.isdigit() else ""


def remove_otp_file():
    try:
        os.remove(OTP_FILE)
    except FileNotFoundError:
        pass
