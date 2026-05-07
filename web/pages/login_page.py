from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object da tela de login do SauceDemo (`/`)."""

    URL = "/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        """Abre a tela de login. Retorna `self` para encadeamento."""
        self.open(self.URL)
        return self

    def login(self, username: str, password: str):
        """Preenche credenciais e submete o formulario."""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_message(self) -> str:
        """Texto da mensagem de erro exibida apos submissao invalida."""
        return self.text_of(self.ERROR_MESSAGE)
