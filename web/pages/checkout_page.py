from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def finish(self):
        self.click(self.FINISH_BUTTON)

    def total_text(self) -> str:
        return self.text_of(self.SUMMARY_TOTAL)

    def confirmation_message(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)

    def error_message(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)
