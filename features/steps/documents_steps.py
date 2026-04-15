from behave import given, when, then
from selenium.webdriver.common.by import By # Fixed internal import
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# File path provided by the user
DOCUMENT_PATH = r"C:\Users\Dell\Downloads\LabEasy.pdf"

@given('User launches the application')
def launch_app(context):
    # Demonstration: Using JSON and Excel data from context
    env = context.json_data.get("environment", "unknown")
    print(f"[STEP] Launching application in {env} environment...")
    
    # Optionally use Excel data
    # login_data = context.excel_data[0]
    # print(f"Using test credentials for: {login_data['test_case_id']}")
    
    context.login_page.open()

@given('User logs in with valid credentials')
def login_valid_credentials(context):
    """
    Handles the login flow using existing page objects.
    """
    print("[STEP] Logging in with valid credentials...")
    # 1. Enter email and continue
    context.login_page.enter_email(context.email_address)
    context.login_page.click_continue()
    
    # 2. Wait for page transition (3s) and then start OTP fetch
    print("[STEP] Continuing to OTP page...")
    time.sleep(3) 
    print("[STEP] Waiting 10s for OTP generation in Gmail...")
    time.sleep(10)
    otp = context.gmail_util.get_otp_from_gmail(timeout=60, retry_interval=5)
    
    if not otp:
        raise Exception("Failed to fetch OTP for document upload login.")
    
    # 3. Enter OTP and login
    context.otp_page.enter_otp(otp)
    context.otp_page.click_login()
    
    # 4. Wait for dashboard to stabilize
    time.sleep(5)
    print("[SUCCESS] Login successful.")

@then('User should be on the "{page_name}" page')
def verify_page_url(context, page_name):
    # Mapping friendly names to URL fragments
    mapping = {
        "Dashboard": "dashboard",
        "Documents": "documents"
    }
    expected_part = mapping.get(page_name, page_name.lower())
    
    print(f"[STEP] Verifying URL contains: {expected_part}")
    actual_url = context.documents_page.get_url()
    
    assert "https://staging-app.brightcone.ai" in actual_url.lower() and expected_part in actual_url.lower(), f"URL Validation Failed! Expected part '{expected_part}' or staging URL not found in '{actual_url}'"
    print(f"[SUCCESS] URL verified for {page_name} page.")

@when('User navigates to Documents page')
def navigate_documents(context):
    context.documents_page.navigate_to_documents()

@when('User selects the "{cat1}", "{cat2}" and "{cat3}" categories')
def select_multiple_categories(context, cat1, cat2, cat3):
    categories = [cat1, cat2, cat3]
    for category in categories:
        print(f"[STEP] Selecting category: {category}")
        context.documents_page.select_category(category)
        time.sleep(1) # Minor pause between selections

@when('User uploads a document')
def upload_doc(context):
    time.sleep(2) # Give UI time to stabilize
    context.documents_page.upload_document(DOCUMENT_PATH)

@when('User clicks the "Upload" button')
def click_upload(context):
    time.sleep(2) # Wait for file to list before confirmation
    context.documents_page.click_upload_button()
@then('a popup with text "{expected_text}" should appear')
def verify_popup_text(context, expected_text):
    print(f"[STEP] Verifying popup text matches: {expected_text}")
    raw_text = context.documents_page.get_notification_text()
    
    # Remove emoji (non-ASCII) and normalize whitespace
    import re
    actual_text = re.sub(r'[^\x00-\x7F]+', '', raw_text).strip()
    
    print(f"DEBUG: Cleaned actual text: '{actual_text}'")
    
    # Validation logic: Only print if it matches exactly
    if actual_text == expected_text:
        print("uploaded document was uder review")
    
    assert actual_text == expected_text, f"Expected popup text '{expected_text}' but found '{actual_text}' (Raw: '{raw_text}')"


@then('Uploaded document should be visible in My Uploads')
def verify_upload_visible(context):
    # Get the file name from path
    context.captured_file_name = os.path.basename(DOCUMENT_PATH)
    print(f"[STEP] Verifying document '{context.captured_file_name}' is visible...")
    
    try:
        # Using the new reused method that handles scrolling and visibility
        element = context.documents_page.find_document_and_scroll(context.captured_file_name)
        assert element.is_displayed(), f"Document {context.captured_file_name} not visible in UI."
        print(f"[SUCCESS] Document {context.captured_file_name} is visible.")
    except Exception as e:
        raise Exception(f"Failed to find uploaded document: {context.captured_file_name}. Error: {e}")

@then('User should capture the document name')
def capture_doc_name(context):
    # Already captured in the previous step, but ensuring it's available
    if not hasattr(context, 'captured_file_name'):
        context.captured_file_name = os.path.basename(DOCUMENT_PATH)
    print(f"[STEP] Captured document name: {context.captured_file_name}")

