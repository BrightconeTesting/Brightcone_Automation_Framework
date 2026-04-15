from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class WebDriverFactory:
    """
    Base class for driver setup/teardown logic.
    """
    def __init__(self, browser_name="chrome"):
        self.browser_name = browser_name

    def get_driver(self):
        if self.browser_name.lower() == "chrome":
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        else:
            raise ValueError(f"Browser {self.browser_name} not supported.")
