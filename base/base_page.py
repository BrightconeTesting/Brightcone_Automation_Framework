from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

<<<<<<< HEAD
    def wait_for_element(self, locator, timeout=20):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        except Exception as e:
            try:
                self.driver.save_screenshot("debug_failure.png")
            except Exception:
                pass
=======
    def wait_for_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except (TimeoutException, NoSuchElementException) as e:
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
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

<<<<<<< HEAD
=======
    def wait_for_all_elements_visible(self, locator, timeout=15):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException as e:
            logging.error(f"Elements {locator} not visible within {timeout}s!")
            raise e

>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url
<<<<<<< HEAD
=======

    def open_url(self, url):
        self.driver.get(url)
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
