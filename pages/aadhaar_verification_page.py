"""
TrucksUp Automation - Profile Verification (Aadhaar via DigiLocker)
====================================================================
Flow:
  1. App screen "Profile Verification": Aadhaar number -> Continue to DigiLocker
  2. DigiLocker WebView: Other ID -> Aadhaar -> number -> OTP se login -> Sign In
  3. USER manually OTP daalta hai (aur Sign In dabata hai - ya automation dabayegi)
  4. Consent screen: Aadhaar Card tick -> Allow
  5. App wapas Registration screen pe aata hai
"""

import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy

from config import Config
from locators import AadhaarVerificationLocators as AV, DigiLockerLocators as DL
from pages.base_page import BasePage
from utils.logger import get_logger


from utils.otp_handoff import OTP_FILE, read_otp_file as _read_otp_file, remove_otp_file as _remove_otp_file


class AadhaarVerificationPage(BasePage):
    """Screen 6: Profile Verification + DigiLocker"""

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger()

    # ─── App screen ───

    def is_aadhaar_screen_visible(self, timeout=15):
        visible = self.is_element_visible(AV.AADHAAR_INPUT, timeout=timeout)
        self.logger.info(f"Profile Verification (Aadhaar) screen visible: {visible}")
        return visible

    def enter_aadhaar_number(self, aadhaar_number):
        self.logger.info(f"Entering Aadhaar number: XXXXXXXX{aadhaar_number[-4:]}")
        self.send_keys(AV.AADHAAR_INPUT, aadhaar_number, log_text=False)
        self.hide_keyboard()

    def click_continue_to_digilocker(self):
        self.click(AV.CONTINUE_DIGILOCKER_BUTTON)
        self.logger.info("Continue to DigiLocker clicked")

    # ─── DigiLocker sign in ───

    def _scroll_to_web_id(self, rid):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().resourceId("{rid}"))',
        )

    def _dismiss_autofill_popup(self):
        """Android ka saved-password popup input ko dhak deta hai"""
        if self.is_element_visible(DL.AUTOFILL_POPUP, timeout=2):
            self.driver.back()
            self.logger.info("Autofill popup dismissed")
            time.sleep(1)

    def _tick(self, rid):
        """
        WebView checkbox ka 'checked' attribute bharosemand nahi hai (ticked par bhi
        'false' deta hai), isliye fresh page par bas ek baar tap karte hain.
        """
        box = self._scroll_to_web_id(rid)
        time.sleep(0.5)  # scroll settle
        box.click()
        time.sleep(1)    # layout shift (PIN field hide) settle
        self.logger.info(f"Checkbox tapped: {rid}")

    def sign_in_digilocker_with_aadhaar(self, aadhaar_number):
        """Other ID tab -> Aadhaar -> number -> OTP mode -> terms -> Sign In"""
        self.logger.info("DigiLocker sign-in page...")
        WebDriverWait(self.driver, 40).until(EC.element_to_be_clickable(DL.OTHER_ID_TAB)).click()
        self.click(DL.ID_TYPE_DROPDOWN)
        self.click(DL.AADHAAR_OPTION)

        field = self.find_element(DL.ID_NUMBER_INPUT)
        field.click()
        field.send_keys(aadhaar_number)
        self.hide_keyboard()
        self._dismiss_autofill_popup()

        # Terms PEHLE: PIN-less tick karne se PIN field chhupta hai aur page upar
        # khisakta hai - baad mein terms tap karne par galat jagah lagta tha.
        self._tick(DL.TERMS_CHECKBOX_ID)
        self._tick(DL.PIN_LESS_CHECKBOX_ID)   # PIN nahi, OTP se login

        for attempt in (1, 2):
            self.click(DL.SIGN_IN_BUTTON)
            self.logger.info(f"DigiLocker Sign In clicked (attempt {attempt})")
            if self.is_element_visible(DL.OTP_INPUT, timeout=20):
                self.logger.info("DigiLocker OTP page khuli - OTP bheja gaya")
                return
            # Abhi bhi sign-in page par -> terms box tick nahi hua tha
            self.logger.warning("OTP page nahi khuli - terms checkbox dobara tap karke retry")
            self._tick(DL.TERMS_CHECKBOX_ID)
        raise AssertionError("DigiLocker Sign In ke baad OTP page nahi khuli")

    def wait_for_manual_otp(self, timeout_seconds=180):
        """
        USER OTP daalega. Hum consent screen aane tak wait karte hain.
        Agar user ne 6 digit daal diye par Sign In nahi dabaya, toh hum dabayenge.
        """
        WebDriverWait(self.driver, 40).until(EC.visibility_of_element_located(DL.OTP_INPUT))
        self.logger.info("=" * 60)
        self.logger.info("⏸️  DigiLocker OTP aapke Aadhaar-linked mobile par gaya hai")
        self.logger.info(f"📱 App mein OTP daalo (max {timeout_seconds}s wait)")
        self.logger.info("=" * 60)

        self.logger.info(f"   (Ya OTP ko '{OTP_FILE}' file mein likh do - test khud bhar dega)")
        _remove_otp_file()

        end = time.time() + timeout_seconds
        clicked = False
        while time.time() < end:
            if self.is_element_visible(DL.ALLOW_BUTTON, timeout=1):
                self.logger.info("⏯️  OTP verified - consent screen aa gayi")
                return
            self.dismiss_truecaller_popup(timeout=1)  # DigiLocker OTP SMS popup
            otp_from_file = _read_otp_file()
            if otp_from_file:
                self.logger.info("OTP file se mila - enter kar rahe hain")
                self.send_keys(DL.OTP_INPUT, otp_from_file, log_text=False)
                self.driver.find_element(*DL.OTP_SIGN_IN_BUTTON).click()
                clicked = True
                continue
            if not clicked:
                try:
                    otp = self.driver.find_element(*DL.OTP_INPUT).get_attribute("text") or ""
                    if len(otp) == 6 and otp.isdigit():
                        self.driver.find_element(*DL.OTP_SIGN_IN_BUTTON).click()
                        clicked = True
                        self.logger.info("OTP filled - Sign In clicked")
                except NoSuchElementException:
                    pass
            time.sleep(2)
        raise TimeoutException(f"{timeout_seconds}s mein OTP verify nahi hua")

    # ─── Consent ───

    def allow_consent(self):
        """Aadhaar Card tick karo aur Allow dabao"""
        aadhaar_box = (AppiumBy.XPATH, "//*[contains(@text,'Aadhaar Card')]/following::android.widget.CheckBox[1]")
        self.click(aadhaar_box)
        self.click(DL.ALLOW_BUTTON)
        self.logger.info("Consent: Aadhaar Card -> Allow clicked")

        # Agar DigiLocker ne "select one or more options" bola, toh retry
        if self.is_element_visible(DL.ALLOW_BUTTON, timeout=4) and \
                "select one or more" in self.driver.page_source:
            self.logger.warning("Aadhaar tick register nahi hua - retry")
            self.click(aadhaar_box)
            self.click(DL.ALLOW_BUTTON)

    def wait_until_back_in_app(self, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            lambda d: "DgVerifyWebView" not in (d.current_activity or "")
        )
        self.logger.info(f"DigiLocker done - app screen: {self.driver.current_activity}")

    # ─── Full flow ───

    def complete_aadhaar_verification(self, aadhaar_number=None, otp_timeout=300):
        aadhaar_number = aadhaar_number or Config.TEST_AADHAAR_NUMBER
        self.logger.info("=" * 60)
        self.logger.info("🆔 Starting Aadhaar Verification via DigiLocker...")
        self.enter_aadhaar_number(aadhaar_number)
        self.click_continue_to_digilocker()
        self.sign_in_digilocker_with_aadhaar(aadhaar_number)
        self.wait_for_manual_otp(otp_timeout)
        self.allow_consent()
        self.wait_until_back_in_app()
        self.logger.info("✅ Aadhaar verification via DigiLocker complete!")
        self.logger.info("=" * 60)
