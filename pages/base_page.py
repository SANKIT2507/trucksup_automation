"""
TrucksUp Automation - Base Page
================================
Har page class isse inherit karegi.
Common actions: click, type, wait, screenshot, etc.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from utils.logger import get_logger
from selenium.common.exceptions import TimeoutException

logger = get_logger()


class BasePage:
    """Base class for all pages"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_element(self, locator):
        """Element ko wait karke find karo"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        """Multiple elements find karo"""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        """Element par click karo"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked on element: {locator}")

    def send_keys(self, locator, text, log_text=True):
        """Text type karo (log_text=False: sensitive data log mein mat likho)"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        shown = text if log_text else "****"
        logger.info(f"Typed '{shown}' in element: {locator}")

    def is_element_visible(self, locator, timeout=5):
        """Check karo element visible hai ya nahi"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def get_text(self, locator):
        """Element ka text return karo"""
        return self.find_element(locator).text

    def is_enabled(self, locator):
        """Check karo button enabled hai ya nahi"""
        return self.find_element(locator).is_enabled()

    def hide_keyboard(self):
        """Keyboard hide karo"""
        try:
            self.driver.hide_keyboard()
        except:
            pass

    def swipe_up(self):
        """Screen ko upar swipe karo"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def take_screenshot(self, name):
        """Screenshot lo"""
        import os
        os.makedirs("screenshots", exist_ok=True)
        path = f"screenshots/{name}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved: {path}")

    def wait_for_element_to_disappear(self, locator):
        """Jab tak element disappear nahi hota, wait karo"""
        self.wait.until(EC.invisibility_of_element_located(locator))

    # Truecaller ka SMS/OTP popup screen ke upar aa kar elements dhak deta hai.
    # Yeh alag window hai - Appium ko dikhane ke liye enableMultiWindows chahiye.
    TRUECALLER_CLOSE = (AppiumBy.ID, "com.truecaller:id/closeBtn")

    def dismiss_truecaller_popup(self, timeout=2):
        """Truecaller overlay dikhe to X dabao (OTP SMS aane par aata hai)"""
        self.driver.update_settings({"enableMultiWindows": True})
        try:
            if self.click_if_visible(self.TRUECALLER_CLOSE, timeout=timeout):
                logger.info("Truecaller popup closed")
                return True
            return False
        finally:
            self.driver.update_settings({"enableMultiWindows": False})

    def click_if_visible(self, locator, timeout=3):
        """
        Agar element visible ho to click karo,
        nahi ho to quietly skip karo.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"Clicked optional element: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Optional element not found: {locator}")
            return False
