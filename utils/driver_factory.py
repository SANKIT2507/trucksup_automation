"""
TrucksUp Automation - Driver Factory
=====================================
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import Config


class DriverFactory:
    """Appium driver create karo"""

    @staticmethod
    def get_driver():
        """Fresh driver instance return karo"""
        options = UiAutomator2Options()
        options.platform_name = Config.PLATFORM_NAME
        options.platform_version = Config.PLATFORM_VERSION
        options.device_name = Config.DEVICE_NAME
        options.app_package = Config.APP_PACKAGE
        options.app_activity = Config.APP_ACTIVITY
        options.automation_name = "UiAutomator2"

        # IMPORTANT: no_reset=True rakho taaki app data clear na ho
        # (Kuch phones pe pm clear permission nahi hoti)
        # Agar fresh install chahiye toh pehle manually uninstall karo
        options.no_reset = True

        # Unicode keyboard
        options.unicode_keyboard = True
        options.reset_keyboard = True

        driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        return driver
