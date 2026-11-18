"""
TrucksUp Automation - Business Associate: Business document
============================================================
Profile type "Business Associate" chunne ke baad aata hai (KYC se pehle):
  1. Business proof type chuno (GSTIN / Trade License / Udyam / Bilty) -> Upload -> Camera -> capture
  2. Shop proof type chuno (Signage Board / Visiting Card) -> Upload -> Camera -> capture
  3. Next (dono upload hone par enable hota hai) -> KYC Verification
"""

from selenium.webdriver.support.ui import WebDriverWait

from locators import BusinessDocsLocators as B
from pages.base_page import BasePage
from utils.logger import get_logger

BUSINESS_PROOFS = {
    "gstin": B.GSTIN,
    "trade": B.TRADE_LICENSE,
    "udyam": B.UDYAM_AADHAAR,
    "bilty": B.BILTY,
}
SHOP_PROOFS = {
    "signage": B.SIGNAGE_BOARD,
    "visiting_card": B.VISITING_CARD,
}


class BusinessDocsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger()

    def is_business_docs_screen_visible(self, timeout=20):
        visible = self.is_element_visible(B.GSTIN, timeout=timeout)
        self.logger.info(f"Business document screen visible: {visible}")
        return visible

    def _capture_with_camera(self, upload_locator):
        """Upload -> Camera -> capture -> wapas docs screen"""
        self.click(upload_locator)
        self.click(B.SOURCE_CAMERA)
        self.dismiss_truecaller_popup(timeout=1)
        self.click(B.CAMERA_CAPTURE)
        # Capture ke baad docs screen par wapas aana chahiye
        WebDriverWait(self.driver, 20).until(
            lambda d: "BaDocsActivity" in (d.current_activity or "")
        )

    def upload_business_proof(self, proof="gstin"):
        self.logger.info(f"Business proof: {proof} -> camera photo")
        self.click(BUSINESS_PROOFS[proof])
        self._capture_with_camera(B.UPLOAD_BUSINESS_PROOF)

    def upload_shop_proof(self, proof="signage"):
        self.logger.info(f"Shop proof: {proof} -> camera photo")
        self.click(SHOP_PROOFS[proof])
        self._capture_with_camera(B.UPLOAD_SHOP_PROOF)

    def click_next(self):
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element(*B.NEXT_BUTTON).is_enabled()
        )
        self.click(B.NEXT_BUTTON)
        self.logger.info("Business document Next clicked")

    def complete_business_documents(self, business_proof="gstin", shop_proof="signage"):
        self.upload_business_proof(business_proof)
        self.upload_shop_proof(shop_proof)
        self.click_next()
