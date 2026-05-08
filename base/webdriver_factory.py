from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class WebDriverFactory:
    """
    Base class for driver setup/teardown logic.
    """
    def __init__(self, browser_name="chrome"):
        self.browser_name = browser_name

    def get_driver(self, user_data_dir=None):
        if self.browser_name.lower() == "chrome":
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            
            if user_data_dir:
                options.add_argument(f"--user-data-dir={user_data_dir}")
                options.add_argument("--profile-directory=Default")
                # When using profile, we might need to disable automation flags to avoid being blocked
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        else:
            raise ValueError(f"Browser {self.browser_name} not supported.")
