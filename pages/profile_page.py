from pages.base_page import BasePage
from locators import ProfileSetupLocators
from utils.logger import get_logger
from config import Config
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProfilePage(BasePage):
    """
    Screen 5: Profile Setup / Personal Details
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger()

    def is_profile_screen_visible(self, timeout=10):
        """Check if profile setup screen is loaded"""
        try:
            self.find_element(ProfileSetupLocators.FULL_NAME_INPUT)
            self.logger.info("Profile setup screen is visible")
            return True
        except TimeoutException:
            self.logger.warning("Profile setup screen NOT visible")
            return False

    # ─── Photo Upload Flow ───

    def click_edit_photo_icon(self):
        """Click the pencil icon on profile photo"""
        self.logger.info("Clicking edit photo icon...")
        self.dismiss_truecaller_popup(timeout=5)  # login OTP SMS ka popup icon dhak deta hai
        self.click(ProfileSetupLocators.EDIT_PHOTO)
        self.logger.info("Edit photo icon clicked")

    def _select_camera_if_dialog_appears(self):
        """
        Agar EDIT_PHOTO click karne ke baad Camera/Gallery dialog aata hai,
        toh 'Camera' option select karo.
        Agar directly camera open hota hai, toh skip karo.
        """
        self.logger.info("Checking if Camera/Gallery dialog appeared...")
        try:
            # Short wait (3 sec) — agar dialog aaya toh click karo
            camera_option = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(ProfileSetupLocators.CAMERA_OPTION)
            )
            camera_option.click()
            self.logger.info("Camera option selected from dialog")
        except TimeoutException:
            self.logger.info("No dialog appeared — camera should open directly")

    def handle_camera_permission(self):
        """Handle camera permission popup (only first launch)"""
        self.logger.info("Checking for camera permission popup...")
        try:
            self.click(ProfileSetupLocators.ALLOW_WHILE_USING_APP)
            self.logger.info("Camera permission allowed (While using the app)")
        except (TimeoutException, NoSuchElementException):
            self.logger.info("Camera permission popup not present (already granted)")

    def capture_photo(self):
        """Click camera capture button"""
        self.logger.info("Clicking camera capture button...")
        self.click(ProfileSetupLocators.CAMERA_CAPTURE)
        self.logger.info("Photo captured")

    def _wait_for_photo_upload(self, timeout=15):
        """
        Camera se wapas profile screen pe aane ka wait karo.
        Photo upload hone mein 2-5 sec lag sakte hain.
        """
        self.logger.info("Waiting for photo to upload and return to profile screen...")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(ProfileSetupLocators.PROFILE_IMAGE)
            )
            self.logger.info("Returned to profile screen after photo upload")
        except TimeoutException:
            self.logger.warning("Timeout waiting for profile screen — proceeding anyway")

    def upload_profile_photo(self):
        """
        Complete photo upload flow:
        1. Click pencil icon
        2. Select Camera from dialog (if appears)
        3. Handle permission (if first time)
        4. Click capture
        5. Wait to return to profile screen
        """
        self.logger.info("=" * 40)
        self.logger.info("📸 Starting Profile Photo Upload...")

        # Step 1: Click edit icon
        self.click_edit_photo_icon()

        # Step 2: Handle dialog if appears
        self._select_camera_if_dialog_appears()

        # Step 3: Handle permission
        self.handle_camera_permission()

        # Step 4: Small wait for camera to be ready
        self.logger.info("Waiting for camera to be ready...")
        import time
        time.sleep(2)

        # Step 5: Capture photo
        self.capture_photo()

        # Step 6: Wait for upload to complete and return to profile
        self._wait_for_photo_upload()

        self.logger.info("✅ Profile photo uploaded successfully!")
        self.logger.info("=" * 40)

    # ─── Form Fields ───

    def enter_full_name(self, name=None):
        """Enter full name"""
        if name is None:
            name = Config.TEST_FULL_NAME

        self.logger.info(f"Entering full name: {name}")
        self.send_keys(ProfileSetupLocators.FULL_NAME_INPUT, name)
        self.hide_keyboard()
        self.logger.info("Full name entered")

    def enter_sales_code(self, sales_code=None):
        """Enter sales/referral code (optional)"""
        if sales_code is None:
            sales_code = Config.TEST_REFERRAL_CODE

        if not sales_code:
            self.logger.info("Sales code is empty, skipping...")
            return

        self.logger.info(f"Entering sales code: {sales_code}")
        try:
            self.send_keys(ProfileSetupLocators.REFERRAL_CODE_INPUT, sales_code)
            self.hide_keyboard()
            self.logger.info("Sales code entered")
        except (TimeoutException, NoSuchElementException):
            self.logger.warning("Sales code field not found, skipping...")

    # ─── Profile Type Selection ───

    def select_profile_type(self, profile_type=None):
        """Select profile type — app auto-navigates after this"""
        if profile_type is None:
            profile_type = Config.SELECT_PROFILE_TYPE

        self.logger.info(f"Selecting profile type: {profile_type}")

        profile_types = {
            "Truck Supplier": ProfileSetupLocators.TRUCK_SUPPLIER,
            "Business Associate": ProfileSetupLocators.BUSINESS_ASSOCIATE,
            "TrucksHub": ProfileSetupLocators.TRUCKSHUB
        }

        if profile_type not in profile_types:
            raise ValueError(
                f"Invalid profile type: {profile_type}. "
                f"Choose from: {list(profile_types.keys())}"
            )

        self.click(profile_types[profile_type])
        self.logger.info(f"Profile type '{profile_type}' selected")

    # ─── Main Orchestrator ───

    def fill_profile_details(self, name=None, profile_type=None, sales_code=None, upload_photo=True):
        """
        Complete profile setup:
        1. Upload photo (if upload_photo=True)
        2. Enter full name
        3. Enter sales code (optional)
        4. Select profile type → auto-navigates
        """
        self.logger.info("=" * 50)
        self.logger.info("🚀 Starting Profile Setup...")

        # Step 1: Photo Upload
        if upload_photo:
            self.upload_profile_photo()
        else:
            self.logger.info("Photo upload skipped (upload_photo=False)")

        # Step 2: Enter full name
        self.enter_full_name(name)

        # Step 3: Enter sales code (optional)
        self.enter_sales_code(sales_code)

        # Step 4: Select profile type → App auto-navigates
        self.select_profile_type(profile_type)

        self.logger.info("✅ Profile setup completed!")
        self.logger.info("=" * 50)