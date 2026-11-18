"""
TrucksUp Automation - OTP Page
===============================
Screen 3: OTP Verification Screen.
NOTE: OTP is a SINGLE EditText input, NOT 4 separate boxes!
"""

import time

from pages.base_page import BasePage
from utils.otp_handoff import read_otp_file, remove_otp_file
from locators import OTPPageLocators
from utils.logger import get_logger

logger = get_logger()


class OTPPage(BasePage):
    """OTP enter karne wala screen"""

    def enter_otp(self, otp_code):
        """OTP enter karo - Single EditText input mein"""
        logger.info(f"Entering OTP: {otp_code}")
        self.send_keys(OTPPageLocators.OTP_INPUT_FIELD, otp_code)
        self.hide_keyboard()
        logger.info(f"OTP entered successfully: {otp_code}")

    def login_with_otp(self, otp_code=None, timeout_seconds=300):
        """
        OTP pata ho to bhar ke Log In dabao.
        Nahi pata (khaali) to user ka wait karo: phone par daale ya otp.txt mein likhe.
        """
        if otp_code:
            self.enter_otp(otp_code)
            self.click_login()
            return

        remove_otp_file()
        logger.info("=" * 60)
        logger.info("⏸️  Login OTP .env mein nahi hai - phone par daalo ya otp.txt mein likho")
        logger.info(f"   (max {timeout_seconds}s wait)")
        logger.info("=" * 60)
        end = time.time() + timeout_seconds
        while time.time() < end:
            otp = read_otp_file()
            if otp:
                self.enter_otp(otp)
                self.click_login()
                return
            if not self.is_element_visible(OTPPageLocators.LOGIN_BUTTON, timeout=1):
                logger.info("OTP screen chali gayi - user ne login kar liya")
                return
            time.sleep(2)
        raise TimeoutError(f"{timeout_seconds}s mein login OTP nahi aaya")

    def click_login(self):
        """Log In button click karo"""
        self.click(OTPPageLocators.LOGIN_BUTTON)
        logger.info("Log In button clicked")

    def click_change_number(self):
        """Change number link click karo"""
        self.click(OTPPageLocators.CHANGE_NUMBER_LINK)
        logger.info("Change number clicked")

    def click_resend_otp(self):
        """Resend OTP link click karo"""
        timer_text = self.get_text(OTPPageLocators.TIMER_TEXT)
        if "00:00" in timer_text or "0:00" in timer_text:
            self.click(OTPPageLocators.RESEND_LINK)
            logger.info("Resend OTP clicked")
        else:
            logger.warning(f"Timer still running: {timer_text}. Please wait.")

    def is_otp_screen_visible(self):
        """Check karo OTP screen aaya hai ya nahi"""
        return self.is_element_visible(OTPPageLocators.LOGIN_BUTTON, timeout=5)

    def get_displayed_phone_number(self):
        """OTP screen par displayed phone number return karo"""
        return self.get_text(OTPPageLocators.OTP_PHONE_DISPLAY)

    def get_timer_text(self):
        """Timer text return karo"""
        return self.get_text(OTPPageLocators.TIMER_TEXT)
