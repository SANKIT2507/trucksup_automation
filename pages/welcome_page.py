"""
TrucksUp Automation - Welcome Page
===================================
Screen 1: Google Phone Hint Popup handle karne wala page
"""

import time
from pages.base_page import BasePage
from locators import WelcomePageLocators
from utils.logger import get_logger

logger = get_logger()


class WelcomePage(BasePage):
    """App launch hone par aane wala welcome screen"""

    def is_google_phone_hint_visible(self, timeout=10):
        """Check karo Google phone hint popup aaya hai ya nahi
        
        Note: Popup thodi der mein appear hota hai, isliye thoda wait karo
        """
        logger.info("Waiting for Google phone hint popup...")

        # Pehle 2 second wait karo taaki popup render ho
        time.sleep(2)

        visible = self.is_element_visible(WelcomePageLocators.GOOGLE_PHONE_HINT_TITLE, timeout=timeout)
        if visible:
            logger.info("[DETECTED] Google phone hint popup is visible")
        else:
            logger.info("[NOT FOUND] Google phone hint popup not detected")
        return visible

    def dismiss_google_popup(self):
        """Google popup ko close karo (Cancel/X button click karke)"""
        try:
            self.click(WelcomePageLocators.GOOGLE_POPUP_CLOSE)
            logger.info("[ACTION] Google phone hint popup dismissed via Cancel button")
            # Dismiss hone ke baad wait karo
            time.sleep(2)
        except Exception as e:
            logger.warning(f"[WARNING] Could not dismiss popup via Cancel: {e}")
            # Agar Cancel se nahi hua toh back button try karo
            try:
                self.driver.back()
                logger.info("[ACTION] Pressed back button to dismiss popup")
                time.sleep(2)
            except:
                pass

    def select_suggested_number(self):
        """Suggested phone number select karo"""
        try:
            self.click(WelcomePageLocators.PHONE_NUMBER_LIST_ITEM)
            logger.info("[ACTION] Suggested phone number selected from popup")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"[WARNING] Could not select suggested number: {e}")
