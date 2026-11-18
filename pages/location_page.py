"""
TrucksUp Automation - Location Page
====================================
Screen 4: Location Permission Handler.
"""

import time
from pages.base_page import BasePage
from locators import LocationPageLocators
from utils.logger import get_logger

logger = get_logger()


class LocationPage(BasePage):
    """Location permission screen"""

    def is_location_popup_visible(self):
        """Check karo app ka location popup aaya hai"""
        return self.is_element_visible(LocationPageLocators.LOCATION_POPUP_TITLE, timeout=3)

    def click_proceed(self):
        """App ke popup mein Proceed button click karo"""
        # Popup sirf pehli baar aata hai (permission already granted ho to skip)
        if self.click_if_visible(LocationPageLocators.PROCEED_BUTTON, timeout=10):
            logger.info("Proceed button clicked for location")
        else:
            logger.info("Location popup nahi aaya - skipping")

    def allow_location_while_using(self):
        """Android system dialog mein 'Allow while using app' select karo"""
        if self.click_if_visible(LocationPageLocators.ALLOW_WHILE_USING, timeout=3):
            logger.info("Location permission: Allow while using app")
        else:
            logger.info("System permission dialog nahi aaya (already granted)")

    def allow_location_once(self):
        """Android system dialog mein 'Only this time' select karo"""
        try:
            self.click(LocationPageLocators.ALLOW_ONCE)
            logger.info("Location permission: Allow only this time")
        except:
            logger.warning("Allow once button not found")

    def deny_location(self):
        """Location permission deny karo"""
        try:
            self.click(LocationPageLocators.DENY)
            logger.info("Location permission: Denied")
        except:
            logger.warning("Deny button not found")

    def handle_location_flow(self):
        """Complete location flow handle karo"""
        self.click_proceed()
        self.allow_location_while_using()
