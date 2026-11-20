"""
TrucksUp Automation - Registration (DigiLocker ke baad)
========================================================
Screen 7: Business details  -> Next
Screen 8: Vehicle details + preferred lane -> Submit
Screen 9: "Vehicle Details Saved" + Welcome -> Home (auto)
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy

from config import Config
from locators import BaRegistrationLocators as BA, RegistrationLocators as R, VehicleDetailsLocators as V, OnboardingSuccessLocators as S
from pages.base_page import BasePage
from utils.logger import get_logger


class RegistrationPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger()

    # ─── Screen 7: Business details ───

    def is_registration_screen_visible(self, timeout=20):
        visible = self.is_element_visible(R.STREET_VILLAGE_INPUT, timeout=timeout)
        self.logger.info(f"Registration (business details) screen visible: {visible}")
        return visible

    def fill_business_details(self, street_village=None):
        """Name/address/pincode/city/state DigiLocker se pre-filled aate hain"""
        street_village = street_village or Config.TEST_STREET_VILLAGE

        box = self.find_element(R.SAME_AS_PROFILE_NAME_CHECKBOX)
        if box.get_attribute("checked") != "true":
            box.click()
        self.logger.info(f"Business name = profile name: {self.get_text(R.BUSINESS_NAME_INPUT)}")

        self.send_keys(R.STREET_VILLAGE_INPUT, street_village)
        self.hide_keyboard()

    def click_next(self):
        self.click(R.NEXT_BUTTON)
        self.logger.info("Registration Next clicked")

    # ─── Screen 8: Vehicle details ───

    def _trucks(self):
        return [t.text for t in self.driver.find_elements(*V.ADDED_TRUCKS)]

    def _lanes(self):
        froms = [t.text for t in self.driver.find_elements(*V.ADDED_LANES)]
        tos = [t.text for t in self.driver.find_elements(*V.ADDED_LANES_TO)]
        return list(zip(froms, tos))

    def add_vehicle(self, vehicle_number=None, timeout=30):
        """Vehicle number daalo -> + dabao -> server verify -> chip list mein aana chahiye"""
        vehicle_number = (vehicle_number or Config.TEST_VEHICLE_NUMBER).upper().replace(" ", "")
        if vehicle_number in self._trucks():
            self.logger.info(f"Vehicle {vehicle_number} pehle se added hai")
            return

        self.logger.info(f"Adding vehicle: {vehicle_number}")
        self.send_keys(V.VEHICLE_NUMBER_INPUT, vehicle_number)
        self.click(V.ADD_VEHICLE_BUTTON)

        def done(d):
            if vehicle_number in self._trucks():
                return "added"
            errs = d.find_elements(*V.VEHICLE_ERROR)
            if errs and errs[0].text:
                return "error:" + errs[0].text
            return False

        result = WebDriverWait(self.driver, timeout).until(done)
        assert result == "added", f"Vehicle {vehicle_number} add nahi hua - app ne bola: {result[6:]}"
        self.logger.info(f"Vehicle added: {self._trucks()}")

    def _pick_city(self, field, suggestions_id, city):
        self.send_keys(field, city)
        option = (AppiumBy.XPATH,
                  f'//*[@resource-id="{suggestions_id}"]//*[@text="{city.upper()}"]')
        self.click(option)

    def add_preferred_lane(self, from_city=None, to_city=None, timeout=15):
        """From/To city search -> exact suggestion select -> + (lane add)"""
        from_city = from_city or Config.TEST_LANE_FROM
        to_city = to_city or Config.TEST_LANE_TO
        want = (from_city.upper(), to_city.upper())
        if want in self._lanes():
            self.logger.info(f"Lane {from_city} -> {to_city} pehle se added hai")
            return

        self.logger.info(f"Adding preferred lane: {from_city} -> {to_city}")
        self._pick_city(V.FROM_INPUT, V.FROM_SUGGESTIONS_ID, from_city)
        self._pick_city(V.TO_INPUT, V.TO_SUGGESTIONS_ID, to_city)
        self.hide_keyboard()

        for attempt in (1, 2):
            self.click(V.ADD_LANE_BUTTON)
            try:
                WebDriverWait(self.driver, timeout).until(lambda d: want in self._lanes())
                self.logger.info(f"Lane added: {self._lanes()}")
                return
            except TimeoutException:
                self.logger.warning(f"Lane add attempt {attempt} - list mein nahi dikhi")
        raise AssertionError(f"Preferred lane {from_city} -> {to_city} add nahi hui")

    def submit_vehicle_details(self, vehicle_number=None, from_city=None, to_city=None):
        self.find_element(V.VEHICLE_NUMBER_INPUT)
        self.logger.info(f"Vehicle Details (start): trucks={self._trucks()}, lanes={self._lanes()}")

        self.add_vehicle(vehicle_number)
        self.add_preferred_lane(from_city, to_city)

        self.click(V.SUBMIT_BUTTON)
        self.logger.info("Vehicle details Submit clicked")

    # ─── Business Associate: details form ───

    def is_ba_registration_screen_visible(self, timeout=20):
        visible = self.is_element_visible(BA.SECTION_TITLE, timeout=timeout)
        self.logger.info(f"Business Associate details screen visible: {visible}")
        return visible

    def fill_ba_details_and_submit(self, firm_name=None, address=None, pincode=None, street_village=None):
        """Firm name, address, pincode (city/state auto), street -> Submit"""
        firm_name = firm_name or Config.BA_FIRM_NAME
        address = address or Config.BA_ADDRESS
        pincode = pincode or Config.BA_PINCODE
        street_village = street_village or Config.TEST_STREET_VILLAGE

        self.send_keys(BA.FIRM_NAME_INPUT, firm_name)
        self.send_keys(BA.ADDRESS_INPUT, address)
        self.send_keys(BA.PINCODE_INPUT, pincode)
        self.hide_keyboard()
        # Pincode se City/State khud bharte hain
        WebDriverWait(self.driver, 15).until(
            lambda d: (d.find_element(*BA.CITY).text or "City").rstrip(" *") not in ("", "City")
        )
        self.logger.info(f"Pincode {pincode} -> {self.get_text(BA.CITY)}, {self.get_text(BA.STATE)}")

        self.send_keys(BA.STREET_VILLAGE_INPUT, street_village)
        self.hide_keyboard()
        self.click(BA.SUBMIT_BUTTON)
        self.logger.info("Business Associate details Submit clicked")

    # ─── Screen 9: Success ───

    def wait_for_onboarding_success(self, timeout=90, retry_submit=False):
        """
        Submit ke baad success/Home ka wait. Test server ka trucksupplier/create
        20-30s+ leta hai, aur kabhi response ke baad bhi form par hi ruk jaata hai.
        retry_submit=True: timeout par Submit dobara dabao aur ek baar aur wait karo.
        """
        def done(d):
            act = d.current_activity or ""
            return "OnBoardingSucessActivity" in act or "MainActivity" in act

        try:
            WebDriverWait(self.driver, timeout, poll_frequency=2).until(done)
        except TimeoutException:
            if not (retry_submit and self.is_element_visible(V.SUBMIT_BUTTON, timeout=2)):
                raise
            self.logger.warning(f"{timeout}s mein aage nahi badha - Submit dobara dabaya")
            self.click(V.SUBMIT_BUTTON)
            WebDriverWait(self.driver, timeout, poll_frequency=2).until(done)
        self.logger.info(f"Onboarding success: {self.driver.current_activity}")
