from selenium.webdriver.common.by import By
from base.base_page import BasePage
import time

class OTPPage(BasePage):
    # Locators
    LOGIN_BUTTON_USER = (By.XPATH, "//button[contains(text(), 'Login')]")  # Corrected user-provided XPath
    LOGIN_BUTTON_SUBMIT = (By.XPATH, "//button[@type='submit']") # Common pattern on the site

    def __init__(self, driver):
        super().__init__(driver)

    def enter_otp(self, otp_digits):
        """
        OTP digits should be a 6-character string.
        Each digit is entered into separate input boxes: //input[@id='otp-0'], //input[@id='otp-1'], etc.
        """
        print(f"DEBUG: Filling OTP boxes...")
        for index, digit in enumerate(otp_digits):
            otp_input_locator = (By.XPATH, f"//input[@id='otp-{index}']")
            self.type(otp_input_locator, digit)
            # Small delay to mimic human typing if needed, but selenium is usually fast enough
            # time.sleep(0.1)

    def click_login(self):
        """
        Try clicking the user-provided XPath first, then fallback to submit button if needed.
        """
        try:
            print(f"DEBUG: Attempting to click login using user XPath: {self.LOGIN_BUTTON_USER[1]}")
            self.click(self.LOGIN_BUTTON_USER)
        except Exception:
            print("DEBUG: User XPath failed or didn't trigger login. Trying //button[@type='submit']...")
            self.click(self.LOGIN_BUTTON_SUBMIT)

    def login_with_otp(self, otp):
        self.enter_otp(otp)
        self.click_login()
