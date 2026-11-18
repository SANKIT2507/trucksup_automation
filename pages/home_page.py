"""
TrucksUp Automation - Home Page
================================
Home Screen validation.
"""

from pages.base_page import BasePage
from locators import HomePageLocators, TrucksHubHomeLocators
from utils.logger import get_logger

logger = get_logger()


class HomePage(BasePage):
    """Home screen"""

    def dismiss_promo_popup(self, timeout=15):
        """
        Home par aane wale popups band karo (agar aaye):
        1. Android notification permission dialog -> Allow
        2. TrucksUp promo banner -> X
        """
        if self.click_if_visible(HomePageLocators.NOTIFICATION_ALLOW, timeout=timeout):
            logger.info("Notification permission: Allow")
        self.click_if_visible(HomePageLocators.PROMO_POPUP_CLOSE, timeout=timeout)

    def is_truckshub_home_visible(self, timeout=30):
        """TrucksHub user ka landing page: greeting + 'Buy Used Trucks' card"""
        if not self.is_element_visible(TrucksHubHomeLocators.GREETING, timeout=timeout):
            return False
        greeting = self.get_text(TrucksHubHomeLocators.GREETING)
        has_features = self.is_element_visible(TrucksHubHomeLocators.BUY_USED_TRUCKS, timeout=5)
        logger.info(f"TrucksHub home: '{greeting}', features visible: {has_features}")
        return has_features

    def is_home_screen_visible(self, timeout=30):
        """Check karo home screen aayi hai"""
        visible = self.is_element_visible(HomePageLocators.HOME_IMAGE, timeout=timeout)
        if visible:
            logger.info("Home screen is visible - Login successful!")
        return visible

    def get_home_element(self):
        """Home element return karo"""
        return self.find_element(HomePageLocators.HOME_IMAGE)
