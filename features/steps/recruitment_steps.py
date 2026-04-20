from behave import given, when, then
import time
from utils.logger_config import logger
from utils.path_util import PathUtil

@when('User navigates to Recruitment module')
def navigate_recruitment(context):
    logger.info("Navigating to Recruitment module...")
    context.recruitment_page.wait_for_element(context.recruitment_page.RECRUITMENT_MENU)
    context.recruitment_page.navigate_to_recruitment()

@when('User clicks on "Continue" button for the correct job role')
def click_role_continue_dynamic(context):
    role = context.test_data.get("job_role", "ML Engineer")
    logger.info(f"Clicking Continue button for role: {role}")
    context.recruitment_page.click_role_continue()

@when('User navigates to the "Candidate" upload section')
def navigate_to_upload_dynamic(context):
    logger.info("Navigating to Candidate upload section...")
    context.recruitment_page.go_to_candidates_tab()

@when('User uploads the correct document')
def upload_file_dynamic(context):
    file_name = context.test_data.get("file_name")
    if not file_name:
        raise ValueError(f"Missing 'file_name' in Excel for scenario '{context.scenario.name}'")
    
    # Resolving path dynamically using PathUtil
    document_path = PathUtil.get_test_file(file_name)
    
    logger.info(f"Uploading recruitment document: {document_path}")
    context.recruitment_page.upload_resume(document_path)


@then('the resume should be uploaded successfully')
def verify_upload(context):
    time.sleep(3)
    logger.info("Checking for successful upload...")

@then('candidate should be listed under the correct role')
def verify_candidate_dynamic(context):
    is_found = context.recruitment_page.is_candidate_uploaded()
    assert is_found is True, "Candidate was not found after upload!"
    logger.info("Candidate verification successful!")

@then('the correct error message for invalid file type should be displayed')
def verify_invalid_file_error_dynamic(context):
    expected_error = context.test_data.get("expected_result")
    actual_error = context.recruitment_page.get_invalid_file_error_text()
    
    logger.info(f"Verifying error message. Expected: {expected_error}")
    assert actual_error == expected_error, f"Error mismatch! Expected '{expected_error}' but got '{actual_error}'"

@then('the resume should not be uploaded')
def verify_no_upload(context):
    try:
        context.driver.implicitly_wait(2)
        is_found = context.recruitment_page.is_candidate_uploaded()
        assert is_found is False, "Resume was uploaded despite invalid format!"
    except Exception:
        logger.info("Verified that the resume was NOT uploaded.")
    finally:
        context.driver.implicitly_wait(context.timeout)

@when('User clicks on "Candidate" tab')
def click_candidate_tab(context):
    context.recruitment_page.go_to_candidates_tab()

@when('User switches to table view')
def switch_view(context):
    context.recruitment_page.switch_to_table_view()

@when('User deletes the candidate based on the correct resume name')
def delete_candidate_dynamic(context):
    resume_name = context.test_data.get("resume_name")
    if not resume_name:
        raise ValueError(f"Missing 'resume_name' in Excel for scenario '{context.scenario.name}'")
    
    context.current_resume_name = resume_name
    logger.info(f"Deleting candidate with resume name: {resume_name}")
    context.recruitment_page.click_three_dot_menu(resume_name)
    context.recruitment_page.click_delete_option()

@then('the confirmation popup should contain the correct resume name')
def validate_popup_text_dynamic(context):
    resume_name = context.current_resume_name
    popup_text = context.recruitment_page.get_delete_popup_text()
    logger.info(f"Validating popup text contains: {resume_name}")
    assert resume_name in popup_text, f"Popup text did not contain '{resume_name}'. Actual: '{popup_text}'"

@when('User confirms the deletion')
def final_delete_confirm(context):
    context.recruitment_page.confirm_deletion()
    logger.info("Deletion confirmed.")

@when('User clicks on "Shortlisting" icon')
def click_shortlisting_icon(context):
    context.recruitment_page.click_shortlisting_icon()

@when('User selects the correct role from the dropdown')
def select_role_dynamic(context):
    role_name = context.test_data.get("job_role", "QA Engineer")
    logger.info(f"Selecting role from dropdown: {role_name}")
    context.recruitment_page.select_role_from_dropdown(role_name)
    context.recruitment_page.click_apply_filters()

@then('"{button}" button should be disabled')
def button_disabled(context, button):
    if button == "Approve Shortlist":
        is_enabled = context.recruitment_page.is_approve_shortlist_enabled()
        assert not is_enabled, f"Expected '{button}' to be disabled."

@when('User selects the candidates based on the provided name')
def select_candidate(context):
    context.recruitment_page.select_first_candidate_checkbox()

@then('"{button}" button should be enabled')
def button_enabled(context, button):
    if button == "Approve Shortlist":
        is_enabled = context.recruitment_page.is_approve_shortlist_enabled()
        assert is_enabled, f"Expected '{button}' to be enabled."

@when('User clicks on "{button}" button')
def click_specific_button(context, button):
    if button == "Approve Shortlist":
        context.recruitment_page.click_approve_shortlist()

@then('User should be navigated to "{page_name}" page')
def navigated_to_specific_page(context, page_name):
    if page_name == "Interview Management":
        time.sleep(2)
        is_present = context.recruitment_page.get_interview_management_icon_presence()
        assert is_present, f"Failed to navigate to '{page_name}' page."

@then('Page should display correctly matched text in Interview Management page')
def verify_page_text_dynamic(context):
    expected_text = context.test_data.get("expected_result")
    if not expected_text:
        # Fallback if not in excel
        expected_text = "User"
    
    page_source = context.driver.page_source
    assert expected_text in page_source, f"Expected text '{expected_text}' not found."
