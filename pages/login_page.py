"""
TrucksUp Automation - Login Page
=================================
Screen 2: Mobile Number Input aur Verify button.
"""

from pages.base_page import BasePage
from locators import LoginPageLocators
from utils.logger import get_logger

logger = get_logger()


class LoginPage(BasePage):
    """Mobile number enter karne wala screen"""

    def enter_mobile_number(self, mobile_number):
        """Mobile number type karo"""
        logger.info(f"Entering mobile number: {mobile_number}")
        self.send_keys(LoginPageLocators.MOBILE_INPUT_FIELD, mobile_number)
        self.hide_keyboard()

    def is_verify_button_enabled(self):
        """Check karo Verify button enabled hai ya nahi"""
        try:
            enabled = self.is_enabled(LoginPageLocators.VERIFY_BUTTON)
            logger.info(f"Verify button enabled: {enabled}")
            return enabled
        except:
            logger.warning("Verify button not found!")
            return False

    def click_verify(self):
        """Verify button click karo"""
        try:
            self.click(LoginPageLocators.VERIFY_BUTTON)
            logger.info("Verify button clicked successfully")
        except Exception as e:
            logger.error(f"Verify button click failed: {e}")
            raise

    def get_entered_number(self):
        """Jo number enter hua hai woh return karo"""
        try:
            element = self.find_element(LoginPageLocators.MOBILE_INPUT_FIELD)
            text = element.get_attribute("text") or ""
            # Hint text ko filter karo
            if "Please enter" in text:
                return ""
            return text
        except:
            return ""

    def click_terms_and_conditions(self):
        """Terms & Conditions link par click karo"""
        logger.info("Clicking Terms & Conditions link...")
        try:
            element = self.find_element(LoginPageLocators.TERMS_PRIVACY_TEXTVIEW)
            element.click()
            logger.info("Clicked on Terms/Privacy TextView")
        except Exception as e:
            logger.warning(f"Direct click failed: {e}")

    def click_privacy_policy(self):
        """Privacy Policy link par click karo"""
        logger.info("Clicking Privacy Policy link...")
        try:
            element = self.find_element(LoginPageLocators.TERMS_PRIVACY_TEXTVIEW)
            element.click()
            logger.info("Clicked on Terms/Privacy TextView")
        except Exception as e:
            logger.warning(f"Direct click failed: {e}")