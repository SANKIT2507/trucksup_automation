"""
TrucksUp Automation - PyTest Configuration
=========================================
Driver setup aur teardown fixtures.
"""
print("========== conftest loaded ==========")
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.driver_factory import DriverFactory
from utils.logger import get_logger

logger = get_logger()


@pytest.fixture(scope="function")
def driver():
    """Har test ke liye fresh driver instance create karo"""
    logger.info("=" * 60)
    logger.info("STARTING NEW TEST")
    logger.info("=" * 60)

    driver = DriverFactory.get_driver()

    # Folders create karo
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    yield driver

    logger.info("Quitting driver...")
    driver.quit()
    logger.info("=" * 60)
    logger.info("TEST COMPLETED")
    logger.info("=" * 60)


@pytest.fixture
def aadhaar_number(request):
    """
    Test start hone se pehle Aadhaar number poocho.
    Enter dabao (khaali) ya terminal interactive na ho -> .env ka TEST_AADHAAR_NUMBER.
    """
    from config import Config

    capman = request.config.pluginmanager.getplugin("capturemanager")
    capman.suspend_global_capture(in_=True)
    try:
        value = input("\nAadhaar number daalo (12 digit, Enter = .env wala): ").strip()
    except (EOFError, OSError):
        value = ""
    finally:
        capman.resume_global_capture()

    value = value.replace(" ", "") or Config.TEST_AADHAAR_NUMBER
    if not (len(value) == 12 and value.isdigit()):
        pytest.fail(f"Aadhaar number 12 digit ka hona chahiye (mila: {len(value)} chars)")
    logger.info(f"Using Aadhaar ending {value[-4:]}")
    return value


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Test fail hone par automatic screenshot lo"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_name = f"screenshots/fail_{item.name}.png"
            driver.save_screenshot(screenshot_name)
            logger.info(f"Failure screenshot saved: {screenshot_name}")
