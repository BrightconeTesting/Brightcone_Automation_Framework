from selenium.webdriver.common.by import By
from base.base_page import BasePage
import os
import time


class DocumentsPage(BasePage):
    # Locators provided by user
    DOCUMENTS_MENU = (By.XPATH, "//span[text()='Documents']")
    FILE_UPLOAD_SECTION = (By.XPATH, "//h3[contains(text(), 'Choose a file')]")
    # Replaced pyautogui-based locator with direct file input for Selenium send_keys
    FILE_INPUT = (By.XPATH, "//div[contains(@class,'cursor-pointer')]//input[@type='file']") 
    UPLOAD_BUTTON = (By.XPATH, "//button[contains(text(), 'Upload')]")
    
    # Category Locators
    ADMIN_CAT = (By.XPATH, "(//span[contains(text(),'Admin')])[1]")
    ENGINEERING_CAT = (By.XPATH, "//span[text()='Engineering (0)']")
    SUPPORT_CAT = (By.XPATH, "//span[text()='Support (0)']")
    GENERAL_CAT = (By.XPATH, "//span[contains(text(), 'General')]")
    
    # Navigation/Dashboard
    DASHBOARD_ICON = (By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/aside/div[2]/nav/a[1]')
    NOTIFICATION_ICON = (By.XPATH, '//*[@id="main-content"]/div/div[1]/div[1]/div[2]/div/button/svg')
    NOTIFICATION_POPUP = (By.XPATH, '//*[@id="root"]/div[2]/div/div/span')

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_documents(self):
        print("DEBUG: Navigating to Documents page...")
        self.click(self.DOCUMENTS_MENU)

    def select_category(self, category_name):
        """
        Dynamically selects the category: 'Admin', 'Engineering', or 'Support'.
        """
        print(f"DEBUG: Selecting category: {category_name}")
        mapping = {
            "Admin": self.ADMIN_CAT,
            "Engineering": self.ENGINEERING_CAT,
            "Support": self.SUPPORT_CAT,
            "General": self.GENERAL_CAT
        }
        
        if category_name in mapping:
            self.click(mapping[category_name])
        else:
            raise ValueError(f"Category '{category_name}' not found in DocumentsPage mapping.")

    def upload_document(self, file_path):
        """
        Uploads a document using Selenium's send_keys method for better stability and headless support.
        """
        print(f"DEBUG: Uploading document via standard Selenium send_keys: {file_path}")
        abs_path = os.path.abspath(file_path)
        
        # Locate the hidden file input and send the absolute path
        file_input = self.wait_for_element(self.FILE_INPUT)
        file_input.send_keys(abs_path)
        
        print(f"[SUCCESS] Document path sent successfully to {self.FILE_INPUT[1]}")

    def click_upload_button(self):
        """
        Clicks the final Upload button.
        """
        print("DEBUG: Clicking final Upload button...")
        self.click(self.UPLOAD_BUTTON)

    def find_document_and_scroll(self, file_name):
        """
        Robust method to find a document, scroll to it, and handle potential stale elements.
        """
        base_name = file_name.split('.')[0]
        locator = (By.XPATH, f"//*[contains(text(), '{base_name}') or contains(@title, '{base_name}')]")
        
        print(f"DEBUG: Scrolling to and finding document: {file_name}")
        try:
            # First wait for presence, then scroll
            self.scroll_into_view(locator)
            # Then wait for visibility
            return self.wait_for_visibility(locator, timeout=10)
        except Exception as e:
            print(f"DEBUG: Initial find failed, retrying once for: {file_name}")
            time.sleep(2)
            self.scroll_into_view(locator)
            return self.wait_for_visibility(locator, timeout=10)
    def get_notification_text(self):
        """
        Captures the text from the notification popup.
        """
        print("DEBUG: Waiting for notification popup text...")
        element = self.wait_for_visibility(self.NOTIFICATION_POPUP, timeout=10)
        return element.text.strip()
