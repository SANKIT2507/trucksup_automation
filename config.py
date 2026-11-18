"""
TrucksUp Automation - Configuration
=====================================
Saari device details aur test data .env file se aati hai.
Setup: .env.example ko .env mein copy karo aur values bharo.
"""
import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _env(key, default=None, required=False):
    value = os.getenv(key, default)
    if required and not value:
        raise RuntimeError(f"'{key}' .env file mein set nahi hai! (.env.example dekho)")
    return value


class Config:
    """Central configuration class"""

    # DEVICE DETAILS
    PLATFORM_NAME = "Android"
    PLATFORM_VERSION = _env("PLATFORM_VERSION", "15")
    DEVICE_NAME = _env("DEVICE_NAME", required=True)

    # APPIUM SERVER
    APPIUM_SERVER_URL = _env("APPIUM_SERVER_URL", "http://localhost:4723")

    # APP DETAILS
    APP_PACKAGE = "com.logistics.trucksup"
    APP_ACTIVITY = ".activities.WLcomeScreen"

    # HOME SCREEN VALIDATION
    HOME_ELEMENT_ID = "com.logistics.trucksup:id/image"

    # TEST DATA (.env se)
    TEST_MOBILE_NUMBER = _env("TEST_MOBILE_NUMBER", required=True)
    TEST_OTP = _env("TEST_OTP", required=True)
    TEST_FULL_NAME = _env("TEST_FULL_NAME", "Test User")

    # Business Associate test ka alag (naya) account. OTP khaali = test wait karega
    BA_MOBILE_NUMBER = _env("BA_MOBILE_NUMBER", "")
    BA_OTP = _env("BA_OTP", "")
    BA_FIRM_NAME = _env("BA_FIRM_NAME", "Test Firm")
    BA_ADDRESS = _env("BA_ADDRESS", "Main Road, Pilkhuwa")
    BA_PINCODE = _env("BA_PINCODE", "245304")

    # TrucksHub test ka alag (naya) account. OTP khaali = test wait karega
    TH_MOBILE_NUMBER = _env("TH_MOBILE_NUMBER", "")
    TH_OTP = _env("TH_OTP", "")
    TEST_REFERRAL_CODE = _env("TEST_REFERRAL_CODE", "")
    SELECT_PROFILE_TYPE = _env("SELECT_PROFILE_TYPE", "Truck Supplier")
    TEST_STREET_VILLAGE = _env("TEST_STREET_VILLAGE", "Pilkhuwa")
    TEST_VEHICLE_NUMBER = _env("TEST_VEHICLE_NUMBER", "NL01AA6244")
    TEST_LANE_FROM = _env("TEST_LANE_FROM", "Delhi")
    TEST_LANE_TO = _env("TEST_LANE_TO", "Mumbai")

    # Aadhaar Verification Data
    TEST_AADHAAR_NUMBER = _env("TEST_AADHAAR_NUMBER", "")

    # TIMEOUTS
    IMPLICIT_WAIT = 15
    EXPLICIT_WAIT = 25

    # PATHS
    BASE_DIR = BASE_DIR
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
