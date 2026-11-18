# TrucksUp Onboarding Automation

End-to-end tests for new-user onboarding in the **TrucksUp** Android app (`com.logistics.trucksup`), written with Appium (UiAutomator2), Selenium and pytest using the Page Object Model.

One test per profile type, each running from the login screen to the user's landing page:

| Test | Profile type | Journey |
|---|---|---|
| `test_new_user_onboarding` | Truck Supplier | Login → location → profile → KYC via DigiLocker → registration → vehicle and preferred lane → Home |
| `test_business_associate_onboarding` | Business Associate | Login → location → profile → business documents → KYC via DigiLocker → firm details → Home |
| `test_truckshub_onboarding` | TrucksHub | Login → location → profile → TrucksHub landing page |
| `test_existing_user_login` | (any) | Skipped for now |

## Requirements

- Windows, macOS or Linux with **Python 3.10+** (developed on 3.13)
- **Node.js** and **Appium 2** with the **UiAutomator2** driver (developed on Appium 2.17.1, uiautomator2 2.45.1)
- **Android SDK platform-tools** (`adb`) and **Java JDK**, with `ANDROID_HOME` and `JAVA_HOME` set
- A real Android phone with **USB debugging** on and the TrucksUp app installed

## Setup

1. **Install Appium and the Android driver**

   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```

2. **Clone the repo and install Python packages**

   ```bash
   git clone https://github.com/SANKIT2507/trucksup_automation.git
   cd trucksup_automation
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   # source .venv/bin/activate     # macOS / Linux
   pip install -r requirements.txt
   ```

3. **Connect the phone** and copy its device id:

   ```bash
   adb devices
   ```

4. **Create your `.env`** from the template and fill it in:

   ```bash
   copy .env.example .env          # Windows
   # cp .env.example .env          # macOS / Linux
   ```

   `.env` holds phone numbers, OTPs and your Aadhaar number. It is in `.gitignore`; never commit it. See [Settings](#settings) for each value.

5. **Check the setup** (optional):

   ```bash
   python setup_check.py
   ```

## Running the tests

1. **Start Appium** in its own terminal and leave it running:

   ```bash
   appium
   ```

2. **Reset the app before every new-user run.** On the phone: Settings → Apps → TrucksUp → Storage → **Clear data**. Each test starts from the login screen, so the app must be logged out. (Some phones block `adb shell pm clear`; on those, enable Developer options → *Disable permission monitoring*, or clear it by hand.)

3. **Run a test:**

   ```bash
   # Truck Supplier
   pytest "tests/test_onboarding.py::TestTrucksUpOnboarding::test_new_user_onboarding" -v --html=reports/truck_supplier.html --self-contained-html

   # Business Associate
   pytest "tests/test_onboarding.py::TestTrucksUpOnboarding::test_business_associate_onboarding" -v --html=reports/business_associate.html --self-contained-html

   # TrucksHub
   pytest "tests/test_onboarding.py::TestTrucksUpOnboarding::test_truckshub_onboarding" -v --html=reports/truckshub.html --self-contained-html
   ```

   Run one test at a time; they share one phone and each needs the app reset first.

4. **Answer the prompts.** At the start the test asks for the Aadhaar number (press Enter to use `TEST_AADHAAR_NUMBER`). Truck Supplier and Business Associate then pause at the **DigiLocker OTP**, which goes to the Aadhaar-linked mobile. Enter it within 5 minutes in either way:
   - type it in the app on the phone (the test taps Sign In once 6 digits are in), or
   - write it to `otp.txt` in the project folder; the test reads it, enters it and deletes the file:

     ```bash
     echo 123456 > otp.txt
     ```

   If `BA_OTP` or `TH_OTP` is empty, the login OTP works the same way.

### Accounts

Each new-user test needs a mobile number that has **not finished onboarding yet**. After a successful run the number is registered with that profile type, and logging in with it goes straight to Home. Use a new number (or have the account reset on the server) for the next run.

### Results

- **HTML report:** the file passed to `--html`, under `reports/`
- **Failure screenshot:** `screenshots/fail_<test name>.png`, saved automatically
- **Success screenshots:** `screenshots/onboarding_complete.png`, `ba_onboarding_complete.png`, `th_onboarding_complete.png`

`reports/` and `screenshots/` are ignored by git.

## Settings

All values are read from `.env` by `config.py`.

| Key | Used by | Meaning |
|---|---|---|
| `DEVICE_NAME` | all | Device id from `adb devices` (required) |
| `PLATFORM_VERSION` | all | Android version of the phone |
| `APPIUM_SERVER_URL` | all | Default `http://localhost:4723` |
| `TEST_FULL_NAME` | all | Name entered on the profile screen |
| `TEST_AADHAAR_NUMBER` | Truck Supplier, Business Associate | 12-digit Aadhaar for DigiLocker |
| `TEST_STREET_VILLAGE` | Truck Supplier, Business Associate | Street/village on the registration form |
| `TEST_MOBILE_NUMBER`, `TEST_OTP` | Truck Supplier | Login number and OTP (required) |
| `TEST_VEHICLE_NUMBER` | Truck Supplier | Vehicle to add; must pass the app's server verification |
| `TEST_LANE_FROM`, `TEST_LANE_TO` | Truck Supplier | Preferred lane cities, picked from the app's suggestions |
| `BA_MOBILE_NUMBER`, `BA_OTP` | Business Associate | Login number and OTP; empty OTP waits for manual entry |
| `BA_FIRM_NAME`, `BA_ADDRESS`, `BA_PINCODE` | Business Associate | Firm details form; city and state fill in from the pincode |
| `TH_MOBILE_NUMBER`, `TH_OTP` | TrucksHub | Login number and OTP; empty OTP waits for manual entry |

## Project layout

```
config.py              Settings loaded from .env
conftest.py            Driver fixture, Aadhaar prompt, failure screenshots
locators.py            All element locators, one class per screen
pages/                 Page objects (one per screen)
  base_page.py           Shared actions: click, type, waits, Truecaller popup
  login_page.py, otp_page.py, location_page.py, profile_page.py
  business_docs_page.py  Business Associate document upload
  kyc_selection_page.py, aadhaar_verification_page.py   KYC + DigiLocker
  registration_page.py   Registration, vehicle/lane, Business Associate details
  home_page.py           Home and TrucksHub landing checks, popups
tests/test_onboarding.py   The tests and shared step helpers
utils/                 Driver factory, logger, OTP handoff (otp.txt)
diagnose.py, activity_verifier.py, xml_capture.py, setup_check.py   Helper scripts
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Test fails at step 2 (mobile number field not found) | The app is still logged in. Clear the app data and run again. |
| `Activity class ... does not exist` | `APP_ACTIVITY` in `config.py` must not include the package name. Open the app on the phone and run `python activity_verifier.py` to see the current activity. |
| App does not open / unsure what is wrong | Run `python diagnose.py`; it checks the install, connects a driver, and saves a screenshot and page source. |
| Need locators for a new screen | Run `python xml_capture.py`, open that screen on the phone, and type a name to save its XML. |
| DigiLocker step times out | The OTP was not entered within 5 minutes. Enter it on the phone or write it to `otp.txt`. |
| Vehicle step fails with "verification attempt failed" | `TEST_VEHICLE_NUMBER` is not a vehicle the app's server can verify. Use a real registered number. |
| A Truecaller popup covers the app | The tests close it automatically. If it still blocks a step, turn off Truecaller's SMS popup on the test phone. |
