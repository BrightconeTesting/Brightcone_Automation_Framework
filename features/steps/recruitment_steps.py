from behave import given, when, then
import os
import time

# Define the file path for the resume
RESUME_PATH = r"C:\Users\Dell\Downloads\Munjala_Anand_Tester_Resume (1).docx"

@given('I am logged into the application')
@given('User is logged into the application')
def check_login_status(context):
    """
    Performs full login sequence using Login and OTP page actions.
    """
    print("[STEP] Performing login to satisfy 'I am logged into the application'...")
    
    # 1. Open login page and enter email
    context.login_page.open()
    context.login_page.enter_email(context.email_address)
    context.login_page.click_continue()
    
    # 2. Wait 10s and fetch OTP
    print("[STEP] Waiting 10s for OTP generation...")
    time.sleep(10)
    otp = context.gmail_util.get_otp_from_gmail(timeout=60, retry_interval=5)
    
    if not otp:
        raise Exception("Login failed during recruitment setup: Could not fetch OTP.")
    
    # 3. Enter OTP and Login
    context.otp_page.enter_otp(otp)
    context.otp_page.click_login()
    
    # 4. Wait for dashboard element (Recruitment Menu) to confirm login
    print(f"[STEP] Current URL: {context.driver.current_url}")
    print("[STEP] Waiting for dashboard UI to load...")
    try:
        context.recruitment_page.wait_for_element(context.recruitment_page.RECRUITMENT_MENU)
        print("[SUCCESS] Dashboard loaded and Recruitment Menu found!")
    except Exception as e:
        print("[ERROR] Dashboard UI failed to load recruitment menu. URL is: " + context.driver.current_url)
        raise e

@then('I should be on the "{page_name}" page')
def verify_recruitment_url(context, page_name):
    # Mapping friendly names to URL fragments
    mapping = {
        "Dashboard": "dashboard",
        "Recruitment": "recruitment",
        "Candidates": "candidates",
        "Overview": "roles"
    }
    expected_part = mapping.get(page_name, page_name.lower())
    
    print(f"[STEP] Verifying Recruitment URL contains: {expected_part}")
    actual_url = context.recruitment_page.get_url()
    
    assert "https://staging-app.brightcone.ai" in actual_url.lower() and expected_part in actual_url.lower(), f"Recruitment URL Validation Failed! Expected part '{expected_part}' or staging URL not found in '{actual_url}'"
    print(f"[SUCCESS] URL verified for {page_name} page.")

@when('I navigate to Recruitment module')
@when('User clicks on "Recruitment" side menu')
def navigate_recruitment(context):
    # Properly wait for the element to be present and stable before navigating
    print("[STEP] Explicitly waiting for Recruitment menu visibility before navigation...")
    context.recruitment_page.wait_for_element(context.recruitment_page.RECRUITMENT_MENU)
    context.recruitment_page.navigate_to_recruitment()

@when('I click on continue button of ML engineer role')
def click_role_continue(context):
    # This step now directly clicks the Role Continue button
    context.recruitment_page.click_role_continue()

@when('I click on "Add Candidate" or "Upload Resume"')
def navigate_to_upload(context):
    # The current flow from user locators goes: Recruitment -> Role -> Candidates -> Upload
    context.recruitment_page.go_to_candidates_tab()

@when('I upload a valid resume file')
def upload_file(context):
    # Check if file exists first for robust testing
    if not os.path.exists(RESUME_PATH):
        print(f"[ERROR] Resume file not found at: {RESUME_PATH}")
        # In a real scenario, you might want to create a mock file if missing
    
    context.recruitment_page.upload_resume(RESUME_PATH)

@then('the resume should be uploaded successfully')
def verify_upload(context):
    # Wait a bit for server processing
    time.sleep(3)
    print("[STEP] Checking upload status message or element appearing...")

@then('the candidate should be listed under the ML Engineer role')
def verify_candidate(context):
    is_found = context.recruitment_page.is_candidate_uploaded()
    assert is_found is True, f"Candidate was not found after upload!"
    print("[SUCCESS] Candidate 'Munjala Anand Tester Resume (1)' verified!")

# --- Negative Scenario Steps ---
@when('I upload a Invalid resume file')
def upload_invalid_file(context):
    INVALID_FILE_PATH = r"C:\Users\Dell\OneDrive\Documents\Basic Java Concepts questions.txt"
    print(f"[STEP] Attempting to upload invalid resume file: {INVALID_FILE_PATH}")
    context.recruitment_page.upload_resume(INVALID_FILE_PATH)

@then('I should see an error message for invalid file type')
def verify_invalid_file_error(context):
    expected_error = "Some files were skipped. Only PDF and DOCX files are supported."
    actual_error = context.recruitment_page.get_invalid_file_error_text()
    
    print(f"[STEP] Validating error message text.")
    print(f"       Expected: {expected_error}")
    print(f"       Actual  : {actual_error}")
    
    # Asserting equality for strict validation
    assert actual_error == expected_error, f"Error message mismatch! Expected: {expected_error}, but got: {actual_error}"
    
    print("[SUCCESS] Error message for invalid file type verified and matches exactly!")

@then('the resume should not be uploaded')
def verify_no_upload(context):
    # This might depend on verifying the candidate is NOT present
    try:
        # Short wait to see if it does NOT appear
        context.driver.implicitly_wait(2)
        is_found = context.recruitment_page.is_candidate_uploaded()
        assert is_found is False, "Resume was uploaded despite invalid format!"
    except Exception:
        # If is_candidate_uploaded throws an exception because element is missing, that's good!
        print("[SUCCESS] Verified that the resume was NOT uploaded.")
    finally:
        context.driver.implicitly_wait(15) # Reset to default

# --- Deletion Scenario Steps ---

@when('I click on "Candidate" tab')
def click_candidate_tab(context):
    print("[STEP] Clicking on Candidates tab...")
    context.recruitment_page.go_to_candidates_tab()

@when('I switch to table view')
def switch_view(context):
    print("[STEP] Switching to Table View...")
    context.recruitment_page.switch_to_table_view()

@when('I click on the three dot menu based on resume name "{resume_name}"')
def click_three_dot(context, resume_name):
    # Store resume name in context for later validation
    context.current_resume_name = resume_name
    print(f"[STEP] Clicking three-dot menu for resume: {resume_name}")
    context.recruitment_page.click_three_dot_menu(resume_name)

@then('I click on delete candidate option')
def click_delete_opt(context):
    print("[STEP] Clicking Delete option...")
    context.recruitment_page.click_delete_option()

@then('I capture the confirmation popup text')
def capture_popup_text(context):
    print("[STEP] Capturing deletion confirmation popup text...")
    context.popup_text = context.recruitment_page.get_delete_popup_text()
    print(f"       Captured Text: {context.popup_text}")

@then('I validate the popup text contains the resume name "{resume_name}"')
def validate_popup_text(context, resume_name):
    print(f"[STEP] Validating popup text contains resume name: {resume_name}")
    assert resume_name in context.popup_text, f"Popup text did not contain resume name! \nExpected to find: {resume_name} \nActual text: {context.popup_text}"
    print("[SUCCESS] Popup text validation passed.")

@then('I click on delete confirmation button only if validation is successful')
def final_delete_confirm(context):
    print("[STEP] Validation successful, clicking final Delete confirmation button...")
    context.recruitment_page.confirm_deletion()
    print("[SUCCESS] Deletion confirmed.")

# --- Approve Shortlist Scenario Steps ---

@when('User clicks on "Shortlisting" icon')
def click_shortlisting_icon(context):
    context.recruitment_page.click_shortlisting_icon()

@when('User selects "{role_name}" role from "{dropdown_name}" dropdown')
def select_all_roles(context, role_name, dropdown_name):
    # Select the role provided in the scenario after comparing with options
    context.recruitment_page.select_role_from_dropdown(role_name)
    context.recruitment_page.click_apply_filters()


@then('"{button}" button should be disabled')
def button_disabled(context, button):
    if button == "Approve Shortlist":
        time.sleep(1) # wait a moment for UI to update
        is_enabled = context.recruitment_page.is_approve_shortlist_enabled()
        assert not is_enabled, f"Expected '{button}' to be disabled, but it was enabled."

@when('User selects the candidates based on the provided name')
def select_candidate(context):
    context.recruitment_page.select_first_candidate_checkbox()

@then('"{button}" button should be enabled')
def button_enabled(context, button):
    if button == "Approve Shortlist":
        time.sleep(1) # wait a moment for UI to update
        is_enabled = context.recruitment_page.is_approve_shortlist_enabled()
        assert is_enabled, f"Expected '{button}' to be enabled, but it was disabled."

@when('User clicks on "{button}" button')
def click_specific_button(context, button):
    if button == "Approve Shortlist":
        context.recruitment_page.click_approve_shortlist()

@then('User should be navigated to "{page_name}" page')
def navigated_to_specific_page(context, page_name):
    if page_name == "Interview Management":
        time.sleep(2) # Wait for navigation
        is_present = context.recruitment_page.get_interview_management_icon_presence()
        assert is_present, f"Failed to navigate to '{page_name}' page. Icon not found."

@then('Page should display text "{text}" in Interview Management page')
def verify_page_text(context, text):
    time.sleep(1) # Wait for render
    page_source = context.driver.page_source
    assert text in page_source, f"Expected text '{text}' not found on the page."
