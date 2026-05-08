from selenium.webdriver.common.by import By
from base.base_page import BasePage
import os
import time

try:
    import pyautogui
    import pyperclip
except ImportError:
    # We catch this later in the method to provide a clear error message
    pass

class DocumentsPage(BasePage):
    # Locators provided by user
    DOCUMENTS_MENU = (By.XPATH, "//span[text()='Documents']")
    FILE_UPLOAD_SECTION = (By.XPATH, "//h3[contains(text(), 'Choose a file')]")
    # Hidden file input usually near the upload section
    FILE_INPUT = (By.XPATH, "//input[@type='file']") 
    UPLOAD_BUTTON = (By.XPATH, "//button[contains(text(), 'Upload')]")
    
    # Category Locators
    ADMIN_CAT = (By.XPATH, "//span[text()='Admin (1)']")
    ENGINEERING_CAT = (By.XPATH, "//span[text()='Engineering (0)']")
    SUPPORT_CAT = (By.XPATH, "//span[text()='Support (0)']")
    
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
            "Support": self.SUPPORT_CAT
        }
        
        if category_name in mapping:
            self.click(mapping[category_name])
        else:
            raise ValueError(f"Category '{category_name}' not found in DocumentsPage mapping.")

    def upload_document(self, file_path):
        """
        Uses keyboard actions to handle the OS File Dialog.
        """
        print("DEBUG: Clicking on FILE_UPLOAD_SECTION to open OS dialog...")
        self.click(self.FILE_UPLOAD_SECTION)
        time.sleep(4) # Increased wait for OS dialog focus
        
        try:
            print(f"DEBUG: Copying path to clipboard and pasting: {file_path}")
            abs_path = os.path.abspath(file_path)
            pyperclip.copy(abs_path)
            
            # Simulate Paste and Enter
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('enter')
            
            # Wait for dialog to close
            time.sleep(2)
            print("[SUCCESS] OS-level File Upload handled via keyboard.")
        except Exception as e:
            print(f"[ERROR] OS File Dialog handling failed: {e}")
            raise

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
