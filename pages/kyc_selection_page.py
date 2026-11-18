from pages.base_page import BasePage
from locators import KycSelectionLocators
from utils.logger import get_logger
from selenium.common.exceptions import TimeoutException


class KycSelectionPage(BasePage):
    """
    Screen: KYC Verification
    3 options mein se koi ek select karna hai:
    Aadhaar Card / PAN Card / Driving License
    """

    OPTIONS = {
        "aadhaar": KycSelectionLocators.AADHAAR_CARD,
        "pan": KycSelectionLocators.PAN_CARD,
        "dl": KycSelectionLocators.DRIVING_LICENSE,
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger()

    def is_kyc_selection_screen_visible(self):
        """Check karo KYC Verification screen khuli hai ya nahi"""
        try:
            self.find_element(KycSelectionLocators.SCREEN_TITLE)
            self.logger.info("KYC selection screen is visible")
            return True
        except TimeoutException:
            self.logger.warning("KYC selection screen NOT visible")
            return False

    def select_kyc_option(self, option="aadhaar"):
        """option: 'aadhaar' ya 'pan' ya 'dl'"""
        if option not in self.OPTIONS:
            raise ValueError(f"option 'aadhaar', 'pan' ya 'dl' hona chahiye, mila: {option}")

        self.logger.info(f"Selecting KYC option: {option}")
        self.click(self.OPTIONS[option])
        self.logger.info(f"KYC option '{option}' selected")

    def click_proceed(self):
        """Proceed button dabao"""
        self.logger.info("Clicking Proceed button")
        self.click(KycSelectionLocators.PROCEED_BUTTON)
        self.logger.info("Proceed button clicked")

    def select_kyc_option_and_proceed(self, option="aadhaar"):
        """KYC option select karo aur Proceed dabao, tabhi next page khulega"""
        self.select_kyc_option(option)
        self.click_proceed()