from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base.base_page import BasePage
import time

class RecruitmentPage(BasePage):
    # Locators
    SIDEBAR_EXPAND_BUTTON = (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/aside/div[1]/div[2]/button")
    RECRUITMENT_MENU = (By.XPATH, "//span[normalize-space()='Recruitment']")
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

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_recruitment(self):
        """
        Navigates to the Recruitment module by interacting with the UI menu.
        Ensures the menu is visible and clickable before attempting interaction.
        """
        print("DEBUG: Thinking like a tester - Locating Recruitment menu in the sidebar...")
        
        # 1. Ensure page is stable (wait for any global loaders to disappear)
        time.sleep(2) 
        
        try:
            # 2. Hover and click sidebar expand button, then verify Recruitment is visible.
            print("DEBUG: Trying to expand sidebar before locating Recruitment...")
            try:
                sidebar_btn = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(self.SIDEBAR_EXPAND_BUTTON)
                )
            except TimeoutException as e:
                current_url = self.driver.current_url
                print(
                    "ERROR: SIDEBAR_EXPAND_BUTTON was NOT found within 15 seconds. "
                    f"Locator={self.SIDEBAR_EXPAND_BUTTON}, URL={current_url}"
                )
                raise Exception(
                    f"SIDEBAR_EXPAND_BUTTON not found. Locator={self.SIDEBAR_EXPAND_BUTTON}, URL={current_url}"
                ) from e

            print(
                f"DEBUG: SIDEBAR_EXPAND_BUTTON found. "
                f"Displayed={sidebar_btn.is_displayed()}, Enabled={sidebar_btn.is_enabled()}"
            )

            # First attempt
            ActionChains(self.driver).move_to_element(sidebar_btn).pause(0.5).perform()
            try:
                sidebar_btn.click()
                print("DEBUG: Sidebar expand clicked using Selenium click.")
            except Exception as click_err:
                print(f"DEBUG: Selenium click failed on sidebar button: {click_err}. Using JS click.")
                try:
                    self.driver.execute_script("arguments[0].click();", sidebar_btn)
                    print("DEBUG: Sidebar expand clicked using JavaScript click.")
                except Exception as js_click_err:
                    raise Exception(
                        "SIDEBAR_EXPAND_BUTTON was found but click failed with both Selenium and JS click. "
                        f"Selenium error={click_err}, JS error={js_click_err}"
                    ) from js_click_err

            # If menu text did not appear, try one more time (DOM may re-render after first click)
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.RECRUITMENT_MENU)
                )
            except Exception:
                print("DEBUG: Recruitment menu still not visible after first expand click. Retrying sidebar click once...")
                sidebar_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.SIDEBAR_EXPAND_BUTTON)
                )
                ActionChains(self.driver).move_to_element(sidebar_btn).pause(0.5).perform()
                self.driver.execute_script("arguments[0].click();", sidebar_btn)
                try:
                    element = self.wait_for_visibility(self.RECRUITMENT_MENU, timeout=15)
                except Exception as menu_err:
                    raise Exception(
                        "SIDEBAR_EXPAND_BUTTON click completed, but RECRUITMENT_MENU still not visible after retry. "
                        f"Sidebar locator={self.SIDEBAR_EXPAND_BUTTON}, Recruitment locator={self.RECRUITMENT_MENU}, "
                        f"URL={self.driver.current_url}, Error={menu_err}"
                    ) from menu_err
            
            # 3. Scroll it into view to ensure it's not hidden behind a header/footer
            print("DEBUG: Scrolling Recruitment menu into view...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)

            # 4. Ensure menu is clickable
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.RECRUITMENT_MENU)
            )
            
            # 5. Perform JavaScript click as primary action for this menu item
            print("DEBUG: Performing JavaScript click on Recruitment menu...")
            self.driver.execute_script("arguments[0].click();", element)
            
        except Exception as e:
            print(f"DEBUG: Standard click failed or element not found. Attempting JavaScript click as fallback. Error: {str(e)}")
            # Fallback to JS click if the element is intercepted by a lingering overlay
            try:
                element = self.driver.find_element(*self.RECRUITMENT_MENU)
                self.driver.execute_script("arguments[0].click();", element)
                print("DEBUG: JavaScript click execution successful.")
            except Exception as js_e:
                print(f"ERROR: Failed to identify or click the Recruitment button. Error: {js_e}")
                raise js_e
            
        # 6. Verify navigation via URL change (not by forcing it, but by observing it)
        print("DEBUG: Waiting for navigation to complete...")
        WebDriverWait(self.driver, 15).until(lambda d: "recruitment" in d.current_url)
        print(f"DEBUG: Navigation confirmed. Current URL: {self.driver.current_url}")

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
