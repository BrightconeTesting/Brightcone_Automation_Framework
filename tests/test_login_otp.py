import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from utils.gmail_util import GmailUtil
import time
import os

# Test Data
EMAIL = "munjalaharikrishna123@gmail.com"
APP_PASSWORD = "linx lpbq ljjj widk"
LOGIN_URL = "https://staging-app.brightcone.ai"

@pytest.fixture(scope="session")
def driver():
    # Setup driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # For CI/CD environments
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    # Teardown
    driver.quit()

def test_login_with_otp(driver):
    """
    Test case to login using email and OTP from Gmail.
    """
    login_page = LoginPage(driver)
    otp_page = OTPPage(driver)
    gmail_util = GmailUtil(EMAIL, APP_PASSWORD)

    # 1. Open the URL and Enter email
    print(f"\n[STEP 1] Navigating to {LOGIN_URL} and entering email: {EMAIL}")
    login_page.login_upto_otp(EMAIL)

    # REQUIREMENT: Wait 10 seconds after clicking submit before fetching OTP
    print("Wait 10 seconds for OTP email to be generated...")
    time.sleep(10)

    # 2. Fetch for OTP
    print("\n[STEP 2] Fetching 6-digit OTP from Gmail...")
    otp = gmail_util.get_otp_from_gmail(timeout=60, retry_interval=5)
    
    if not otp:
        pytest.fail("Failed to fetch OTP from Gmail! Check credentials or account status.")

    # REQUIREMENT: print the otp in the console before entering
    print(f"*** FOUND OTP: {otp} ***")
    print(f"Entering OTP {otp} now...")
    print("OTP:", otp)

    # 3. Enter OTP into 6 input fields 
    print("[STEP 3] Entering OTP digits into separate input boxes...")
    try:
        otp_page.enter_otp(otp)
    except Exception as e:
        print(f"ERROR: Could not enter OTP. Are we on the OTP page? Error: {e}")
        pytest.fail("Failed to proceed to OTP page. Check if the email is registered.")

    # 4. Click Login
    print("[STEP 4] Clicking Login button...")
    otp_page.click_login()

    # REQUIREMENT: wait 5seconds after click on login button
    print("Wait 5 seconds for redirection...")
    time.sleep(5)

    # 5. Verify Login (Check if URL changes or post-login element appears)
    current_url = driver.current_url
    print(f"[DEBUG] Current URL after login: {current_url}")
    
    # Simple assertion for demonstration
    assert "https://staging-app.brightcone.ai" in current_url.lower() and ("login" not in current_url.lower() or "dashboard" in current_url.lower()), "Login failed! Still on the login page."
    print("[SUCCESS] Login test completed!")

if __name__ == "__main__":
    pytest.main([__file__])
