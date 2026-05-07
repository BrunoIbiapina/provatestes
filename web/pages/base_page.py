from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Config


class BasePage:
    """Classe base de todos os Page Objects.

    Encapsula primitivas do Selenium com espera explicita embutida
    (WebDriverWait + expected_conditions). Subclasses devem definir
    locators como tuplas `(By, value)` e expor metodos de negocio
    que delegam para `find`, `click`, `type`, etc.

    Nenhuma subclasse deve usar `time.sleep()` ou waits implicitos
    alem do configurado em `Config.IMPLICIT_WAIT`.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def open(self, url: str = ""):
        """Navega para `BASE_URL + url`."""
        self.driver.get(f"{Config.BASE_URL}{url}")

    def find(self, locator):
        """Espera o elemento estar presente no DOM e retorna."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Espera o elemento ser clicavel e clica."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        """Espera o elemento, limpa o conteudo e digita `text`."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        """Retorna o texto visivel do elemento."""
        return self.find(locator).text

    def is_visible(self, locator) -> bool:
        """True se o elemento ficar visivel dentro do timeout, False caso contrario."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def current_url(self) -> str:
        """URL atual do browser."""
        return self.driver.current_url
