from selenium.webdriver.common.by import By
<<<<<<< HEAD
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
=======
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
from base.base_page import BasePage
import time

class RecruitmentPage(BasePage):
    # Locators
<<<<<<< HEAD
    SIDEBAR_EXPAND_BUTTON = (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/aside/div[1]/div[2]/button")
    RECRUITMENT_MENU = (By.XPATH, "//span[normalize-space()='Recruitment']")
=======
    # RECRUITMENT_MENU = (By.XPATH, "(//span[text()='Recruitment'])[1]") # Old strict xpath
    RECRUITMENT_MENU = (By.XPATH, "//span[contains(text(), 'Recruitment')]")
    RECRUITMENT_MENU_ADMIN = (By.XPATH, "//aside//a[@href='/admin/recruitment']")
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
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

<<<<<<< HEAD
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
=======
    # Approve Shortlist Locators
    SHORTLISTING_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[1]/div/div[4]/div')
    ALL_ROLES_DROPDOWN = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[2]/div/div[2]/select')
    APPLY_FILTERS_BTN = (By.XPATH, "//span[text()='Apply Filters']")
    CANDIDATE_CHECKBOX = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[3]/div/div[1]/table/tbody/tr/td[1]/input')
    APPROVE_SHORTLIST_BTN = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[3]/div/div/div[1]/div[2]/button[2]')
    INTERVIEW_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[1]/div/div[5]/img')

    # Google Drive Scenario Locators
    ROLE_START_BUTTON = (By.XPATH, "(//span[text()='Start'])[1]")
    # Dynamic locator as requested
    ROLE_DYNAMIC_XPATH = "(//h4[normalize-space()='{role_name}']/following::button[.//span[normalize-space()='Start']])[1]"
    SOURCE_DROPDOWN = (By.XPATH, "//button[@role='combobox']")
    DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='option']")
    GD_LINK_INPUT = (By.XPATH, "//input[contains(@placeholder, 'link') or contains(@placeholder, 'URL')]") # Generic placeholder
    CONFIGURE_BUTTON = (By.XPATH, "//span[text()='Save Configuration']")
    CANDIDATE_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search Candidates' or @placeholder='Search']")
    CANDIDATE_NAME_TEXT = (By.XPATH, "//span[contains(@class, 'candidate-name') or @title]") # Generic
    MY_QUEUE_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div[1]/div/div[2]')
    
    # Interview Slot Locators
    INTERVIEW_ICON = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[1]/div/div[5]")
    DROPDOWN_CONTAINER_V2 = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/div/div[1]/div[2]/div/div/div/span")
    DROPDOWN_OPTIONS_V2 = (By.XPATH, "//div[contains(@class,'fixed')]//div[contains(@class,'group') and contains(@class,'items-center')]")
    SLOT_POOL_BUTTON = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/div/div[2]/div/button[2]")
    ADD_SLOTS_BUTTON = (By.XPATH, "//span[text()='Add Slots']")
    START_DATE_INPUT = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/input")
    END_DATE_INPUT = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/div/div/input")
    INTERVIEWER_INPUT = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/input")
    CREATE_SLOT_BUTTON = (By.XPATH, "//span[text()='Create Slots']")
    SYNC_FROM_CALENDAR_BUTTON = (By.XPATH, "//span[text()='Sync from Calendar']")
    FROM_DATE_INPUT = (By.XPATH, "//input[@placeholder='From Date']")
    TO_DATE_INPUT = (By.XPATH, "//input[@placeholder='To Date']")
    INTERVIEWER_MAIL_INPUT = (By.XPATH, "//input[@placeholder='interviewer1@company.com, interviewer2@company.com']")
    SLOT_DURATION_DROPDOWN = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div/select")
    SYNC_SLOTS_BUTTON = (By.XPATH, "//span[text()='Sync Slots']")
    INVITATION_TAB = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/div/div[2]/div/button[3]")
    INVITATION_SEND_BUTTON = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div/div[1]/div[2]/button[2]/span")
    SEND_ALL_CONFIRMATION_BUTTON = (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/button[2]")

    # Re-schedule Locators
    INTERVIEW_ICON_V3 = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[1]/div/div[5]")
    ROLE_DROPDOWN_V3 = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/div/div[1]/div[2]/div/div/div/span")
    SCHEDULE_SECTION = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/div/div[2]/div/button[4]")
    PAST_BUTTON = (By.XPATH, "//span[text()='Past']")
    ACTION_MENU_BTN = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[6]/div/button")
    RESCHEDULE_BTN = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[6]/div/div[2]/div/button[2]")
    RESCHEDULE_START_TIME = (By.XPATH, "//input[@placeholder='Select new start time']")
    RESCHEDULE_END_TIME = (By.XPATH, "//input[@placeholder='Select new end time']")
    RESCHEDULE_REASON = (By.XPATH, "//textarea[@placeholder='Brief reason for the candidate...']")
    CONFIRM_RESCHEDULE = (By.XPATH, "//span[text()='Confirm Reschedule']")
    STATUS_ELEMENT = (By.XPATH, "//span[text()='CONFIRMED']")
    CANCEL_BTN = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/main/div/div/div/div[2]/div/div[1]/table/tbody/tr/td[6]/div/div[2]/div/button[4]")
    CONFIRM_CANCELLATION = (By.XPATH, "//button[text()='Confirm Cancellation']")
    STATUS_CANCELLED = (By.XPATH, "//span[text()='CANCELLED']")
    FEEDBACK_SECTION = (By.XPATH, "//button[contains(., 'Feedback')]")
    SUBMITTED_OPTION = (By.XPATH, "//span[text()='Submitted']")
    REVIEW_BTN = (By.XPATH, "//button[text()='Review']")
    HIRE_STATUS = (By.XPATH, "//div[text()='HIRE']")
    BRIGHTFIT_SCORE = (By.XPATH, "/html/body/div/div[1]/div/main/div/div[1]/div/div[3]/div[3]/div/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/span[1]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_recruitment(self, role="user"):
        print(f"DEBUG: Navigating to Recruitment for role: {role}")
        if role.lower() == "admin":
            print("DEBUG: Using Admin specific XPath for Recruitment menu")
            self.click(self.RECRUITMENT_MENU_ADMIN)
        else:
            print("DEBUG: Waiting for Recruitment menu to be clickable (page load check)...")
            self.click(self.RECRUITMENT_MENU)
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201

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
<<<<<<< HEAD
=======

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

    def select_from_dynamic_dropdown(self, dropdown_locator, option_text):
        """
        Clicks the dropdown and selects an option dynamically.
        If no option_text is provided, selects a random option.
        """
        print(f"DEBUG: Clicking dropdown: {dropdown_locator}")
        self.click(dropdown_locator)

        print("DEBUG: Waiting for all options to be visible...")
        # Use the provided locator for options
        options = self.wait_for_all_elements_visible(self.DROPDOWN_OPTIONS)

        if not option_text or option_text == "None" or option_text == "":
            import random
            random_option = random.choice(options)
            selected_text = random_option.text.strip()
            print(f"DEBUG: No specific value provided in Excel, selecting random option: {selected_text}")
            random_option.click()
            return selected_text
        else:
            print(f"DEBUG: Searching for matching option: {option_text}")
            for option in options:
                if option.text.strip() == option_text:
                    print(f"DEBUG: Match found. Selecting '{option_text}'")
                    option.click()
                    return option_text
            raise Exception(f"Option '{option_text}' not found in dropdown. Available: {[o.text.strip() for o in options]}")

    def search_and_open_role(self, role_name):
        """
        Searches for the role and opens it using a specific dynamic XPath.
        Ensures visibility, scrolls into view, and uses a JS click fallback.
        """
        print(f"DEBUG: Opening role using dynamic XPath for: {role_name}")
        # Build dynamic XPath using role name from Excel
        dynamic_xpath = self.ROLE_DYNAMIC_XPATH.format(role_name=role_name)
        locator = (By.XPATH, dynamic_xpath)
        
        try:
            # 1. Wait and Scroll
            element = self.scroll_into_view(locator)
            # 2. Wait for clickability
            self.wait_for_clickable(locator)
            
            print("DEBUG: Attempting standard Selenium click...")
            element.click()
        except Exception as e:
            print(f"DEBUG: Standard click failed or element intercepted. Attempting JS click fallback. Error: {e}")
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def click_my_queue_icon(self):
        print("DEBUG: Clicking My Queue icon...")
        self.click(self.MY_QUEUE_ICON)

    def paste_google_drive_link(self, link):
        print(f"DEBUG: Pasting Google Drive link: {link}")
        self.type(self.GD_LINK_INPUT, link)

    def click_save_configuration(self):
        print("DEBUG: Clicking Save Configuration...")
        self.click(self.CONFIGURE_BUTTON)

    def search_candidate(self, candidate_name):
        print(f"DEBUG: Searching for candidate: {candidate_name}")
        self.type(self.CANDIDATE_SEARCH_INPUT, candidate_name)
        time.sleep(2)

    def is_candidate_displayed(self, candidate_name):
        print(f"DEBUG: Verifying if candidate '{candidate_name}' is displayed...")
        xpath = f"//*[contains(text(), '{candidate_name}')]"
        try:
            element = self.wait_for_visibility((By.XPATH, xpath))
            return element.is_displayed()
        except:
            return False

    def navigate_to_interviews(self):
        print("DEBUG: Navigating to Interviews section...")
        locator = self.INTERVIEW_ICON
        try:
            # 1. Wait and Scroll
            self.scroll_into_view(locator)
            # 2. Wait for clickability
            self.wait_for_clickable(locator).click()
        except Exception as e:
            print(f"DEBUG: Interview icon click failed or element intercepted. Attempting JS click fallback. Error: {e}")
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def select_role_dynamic_v2(self, role_name):
        """
        Dynamically handles the role dropdown in Interviews section.
        Clicks directly on the dropdown container as requested.
        """
        locator = self.DROPDOWN_CONTAINER_V2
        
        try:
            # Attempt standard click with wait
            self.scroll_into_view(locator)
            self.wait_for_clickable(locator).click()
        except Exception as e:
            print(f"DEBUG: Dropdown container click failed. Attempting JS click fallback. Error: {e}")
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
        
        print("DEBUG: Waiting for dropdown options to be visible...")
        options_elements = self.wait_for_all_elements_visible(self.DROPDOWN_OPTIONS_V2)
        options_text = [opt.text.strip() for opt in options_elements]
        print(f"DEBUG: Found {len(options_text)} options: {options_text}")

        if not role_name or role_name == "None" or role_name == "":
            import random
            idx = random.randint(0, len(options_elements) - 1)
            selected = options_text[idx]
            print(f"DEBUG: No role in Excel, selecting random: {selected}")
            options_elements[idx].click()
            return selected
        else:
            print(f"DEBUG: Searching for matching role: {role_name}")
            for opt in options_elements:
                if opt.text.strip() == role_name:
                    print(f"DEBUG: Match found. Clicking '{role_name}'")
                    opt.click()
                    return role_name
            raise Exception(f"Role '{role_name}' not found in dropdown. Available: {options_text}")

    def is_slot_pool_tab_enabled(self):
        print("DEBUG: Checking if Slot Pool tab is enabled...")
        element = self.wait_for_element(self.SLOT_POOL_BUTTON)
        # Often 'enabled' in UI means not having a 'disabled' attribute or class
        return element.is_enabled()

    def click_slot_pool_tab(self):
        print("DEBUG: Clicking Slot Pool tab...")
        self.click(self.SLOT_POOL_BUTTON)

    def click_add_slots_button(self):
        print("DEBUG: Clicking Add Slots button...")
        self.click(self.ADD_SLOTS_BUTTON)

    def enter_interview_details(self, start_date, end_date, interviewer):
        print(f"DEBUG: Entering Start Date: {start_date}")
        self.type(self.START_DATE_INPUT, start_date)
        
        print(f"DEBUG: Entering End Date: {end_date}")
        self.type(self.END_DATE_INPUT, end_date)
        
        print(f"DEBUG: Entering Interviewer: {interviewer}")
        self.type(self.INTERVIEWER_INPUT, interviewer)

    def click_create_slots(self):
        print("DEBUG: Clicking Create Slots...")
        self.click(self.CREATE_SLOT_BUTTON)

    def click_invitation_tab(self):
        print("DEBUG: Clicking Invitation tab...")
        self.click(self.INVITATION_TAB)

    def select_candidate_for_invitation(self, candidate_name):
        print(f"DEBUG: Selecting candidate '{candidate_name}' for invitation...")
        # Adding a wait for the table to load
        time.sleep(5)
        
        # Log all available spans in the table to see what's there
        all_spans = self.driver.find_elements(By.XPATH, "//table//span")
        available_names = [span.text or span.get_attribute('title') for span in all_spans if span.text or span.get_attribute('title')]
        print(f"DEBUG: Available names in table: {available_names}")

        checkbox_xpath = f"//span[contains(@title, '{candidate_name}') or contains(text(), '{candidate_name}')]/ancestor::tr//input[@type='checkbox']"
        locator = (By.XPATH, checkbox_xpath)
        
        try:
            # 1. Scroll into view
            self.scroll_into_view(locator)
            # 2. Wait and Click
            self.wait_for_clickable(locator).click()
            print(f"DEBUG: Successfully selected candidate: {candidate_name}")
            time.sleep(2) # Wait 2s after clicking checkbox
        except Exception as e:
            print(f"ERROR: Could not select candidate '{candidate_name}'. Available names: {available_names}")
            print(f"DEBUG: Target locator was: {locator}")
            raise e

    def click_send_invitation_button(self):
        print("DEBUG: Scrolling to and clicking Send Invitation button...")
        locator = self.INVITATION_SEND_BUTTON
        self.scroll_into_view(locator)
        # Normal click using Selenium after waiting for clickability
        self.wait_for_clickable(locator).click()
        time.sleep(3) # Wait 3s after clicking send button

    def click_send_all_button(self):
        print("DEBUG: Clicking Send All button...")
        self.click(self.SEND_ALL_CONFIRMATION_BUTTON)
        time.sleep(2)

    def click_sync_from_calendar(self):
        print("DEBUG: Clicking Sync from Calendar button...")
        self.click(self.SYNC_FROM_CALENDAR_BUTTON)

    def fill_sync_calendar_details(self, from_date, to_date, interviewer_mail, duration):
        print(f"DEBUG: Filling Sync calendar details: From={from_date}, To={to_date}, Mail={interviewer_mail}, Duration={duration}")
        from selenium.webdriver.common.keys import Keys
        
        # 1. Fill From Date and close picker
        print("DEBUG: Entering From Date...")
        from_input = self.wait_for_element(self.FROM_DATE_INPUT)
        from_input.clear()
        from_input.send_keys(from_date)
        from_input.send_keys(Keys.ESCAPE)
        time.sleep(1)
        
        # 2. Fill To Date and close picker
        print("DEBUG: Entering To Date...")
        to_input = self.wait_for_element(self.TO_DATE_INPUT)
        to_input.clear()
        to_input.send_keys(to_date)
        to_input.send_keys(Keys.ESCAPE)
        time.sleep(1)
        
        # 3. Enter Interviewer Mail
        print("DEBUG: Entering Interviewer Mail...")
        self.type(self.INTERVIEWER_MAIL_INPUT, interviewer_mail)
        self.driver.find_element(By.TAG_NAME, 'body').click() # Final click to be sure
        
        # 4. Stable Dropdown Interaction
        print("DEBUG: Selecting slot duration with stable interaction...")
        locator = self.SLOT_DURATION_DROPDOWN
        self.scroll_into_view(locator)
        dropdown_element = self.wait_for_clickable(locator)
        
        from selenium.webdriver.support.ui import Select
        select = Select(dropdown_element)
        print(f"DEBUG: Selecting duration: {duration}")
        select.select_by_visible_text(duration)

        # 5. Final Sync Action
        print("DEBUG: Clicking Sync Slots button...")
        self.click(self.SYNC_SLOTS_BUTTON)
        time.sleep(3)

    def click_schedule_section(self):
        print("DEBUG: Clicking Schedule section...")
        self.click(self.SCHEDULE_SECTION)

    def click_past_button(self):
        print("DEBUG: Clicking Past button...")
        self.click(self.PAST_BUTTON)

    def click_action_menu(self):
        print("DEBUG: Clicking Action Menu...")
        self.click(self.ACTION_MENU_BTN)

    def click_reschedule_option(self):
        print("DEBUG: Clicking Re-schedule button...")
        self.click(self.RESCHEDULE_BTN)

    def enter_reschedule_details(self, start_time, end_time, reason="Testing Re-schedule"):
        print(f"DEBUG: Entering Re-schedule Start Time: {start_time}")
        self.type(self.RESCHEDULE_START_TIME, start_time)
        print(f"DEBUG: Entering Re-schedule End Time: {end_time}")
        self.type(self.RESCHEDULE_END_TIME, end_time)
        print(f"DEBUG: Entering Re-schedule Reason: {reason}")
        self.type(self.RESCHEDULE_REASON, reason)

    def confirm_reschedule(self):
        print("DEBUG: Clicking Confirm Reschedule...")
        self.click(self.CONFIRM_RESCHEDULE)

    def get_status_text(self):
        print("DEBUG: Getting status text...")
        # Check if the element is CONFIRMED or CANCELLED or any span
        try:
            element = self.wait_for_element(self.STATUS_ELEMENT)
            return element.text.strip()
        except:
            element = self.wait_for_element(self.STATUS_CANCELLED)
            return element.text.strip()

    def click_cancel_option(self):
        print("DEBUG: Clicking Cancel button...")
        self.scroll_into_view(self.CANCEL_BTN)
        self.click(self.CANCEL_BTN)

    def confirm_cancellation_action(self):
        print("DEBUG: Clicking Confirm Cancellation...")
        self.click(self.CONFIRM_CANCELLATION)

    def click_feedback_section(self):
        print("DEBUG: Clicking Feedback section...")
        locator = self.FEEDBACK_SECTION
        try:
            self.wait_for_clickable(locator).click()
        except Exception as e:
            print(f"DEBUG: Feedback section click failed. Attempting JS click. Error: {e}")
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2) # Wait for options to load

    def click_submitted_option(self):
        print("DEBUG: Clicking Submitted option...")
        self.scroll_into_view(self.SUBMITTED_OPTION)
        self.click(self.SUBMITTED_OPTION)

    def click_review_button(self):
        print("DEBUG: Clicking Review button...")
        self.click(self.REVIEW_BTN)

    def get_hire_status_text(self):
        print("DEBUG: Getting hire status text...")
        element = self.wait_for_element(self.HIRE_STATUS)
        return element.text.strip()

    def get_brightfit_score(self):
        print("DEBUG: Getting Brightfit score...")
        element = self.wait_for_element(self.BRIGHTFIT_SCORE)
        return element.text.strip()
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
