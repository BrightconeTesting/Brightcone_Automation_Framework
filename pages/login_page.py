from selenium.webdriver.common.by import By
from base.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    CONTINUE_BUTTON = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        super().__init__(driver)
<<<<<<< HEAD
        self.url = "https://app.brightcone.ai/login"
=======
        self.url = "https://staging-app.brightcone.ai"
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201

    def open(self):
        self.driver.get(self.url)

    def enter_email(self, email):
        self.type(self.EMAIL_INPUT, email)

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)

    def login_upto_otp(self, email):
        self.open()
        self.enter_email(email)
        self.click_continue()
