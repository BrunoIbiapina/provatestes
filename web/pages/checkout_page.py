from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object das telas de checkout do SauceDemo.

    Cobre as 3 etapas: dados pessoais (step-one), resumo (step-two) e
    confirmacao (complete). A navegacao entre elas acontece via
    `fill_info()` (continue) e `finish()`.
    """

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        """Preenche os 3 campos da etapa 1 e clica em Continue."""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def finish(self):
        """Confirma a compra na etapa de resumo."""
        self.click(self.FINISH_BUTTON)

    def total_text(self) -> str:
        """Texto completo da linha de total no resumo."""
        return self.text_of(self.SUMMARY_TOTAL)

    def confirmation_message(self) -> str:
        """Mensagem de sucesso exibida na tela final."""
        return self.text_of(self.COMPLETE_HEADER)

    def error_message(self) -> str:
        """Texto da mensagem de erro de validacao da etapa de dados."""
        return self.text_of(self.ERROR_MESSAGE)
