from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def wait_for_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Element {locator} not found!")
            raise e

    def wait_for_clickable(self, locator):
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Element {locator} not clickable!")
            raise e

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        element.click()

    def type(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def scroll_into_view(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element

    def wait_for_visibility(self, locator, timeout=15):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            logging.error(f"Element {locator} not visible within {timeout}s!")
            raise e

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url
