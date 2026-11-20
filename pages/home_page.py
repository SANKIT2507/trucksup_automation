"""
TrucksUp Automation - Home Page
================================
Home Screen validation.
"""

from appium.webdriver.common.appiumby import AppiumBy

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

    def logout_if_logged_in(self, timeout=5):
        """
        Agar app pehle se logged in hai (Home khula hai), toh hamburger menu ->
        Logout -> Yes. Test phir login screen se shuru hota hai.
        Returns True agar logout kiya.
        """
        # "Do you want to logout?" dialog pehle se khula ho toh seedha Yes
        if self.click_if_visible(HomePageLocators.LOGOUT_CONFIRM_YES, timeout=2):
            logger.info("Logout dialog pehle se khula tha - Yes clicked")
            return True
        if not self.is_element_visible(HomePageLocators.MENU_BUTTON, timeout=timeout):
            return False
        logger.info("App pehle se logged in hai - hamburger menu se Logout kar rahe hain")
        self.dismiss_promo_popup(timeout=3)
        self.click(HomePageLocators.MENU_BUTTON)
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().resourceId("{HomePageLocators.LOGOUT_ID}"))',
        ).click()
        self.click(HomePageLocators.LOGOUT_CONFIRM_YES)
        logger.info("Logout: Yes clicked")
        return True
