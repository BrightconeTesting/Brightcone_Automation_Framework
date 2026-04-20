from behave import given, when, then
import os
import time
from utils.logger_config import logger

@given('User launches the application')
def launch_app(context):
    logger.info(f"Launching app at {context.base_url} for role {context.role_name}")
    context.login_page.open_url(context.base_url)

@given('User logs in with valid credentials')
def login_valid_credentials(context):
    # Mapping friendly environment check
    logger.info(f"Target Base URL: {context.base_url}")
    email = context.current_user["email"]
    wait_time = context.current_user["otp_wait_time"]
    
    logger.info(f"Logging in with email: {email} (Role: {context.role_name})")
    context.login_page.enter_email(email)
    context.login_page.click_continue()
    
    logger.info(f"Waiting {wait_time}s for OTP...")
    time.sleep(wait_time)
    
    otp = context.gmail_util.get_otp_from_gmail()
    if not otp:
        raise ValueError(f"Failed to fetch OTP for {email}")
    
    context.otp_page.enter_otp(otp)
    context.otp_page.click_login()
    time.sleep(5)

from utils.path_util import PathUtil

@when('User uploads a document')
def upload_doc(context):
    # Use data from Excel (context.test_data)
    file_name = context.test_data.get("file_name")
    if not file_name:
        raise ValueError(f"Missing 'file_name' in Excel data for scenario '{context.scenario.name}'")
    
    # Resolving path dynamically using PathUtil
    document_path = PathUtil.get_test_file(file_name)
    
    logger.info(f"Uploading document: {document_path}")
    context.documents_page.upload_document(document_path)


@then('a popup with correctly matched text should appear')
def verify_dynamic_popup(context):
    # Use expected result from Excel
    expected_text = context.test_data.get("expected_result")
    logger.info(f"Verifying popup matches expected text: {expected_text}")
    
    actual_text = context.documents_page.get_notification_text()
    assert actual_text == expected_text, f"Expected '{expected_text}' but found '{actual_text}'"

@when('User selects the correct category')
def select_category_from_data(context):
    categories_str = context.test_data.get("category")
    if not categories_str:
        logger.warning("No category found for this scenario.")
        return
        
    # Split by comma and strip whitespace
    categories = [cat.strip() for cat in categories_str.split(',')]
    
    for category in categories:
        logger.info(f"Selecting category from Excel: '{category}'")
        context.documents_page.select_category(category)
        time.sleep(1) # Small pause between clicks

@when('User navigates to Documents page')
def navigate_documents(context):
    logger.info("Navigating to Documents page...")
    context.documents_page.navigate_to_documents()

@when('User clicks the "Upload" button')
def click_upload(context):
    logger.info("Clicking the final Upload button...")
    context.documents_page.click_upload_button()
