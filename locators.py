"""
TrucksUp Automation - Element Locators
========================================
"""

from appium.webdriver.common.appiumby import AppiumBy


# ==========================================
# SCREEN 1: Google Phone Hint Popup
# ==========================================
class WelcomePageLocators:
    """App Launch / Google Phone Hint"""
    GOOGLE_PHONE_HINT_TITLE = (AppiumBy.ID, "com.google.android.gms:id/title")
    GOOGLE_POPUP_CLOSE = (AppiumBy.ID, "com.google.android.gms:id/cancel")
    SUGGESTED_PHONE_NUMBER = (AppiumBy.ID, "com.google.android.gms:id/phone_number")
    PHONE_NUMBER_LIST_ITEM = (AppiumBy.ID, "com.google.android.gms:id/phone_number_list_item")


# ==========================================
# ==========================================
# SCREEN 2: Mobile Number Input (LOGIN)
# EXACT IDs from XML — UPDATED ✅
# ==========================================
class LoginPageLocators:
    """Mobile Number Input Screen"""

    # Mobile number input field
    # resource-id="com.logistics.trucksup:id/phone"
    # hint="Please enter mobile number"
    # max-text-length="10"
    MOBILE_INPUT_FIELD = (AppiumBy.ID, "com.logistics.trucksup:id/phone")

    # Verify button container (CardView)
    VERIFY_BUTTON_CARD = (AppiumBy.ID, "com.logistics.trucksup:id/sendOtpCard")

    # Verify button clickable area (RelativeLayout)
    VERIFY_BUTTON_CLICKABLE = (AppiumBy.ID, "com.logistics.trucksup:id/subBut")

    # Verify button text
    VERIFY_BUTTON_TEXT = (AppiumBy.ID, "com.logistics.trucksup:id/sub")

    # Verify button (best locator — clickable TextView with text "Verify")
    VERIFY_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/sub")

    # Country code (+91)
    COUNTRY_CODE = (AppiumBy.XPATH, "//android.widget.TextView[@text='+91 ']")

    # Terms & Privacy — ek hi TextView mein hain
    # resource-id="com.logistics.trucksup:id/privecy"
    # text-has-clickable-span="true"
    TERMS_PRIVACY_TEXTVIEW = (AppiumBy.ID, "com.logistics.trucksup:id/privecy")


# ==========================================
# SCREEN 3: OTP Verification
# EXACT IDs from XML — WORKING ✅
# ==========================================
class OTPPageLocators:
    """OTP Verification Screen"""

    OTP_MESSAGE = (AppiumBy.ID, "com.logistics.trucksup:id/otpMsg")
    OTP_PHONE_DISPLAY = (AppiumBy.ID, "com.logistics.trucksup:id/otpPhoneMsg")
    CHANGE_NUMBER_LINK = (AppiumBy.ID, "com.logistics.trucksup:id/otpPhoneChange")

    # Single EditText input (NOT 4 boxes)
    OTP_INPUT_FIELD = (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='com.logistics.trucksup:id/otpTextView']/android.widget.EditText")

    TIMER_TEXT = (AppiumBy.ID, "com.logistics.trucksup:id/timecounter")
    RESEND_LINK = (AppiumBy.ID, "com.logistics.trucksup:id/resentOtp")
    LOGIN_BUTTON_CARD = (AppiumBy.ID, "com.logistics.trucksup:id/verifyOtpCard")
    LOGIN_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/clickOtp")
    LOGIN_BUTTON_TEXT = (AppiumBy.ID, "com.logistics.trucksup:id/otpSub")


# ==========================================
# SCREEN 4: Location Permission
# TODO: Location screen ka XML chahiye
# ==========================================
class LocationPageLocators:
    """Location Permission Screen"""
    LOCATION_POPUP_TITLE = (AppiumBy.XPATH, "//*[contains(@text, 'location')]")
    # Bottom sheet "We need your location... Kindly click Proceed"
    PROCEED_BUTTON = (AppiumBy.XPATH, '//*[@resource-id="com.logistics.trucksup:id/ok" and @text="Proceed"]')
    ALLOW_WHILE_USING = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
    ALLOW_ONCE = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button")
    DENY = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button")


# ==========================================
from appium.webdriver.common.appiumby import AppiumBy


class ProfileSetupLocators:

    # Profile Photo
    PROFILE_IMAGE = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/profileImage"
    )

    EDIT_PHOTO = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/getImage"
    )

    CAMERA_OPTION = (
        AppiumBy.XPATH,
        "//*[contains(@text,'Camera')]"
    )

    # Camera Permission
    ALLOW_WHILE_USING_APP = (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
    )

    # Camera
    CAMERA_CAPTURE = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/cameraBtn"
    )

    # Name
    FULL_NAME_INPUT = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/name"
    )

    # Referral Code
    REFERRAL_CODE_INPUT = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/refral"
    )

    # Profile Type
    TRUCK_SUPPLIER = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/owner"
    )

    BUSINESS_ASSOCIATE = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/broker"
    )

    TRUCKSHUB = (
        AppiumBy.ID,
        "com.logistics.trucksup:id/buyerSellor"
    )


class BusinessDocsLocators:
    """Business Associate: 'Business document' screen (activity: BaDocsActivity)"""
    # Business proof - koi ek type
    GSTIN = (AppiumBy.ID, "com.logistics.trucksup:id/btnGst")
    TRADE_LICENSE = (AppiumBy.ID, "com.logistics.trucksup:id/btnTrade")
    UDYAM_AADHAAR = (AppiumBy.ID, "com.logistics.trucksup:id/btnAadhaar")
    BILTY = (AppiumBy.ID, "com.logistics.trucksup:id/btnLorry")
    UPLOAD_BUSINESS_PROOF = (AppiumBy.ID, "com.logistics.trucksup:id/btnUploadBusinessProof")

    # Shop / establishment proof - koi ek type
    SIGNAGE_BOARD = (AppiumBy.ID, "com.logistics.trucksup:id/btnSign")
    VISITING_CARD = (AppiumBy.ID, "com.logistics.trucksup:id/btnVisit")
    UPLOAD_SHOP_PROOF = (AppiumBy.ID, "com.logistics.trucksup:id/btnUploadShopProof")

    # Upload bottom sheet: Camera / Gallery
    SOURCE_CAMERA = (AppiumBy.ID, "com.logistics.trucksup:id/btnCamera")
    CAMERA_CAPTURE = (AppiumBy.ID, "com.logistics.trucksup:id/cameraBtn")

    NEXT_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/btnNext")


class KycSelectionLocators:
    """KYC Verification screen: 3 options, koi ek select karna hai"""
    PROCEED_BUTTON = (AppiumBy.XPATH, '//android.widget.TextView[@text="Proceed"]')
    AADHAAR_CARD = (AppiumBy.XPATH, '//android.widget.TextView[@text="Aadhaar Card" or @text="Aadhar Card" or @text="Aadhaar card"]')
    PAN_CARD = (AppiumBy.XPATH, '//android.widget.TextView[@text="PAN Card"]')
    DRIVING_LICENSE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Driving License"]')
    SCREEN_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="KYC Verification"]')


class AadhaarVerificationLocators:
    """Screen 6: Profile Verification (Aadhaar -> Continue to DigiLocker)"""

    PAGE_TITLE = (AppiumBy.XPATH, '//*[@resource-id="com.logistics.trucksup:id/appBarTitle" and @text="Profile Verification"]')
    AADHAAR_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/dg_etAadhaarNumber")
    PAN_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/etPanno")
    CONTINUE_DIGILOCKER_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/digiLockerBtn")
    BACK_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/btnBack")
    HELP_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/customerHelpLine")


def _web(rid):
    """DigiLocker WebView elements: HTML id native tree mein resource-id ban jaata hai"""
    return (AppiumBy.XPATH, f'//*[@resource-id="{rid}"]')


class DigiLockerLocators:
    """DigiLocker sign-in WebView (activity: .DGLocker.DgVerifyWebView)"""

    # Sign in page -> "Other ID" tab
    OTHER_ID_TAB = _web("otherbtn")
    ID_TYPE_DROPDOWN = _web("dropdownmenu")
    AADHAAR_OPTION = (AppiumBy.XPATH, '//android.widget.CheckedTextView[@text="Aadhaar"]')
    ID_NUMBER_INPUT = _web("validateinput")
    PIN_LESS_CHECKBOX_ID = "others_pin_less_auth"   # tick = PIN ki jagah OTP se login
    TERMS_CHECKBOX_ID = "terms3"
    SIGN_IN_BUTTON = _web("submitbtn3")

    # Android autofill popup (saved passwords) jo input ko dhak deta hai
    AUTOFILL_POPUP = (AppiumBy.ID, "android:id/autofill_dataset_list")

    # OTP page
    OTP_FORM = _web("frm_otp")
    OTP_INPUT = _web("otp")
    OTP_SIGN_IN_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@text="Sign In"]')

    # Consent page
    CONSENT_FORM = _web("consent_form")
    ALLOW_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@text="Allow"]')


class RegistrationLocators:
    """Screen 7: Registration - Business details (activity: TSRegistrationActivity)"""
    PAGE_TITLE = (AppiumBy.XPATH, '//*[@text="Registration"]')
    SAME_AS_PROFILE_NAME_CHECKBOX = (AppiumBy.ID, "com.logistics.trucksup:id/checkBoxBusiness")
    BUSINESS_NAME_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/registrationBusinessName")
    STREET_VILLAGE_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/autoCompleteTextView")
    NEXT_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/registrationNextButton")


class BaRegistrationLocators:
    """Business Associate: 'BUSINESS ASSOCIATE DETAILS' (activity: RagisterdScreen) - kuch pre-filled nahi"""
    SECTION_TITLE = (AppiumBy.XPATH, '//*[@text="BUSINESS ASSOCIATE DETAILS"]')
    FIRM_NAME_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/name")
    ADDRESS_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/address")
    PINCODE_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/pinCode")
    STREET_VILLAGE_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/spinnerSubCity")
    CITY = (AppiumBy.ID, "com.logistics.trucksup:id/city")      # pincode se auto-fill
    STATE = (AppiumBy.ID, "com.logistics.trucksup:id/state")    # pincode se auto-fill
    SUBMIT_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/registrationNextButton")


class VehicleDetailsLocators:
    """Screen 8: Registration - Vehicle details + preferred lane (activity: TruckRegistrationActivity)"""
    VEHICLE_NUMBER_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/etTruckNumber")
    ADD_VEHICLE_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/btnAddTruck")  # number type karne par dikhta hai
    VEHICLE_ERROR = (AppiumBy.ID, "com.logistics.trucksup:id/errorMessage")      # e.g. "verification attempt failed"
    ADDED_TRUCKS = (AppiumBy.ID, "com.logistics.trucksup:id/tvTruck")

    FROM_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/etFrom")
    TO_INPUT = (AppiumBy.ID, "com.logistics.trucksup:id/etTo")
    FROM_SUGGESTIONS_ID = "com.logistics.trucksup:id/rvFromSuggestions"
    TO_SUGGESTIONS_ID = "com.logistics.trucksup:id/rvToSuggestions"
    ADD_LANE_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/btnAddLane")
    ADDED_LANES = (AppiumBy.ID, "com.logistics.trucksup:id/tvFromCity")
    ADDED_LANES_TO = (AppiumBy.ID, "com.logistics.trucksup:id/tvToCity")

    SUBMIT_BUTTON = (AppiumBy.ID, "com.logistics.trucksup:id/submitTSProfileData")


class OnboardingSuccessLocators:
    """Screen 9: 'Vehicle Details Saved' + Welcome (activity: OnBoardingSucessActivity)"""
    SAVED_MESSAGE = (AppiumBy.ID, "com.logistics.trucksup:id/msg1")
    WELCOME_NAME = (AppiumBy.ID, "com.logistics.trucksup:id/tvName")



# ==========================================
# HOME SCREEN
# ==========================================
class HomePageLocators:
    """Home Screen"""
    # Bottom bar ka Home tab (MainActivity). Purana "id/image" ab exist nahi karta.
    HOME_IMAGE = (AppiumBy.ID, "com.logistics.trucksup:id/home")
    PROMO_POPUP_CLOSE = (AppiumBy.ID, "com.logistics.trucksup:id/removeImag")
    # Android 13+ system dialog: "Allow TrucksUp to send you notifications?" (fresh data par)
    NOTIFICATION_ALLOW = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")


class TrucksHubHomeLocators:
    """TrucksHub profile ka landing page (activity: activities.sellor.TrucksHub)"""
    GREETING = (AppiumBy.ID, "com.logistics.trucksup:id/nameMassage")   # "Hey, <NAME>!"
    BUY_USED_TRUCKS = (AppiumBy.XPATH, '//*[@resource-id="com.logistics.trucksup:id/title" and @text="Buy Used Trucks"]')

