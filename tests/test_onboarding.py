"""
TrucksUp Automation - Onboarding Tests
=======================================
New user aur existing user ke liye test cases.
"""

import pytest
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

from pages.welcome_page import WelcomePage
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.location_page import LocationPage
from pages.profile_page import ProfilePage
from pages.aadhaar_verification_page import AadhaarVerificationPage
from pages.kyc_selection_page import KycSelectionPage
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.business_docs_page import BusinessDocsPage
from utils.logger import get_logger

logger = get_logger()


# ─── Shared steps (Truck Supplier aur Business Associate dono ke liye) ───

def login_and_fill_profile(driver, mobile_number, otp, profile_type):
    """STEP 1-5: popup -> mobile -> OTP -> location -> profile (photo, naam, profile type)"""
    logger.info("[INIT] Waiting for app to fully launch...")
    time.sleep(5)
    if HomePage(driver).logout_if_logged_in():
        time.sleep(3)

    logger.info("[STEP 1] Checking for Google Phone Hint Popup...")
    welcome_page = WelcomePage(driver)
    if welcome_page.is_google_phone_hint_visible(timeout=10):
        welcome_page.dismiss_google_popup()
    time.sleep(3)

    logger.info("[STEP 2] Mobile Number Screen...")
    login_page = LoginPage(driver)
    login_page.enter_mobile_number(mobile_number)
    entered = login_page.get_entered_number()
    assert len(entered) == 10, f"Mobile number 10 digit nahi hai! Entered: {entered}"
    login_page.click_verify()
    time.sleep(3)

    logger.info("[STEP 3] OTP Verification Screen...")
    otp_page = OTPPage(driver)
    assert otp_page.is_otp_screen_visible(), "OTP screen nahi aaya!"
    otp_page.login_with_otp(otp)
    time.sleep(3)

    logger.info("[STEP 4] Location Permission...")
    LocationPage(driver).handle_location_flow()
    time.sleep(2)

    logger.info(f"[STEP 5] Personal Details Screen ({profile_type})...")
    profile_page = ProfilePage(driver)
    assert profile_page.is_profile_screen_visible(), "Profile setup screen nahi aaya!"
    profile_page.fill_profile_details(
        name=Config.TEST_FULL_NAME,
        profile_type=profile_type,
        sales_code="",  # Referral abhi skip
        upload_photo=True,
    )


def verify_aadhaar_via_digilocker(driver, aadhaar_number):
    """STEP 6: KYC -> Aadhaar -> DigiLocker (OTP user deta hai) -> consent"""
    logger.info("[STEP 6] Aadhaar Verification (KYC + DigiLocker)...")
    kyc_select = KycSelectionPage(driver)
    assert kyc_select.is_kyc_selection_screen_visible(), "KYC selection screen nahi khuli"
    kyc_select.select_kyc_option_and_proceed("aadhaar")

    aadhaar_page = AadhaarVerificationPage(driver)
    assert aadhaar_page.is_aadhaar_screen_visible(), "Aadhaar screen nahi aayi!"
    aadhaar_page.complete_aadhaar_verification(
        aadhaar_number=aadhaar_number,
        otp_timeout=300,  # DigiLocker OTP: phone par daalo ya otp.txt mein likho
    )


def land_on_home(driver, screenshot_name):
    """Last step: popups band karo aur Home check karo"""
    logger.info("[HOME] Home Screen Validation...")
    home_page = HomePage(driver)
    home_page.dismiss_promo_popup()
    assert home_page.is_home_screen_visible(), "Home screen nahi aayi!"
    logger.info("✅ Home screen visible — Onboarding COMPLETE!")
    driver.save_screenshot(f"screenshots/{screenshot_name}.png")


class TestTrucksUpOnboarding:
    """TrucksUp app ka complete new user onboarding flow"""

    def test_new_user_onboarding(self, driver, aadhaar_number):
        """Truck Supplier: new user onboarding, login se Home tak"""
        logger.info("=" * 60)
        logger.info("TRUCKSUP ONBOARDING TEST - TRUCK SUPPLIER")
        logger.info("=" * 60)

        login_and_fill_profile(driver, Config.TEST_MOBILE_NUMBER, Config.TEST_OTP, "Truck Supplier")
        verify_aadhaar_via_digilocker(driver, aadhaar_number)

        # STEP 7: Registration - business details
        logger.info("[STEP 7] Registration Screen...")
        registration = RegistrationPage(driver)
        assert registration.is_registration_screen_visible(), "DigiLocker ke baad Registration screen nahi aayi!"
        registration.fill_business_details(street_village=Config.TEST_STREET_VILLAGE)
        registration.click_next()

        # STEP 8: Vehicle + preferred lane -> Submit
        logger.info("[STEP 8] Vehicle Details...")
        registration.submit_vehicle_details()
        registration.wait_for_onboarding_success(retry_submit=True)

        # STEP 9: Home
        land_on_home(driver, "onboarding_complete")

    def test_business_associate_onboarding(self, driver, aadhaar_number):
        """Business Associate: new user onboarding, login se Home tak"""
        assert Config.BA_MOBILE_NUMBER, "BA_MOBILE_NUMBER .env mein set nahi hai"
        logger.info("=" * 60)
        logger.info("TRUCKSUP ONBOARDING TEST - BUSINESS ASSOCIATE")
        logger.info("=" * 60)

        login_and_fill_profile(driver, Config.BA_MOBILE_NUMBER, Config.BA_OTP, "Business Associate")

        # STEP 5b: Business document (sirf Business Associate) - dono proofs camera se
        logger.info("[STEP 5b] Business document...")
        docs = BusinessDocsPage(driver)
        assert docs.is_business_docs_screen_visible(), "Business document screen nahi aayi!"
        docs.complete_business_documents(business_proof="gstin", shop_proof="signage")

        verify_aadhaar_via_digilocker(driver, aadhaar_number)

        # STEP 7: Business Associate details (firm, address, pincode, street) -> Submit
        logger.info("[STEP 7] Business Associate details...")
        registration = RegistrationPage(driver)
        assert registration.is_ba_registration_screen_visible(), "DigiLocker ke baad BA details screen nahi aayi!"
        registration.fill_ba_details_and_submit()
        registration.wait_for_onboarding_success()

        # STEP 8: Home
        land_on_home(driver, "ba_onboarding_complete")

    def test_truckshub_onboarding(self, driver, aadhaar_number):
        """TrucksHub: new user onboarding, login se Home tak"""
        assert Config.TH_MOBILE_NUMBER, "TH_MOBILE_NUMBER .env mein set nahi hai"
        logger.info("=" * 60)
        logger.info("TRUCKSUP ONBOARDING TEST - TRUCKSHUB")
        logger.info("=" * 60)

        login_and_fill_profile(driver, Config.TH_MOBILE_NUMBER, Config.TH_OTP, "TrucksHub")

        # STEP 6: TrucksHub ka koi KYC/registration nahi - profile ke baad seedha
        # TrucksHub landing page (notification permission popup pehle aata hai)
        logger.info("[STEP 6] TrucksHub landing page...")
        home_page = HomePage(driver)
        home_page.dismiss_promo_popup(timeout=10)
        assert home_page.is_truckshub_home_visible(), "TrucksHub landing page nahi aayi!"
        logger.info("✅ TrucksHub landing page visible — Onboarding COMPLETE!")
        driver.save_screenshot("screenshots/th_onboarding_complete.png")

    @pytest.mark.skip(reason="Temporarily disabled - re-enable when existing-user flow is needed")
    def test_existing_user_login(self, driver):
        """Existing user login flow (OTP based)"""

        logger.info("\n" + "=" * 60)
        logger.info("TRUCKSUP EXISTING USER LOGIN TEST")
        logger.info("=" * 60)

        # Wait for app to launch
        logger.info("[INIT] Waiting for app to fully launch...")
        time.sleep(5)

        welcome_page = WelcomePage(driver)
        if welcome_page.is_google_phone_hint_visible(timeout=10):
            logger.info("[FOUND] Google popup detected! Dismissing...")
            welcome_page.dismiss_google_popup()

        time.sleep(3)

        login_page = LoginPage(driver)
        login_page.enter_mobile_number(Config.TEST_MOBILE_NUMBER)
        login_page.click_verify()

        time.sleep(3)

        otp_page = OTPPage(driver)
        otp_page.enter_otp(Config.TEST_OTP)
        otp_page.click_login()

        time.sleep(5)

        # Home screen validation
        home_page = HomePage(driver)
        assert home_page.is_home_screen_visible(), "Home screen nahi aayi!"
        logger.info("Home screen visible - Login successful!")

        driver.save_screenshot("screenshots/existing_user_login.png")
