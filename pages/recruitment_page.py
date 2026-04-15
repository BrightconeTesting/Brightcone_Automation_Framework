from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_page import BasePage
import time

class RecruitmentPage(BasePage):
    # Locators
    # RECRUITMENT_MENU = (By.XPATH, "(//span[text()='Recruitment'])[1]") # Old strict xpath
    RECRUITMENT_MENU = (By.XPATH, "//span[contains(text(), 'Recruitment')]")
    ROLE_CONTINUE_BUTTON = (By.XPATH, "(//span[text()='Continue'])[1]")
    CANDIDATES_BUTTON = (By.XPATH, "//button[text()='Candidates']")
    UPLOAD_RESUME_BUTTON = (By.XPATH, "//span[text()='Upload Resume']")
    RESUME_FILE_INPUT = (By.XPATH, "//input[@id='resume-upload']")
    UPLOAD_CONFIRM_BUTTON = (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/form/div[3]/button[2]")
    CANDIDATE_VERIFICATION = (By.XPATH, "//span[text()='Munjala Anand Tester Resume (1)']")
    INVALID_FILE_ERROR = (By.XPATH, "//span[text()='Some files were skipped. Only PDF and DOCX files are supported.']")
    UPLOAD_SUCCESS_MSG = (By.XPATH, "//*[text()='Upload Successful']")
    
    # Candidate Deletion Locators
    DELETE_OPTION = (By.XPATH, "//div[@role='menu']//div[contains(., 'Delete')]")
    DELETE_POPUP_TEXT = (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/p')
    DELETE_CONFIRM_BTN = (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/button[2]')
    TABLE_VIEW_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[3]/div/div[1]/div[5]/div[2]')

    # Approve Shortlist Locators
    SHORTLISTING_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[1]/div/div[4]/div')
    ALL_ROLES_DROPDOWN = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[2]/div/div[2]/select')
    APPLY_FILTERS_BTN = (By.XPATH, "//span[text()='Apply Filters']")
    CANDIDATE_CHECKBOX = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[3]/div/div[1]/table/tbody/tr/td[1]/input')
    APPROVE_SHORTLIST_BTN = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[1]/div[2]/button[2]')
    INTERVIEW_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[1]/div/div[5]/img')
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_recruitment(self):
        print("DEBUG: Waiting for Recruitment menu to be clickable (page load check)...")
        # Ensure the Recruitment menu is ready before clicking
        # The .click() method already uses wait_for_clickable, but we'll add a log for clarity
        self.click(self.RECRUITMENT_MENU)

    def click_role_continue(self):
        """
        Directly clicks the Role Continue button for the desired role.
        """
        print("DEBUG: Clicking Role Continue button...")
        self.click(self.ROLE_CONTINUE_BUTTON)

    def go_to_candidates_tab(self):
        print("DEBUG: Navigating to Candidates tab...")
        self.click(self.CANDIDATES_BUTTON)

    def upload_resume(self, file_path):
        """
        Handles the file upload process using send_keys on the hidden input.
        Checks if the confirm button is enabled before clicking.
        """
        print("DEBUG: Clicking Upload Resume button...")
        self.click(self.UPLOAD_RESUME_BUTTON)
        
        print(f"DEBUG: Sending file path to input: {file_path}")
        # Wait for the input field to be present and send keys
        file_input = self.wait_for_element(self.RESUME_FILE_INPUT)
        file_input.send_keys(file_path)
        
        print("DEBUG: Checking if Upload Confirm button is enabled...")
        # Add explicit wait for the confirm button element to be present
        try:
            wait_5s = WebDriverWait(self.driver, 5)
            # Find the element first to check its properties
            confirm_btn = wait_5s.until(EC.presence_of_element_located(self.UPLOAD_CONFIRM_BUTTON))
            
            if confirm_btn.is_enabled():
                print("DEBUG: Upload Confirm button was enabled. Clicking it...")
                confirm_btn.click()
            else:
                print("DEBUG: UPLOAD_CONFIRM_BUTTON was disabled. Skipping click and continuing...")
        except Exception as e:
            print(f"DEBUG: Upload Confirm button not found or interaction failed. Proceeding... Error: {e}")

    def is_candidate_uploaded(self):
        """
        Verifies if the specified candidate appeared in the list.
        """
        print("DEBUG: Verifying candidate presence...")
        # Wait for the candidate element to appear
        element = self.wait_for_element(self.CANDIDATE_VERIFICATION)
        return element.is_displayed()

    def is_error_displayed(self):
        """
        Checks for the 'unsupported file type' error message.
        """
        print("DEBUG: Checking for invalid file type error...")
        try:
            # Using current wait defined in BasePage
            element = self.wait_for_element(self.INVALID_FILE_ERROR)
            return element.is_displayed()
        except Exception:
            return False

    def get_invalid_file_error_text(self):
        """
        Retrieves the actual text from the INVALID_FILE_ERROR element for validation.
        """
        print("DEBUG: Fetching actual text content from invalid file error message...")
        element = self.wait_for_element(self.INVALID_FILE_ERROR)
        return element.text.strip()

    def get_upload_success_text(self):
        """
        Retrieves the text from the Upload Success popup/message.
        """
        print("DEBUG: Fetching actual text content from upload success message...")
        element = self.wait_for_element(self.UPLOAD_SUCCESS_MSG)
        return element.text.strip()

    def click_three_dot_menu(self, resume_name):
        """
        Clicks the three-dot 'More Actions' menu for a specific resume.
        """
        xpath = f"//span[@title='{resume_name}']/ancestor::tr//button[@title='More Actions']"
        print(f"DEBUG: Clicking three-dot menu for resume: {resume_name}")
        self.click((By.XPATH, xpath))

    def click_delete_option(self):
        print("DEBUG: Clicking Delete candidate option...")
        self.click(self.DELETE_OPTION)

    def get_delete_popup_text(self):
        print("DEBUG: Fetching delete confirmation popup text...")
        element = self.wait_for_element(self.DELETE_POPUP_TEXT)
        return element.text.strip()

    def confirm_deletion(self):
        print("DEBUG: Clicking final delete confirmation button...")
        self.click(self.DELETE_CONFIRM_BTN)

    def switch_to_table_view(self):
        print("DEBUG: Clicking Table View icon...")
        self.click(self.TABLE_VIEW_ICON)

    def click_shortlisting_icon(self):
        print("DEBUG: Clicking Shortlisting icon...")
        self.click(self.SHORTLISTING_ICON)

    def select_role_from_dropdown(self, role_name):
        print(f"DEBUG: Attempting to select role '{role_name}' from dropdown...")
        from selenium.webdriver.support.ui import Select
        dropdown_element = self.wait_for_element(self.ALL_ROLES_DROPDOWN)
        select = Select(dropdown_element)
        
        # Get all options and store them in a list
        options = [option.text.strip() for option in select.options]
        print(f"DEBUG: Found dropdown options: {options}")
        
        # Compare and select
        for option_text in options:
            if option_text == role_name:
                print(f"DEBUG: Match found for '{role_name}'. Selecting...")
                select.select_by_visible_text(role_name)
                return
        
        raise Exception(f"Role '{role_name}' not found in dropdown options: {options}")

    def click_apply_filters(self):
        print("DEBUG: Clicking Apply Filters button...")
        self.click(self.APPLY_FILTERS_BTN)

    def is_approve_shortlist_enabled(self):
        print("DEBUG: Checking if Approve Shortlist button is enabled...")
        try:
            element = self.wait_for_element(self.APPROVE_SHORTLIST_BTN)
            return element.is_enabled()
        except Exception:
            return False

    def select_first_candidate_checkbox(self):
        print("DEBUG: Selecting first candidate from the table...")
        self.click(self.CANDIDATE_CHECKBOX)

    def click_approve_shortlist(self):
        print("DEBUG: Clicking Approve Shortlist button...")
        self.click(self.APPROVE_SHORTLIST_BTN)
        
    def get_interview_management_icon_presence(self):
        print("DEBUG: Checking for Interview Management icon/text...")
        try:
            element = self.wait_for_element(self.INTERVIEW_ICON)
            return element.is_displayed()
        except:
            return False
