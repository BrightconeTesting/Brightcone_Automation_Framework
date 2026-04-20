from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.logger_config import logger

class WebDriverFactory:
    """
    Reusable Factory for Selenium WebDriver. 
    Supports Chrome, Firefox, and Edge with automatic driver management.
    """
    def __init__(self, browser_name="chrome"):
        self.browser_name = browser_name.lower()
        logger.debug(f"Initializing WebDriverFactory for: {self.browser_name}")

    def get_driver(self):
        """
        Creates and returns a fresh WebDriver instance based on browser_name.
        """
        try:
            if self.browser_name == "chrome":
                logger.info("Setting up Chrome WebDriver...")
                options = webdriver.ChromeOptions()
                options.add_argument("--start-maximized")
                try:
                    service = ChromeService(ChromeDriverManager().install())
                except Exception as e:
                    logger.warning(f"WebDriver Manager failed for Chrome: {e}. Falling back to default.")
                    service = ChromeService()
                return webdriver.Chrome(service=service, options=options)
            
            elif self.browser_name == "firefox":
                logger.info("Setting up Firefox WebDriver...")
                options = webdriver.FirefoxOptions()
                try:
                    service = FirefoxService(GeckoDriverManager().install())
                except Exception as e:
                    logger.warning(f"WebDriver Manager failed for Firefox: {e}. Falling back to default.")
                    service = FirefoxService()
                driver = webdriver.Firefox(service=service, options=options)
                driver.maximize_window()
                return driver
            
            elif self.browser_name == "edge":
                logger.info("Setting up Edge WebDriver...")
                options = webdriver.EdgeOptions()
                options.add_argument("--start-maximized")
                try:
                    # Attempt WDM first
                    service = EdgeService(EdgeChromiumDriverManager().install())
                except Exception as e:
                    logger.warning(f"WebDriver Manager failed for Edge: {e}. Falling back to Selenium Manager.")
                    # Fallback allows Selenium 4's built-in manager to try and find/download the driver
                    service = EdgeService()
                return webdriver.Edge(service=service, options=options)
            
            else:
                msg = f"Unsupported browser: '{self.browser_name}'. Supported: chrome, firefox, edge"
                logger.error(msg)
                raise ValueError(msg)
        except Exception as global_e:
            logger.error(f"Global driver initialization failed: {global_e}")
            raise global_e
