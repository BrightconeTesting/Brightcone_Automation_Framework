from selenium import webdriver
<<<<<<< HEAD
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
=======
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
    def __init__(self, browser_name="chrome", headless=False):
        self.browser_name = browser_name.lower()
        self.headless = headless
        logger.debug(f"Initializing WebDriverFactory for: {self.browser_name} | Headless: {self.headless}")

    def get_driver(self):
        """
        Creates and returns a fresh WebDriver instance based on browser_name.
        """
        try:
            if self.browser_name == "chrome":
                logger.info(f"Setting up Chrome WebDriver (Headless={self.headless})...")
                options = webdriver.ChromeOptions()
                options.add_argument("--start-maximized")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                if self.headless:
                    options.add_argument("--headless=new")

                try:
                    service = ChromeService(ChromeDriverManager().install())
                except Exception as e:
                    logger.warning(f"WebDriver Manager failed for Chrome: {e}. Falling back to default.")
                    service = ChromeService()
                return webdriver.Chrome(service=service, options=options)
            
            elif self.browser_name == "firefox":
                logger.info(f"Setting up Firefox WebDriver (Headless={self.headless})...")
                options = webdriver.FirefoxOptions()
                # Adding arguments requested by user
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                if self.headless:
                    options.add_argument("-headless")

                try:
                    service = FirefoxService(GeckoDriverManager().install())
                except Exception as e:
                    logger.warning(f"WebDriver Manager failed for Firefox: {e}. Falling back to default.")
                    service = FirefoxService()
                driver = webdriver.Firefox(service=service, options=options)
                if not self.headless:
                    driver.maximize_window()
                return driver
            
            elif self.browser_name == "edge":
                logger.info(f"Setting up Edge WebDriver (Headless={self.headless})...")
                options = webdriver.EdgeOptions()
                options.add_argument("--start-maximized")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                if self.headless:
                    options.add_argument("--headless")

                try:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                except Exception as e:
                    logger.warning(f"WebDriver Manager failed for Edge: {e}. Falling back to Selenium Manager.")
                    service = EdgeService()
                return webdriver.Edge(service=service, options=options)
            
            else:
                msg = f"Unsupported browser: '{self.browser_name}'. Supported: chrome, firefox, edge"
                logger.error(msg)
                raise ValueError(msg)
        except Exception as global_e:
            logger.error(f"Global driver initialization failed: {global_e}")
            raise global_e
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
