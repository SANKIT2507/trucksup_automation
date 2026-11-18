"""
OTP handoff: test chalte waqt OTP 'otp.txt' (project root) mein likh do,
test use padh kar khud bhar deta hai. File ek baar padhne ke baad hat jaati hai.
"""

import os

from config import Config

OTP_FILE = os.path.join(Config.BASE_DIR, "otp.txt")


def read_otp_file():
    try:
        with open(OTP_FILE, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        return ""
    # PowerShell 'echo > file' UTF-16 likhta hai, cmd/bash UTF-8 - dono sambhalo
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-8-sig", errors="ignore")
    otp = "".join(ch for ch in text if ch.isdigit())
    remove_otp_file()
    return otp


def remove_otp_file():
    try:
        os.remove(OTP_FILE)
    except FileNotFoundError:
        pass
