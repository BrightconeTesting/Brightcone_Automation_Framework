from behave import given, when, then
import time

@given('I open the Brightcone login page')
def step_impl(context):
    print("[STEP] Navigating to Login Page...")
    context.login_page.open()

@when('I enter my email "{email}"')
def step_impl(context, email):
    print(f"[STEP] Entering email: {email}")
    context.login_page.enter_email(email)
    context.email_address = email # Update context if different

@when('I click on the Continue button')
def step_impl(context):
    print("[STEP] Clicking on the Continue button...")
    context.login_page.click_continue()

@then('I fetch the latest 6-digit OTP from my Gmail inbox')
def step_impl(context):
    # Fetching for the OTP after 10 seconds wait (as per previous requirement)
    print("[STEP] Waiting 10s and fetching OTP from Gmail...")
    time.sleep(10)
    context.otp = context.gmail_util.get_otp_from_gmail(timeout=60, retry_interval=5)
    
    if not context.otp:
        raise Exception(f"Failed to fetch OTP from Gmail for {context.email_address}")
    
    print(f"[SUCCESS] OTP found: {context.otp}")

@then('I enter the 6-digit OTP into separate input fields')
def step_impl(context):
    print(f"[STEP] Entering OTP {context.otp} into separate fields...")
    context.otp_page.enter_otp(context.otp)

@then('I click on the Login button')
def step_impl(context):
    print("[STEP] Clicking on the Login button...")
    context.otp_page.click_login()

@then('I should be successfully logged in to the dashboard')
def step_impl(context):
    print("[STEP] Verifying successful login...")
    time.sleep(5)
    current_url = context.driver.current_url
    print(f"[DEBUG] Current URL after login: {current_url}")
    
    assert "https://staging-app.brightcone.ai" in current_url.lower() and ("login" not in current_url.lower() or "dashboard" in current_url.lower()), \
        f"Login verification failed! Current URL: {current_url}"
    print("[SUCCESS] Login verified successfully!")
