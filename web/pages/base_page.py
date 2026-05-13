from selenium.webdriver.common.keys import Keys
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
        """Espera o elemento ser clicavel e clica via JS.

        Usar `execute_script("arguments[0].click()")` em vez do click do
        W3C evita flakiness em `headless=new` no Linux, onde o click
        nativo dispara em coordenadas de elementos que o React acabou
        de re-renderizar (segundo click de uma sequencia "passa" sem
        rodar o handler).
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text: str):
        """Espera o elemento, limpa o conteudo e digita `text`.

        Usar Ctrl+A / Delete em vez de `element.clear()` evita race com
        re-renderizacao em `headless=new` no Linux: o clear() dispara
        input/blur que re-renderiza o campo no meio do send_keys
        seguinte, fazendo caracteres se perderem silenciosamente.
        """
        element = self.find(locator)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        if text:
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
