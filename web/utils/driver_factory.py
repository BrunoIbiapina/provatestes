from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from config import Config


class DriverFactory:
    """Cria instancias de WebDriver com base na configuracao.

    Suporta Chrome e Firefox, modo visual ou headless. Usa
    `webdriver-manager` para baixar o driver compativel com o
    browser instalado, eliminando a necessidade de configurar
    PATH manualmente.
    """

    @staticmethod
    def create():
        """Cria e retorna o WebDriver configurado.

        Le `Config.BROWSER` (`chrome` ou `firefox`) e `Config.HEADLESS`.
        Para Chrome, aplica flags de estabilidade em CI
        (`--no-sandbox`, `--disable-dev-shm-usage`) e fixa resolucao 1920x1080.

        Raises:
            ValueError: se o browser configurado nao for suportado.
        """
        browser = Config.BROWSER.lower()
        if browser == "chrome":
            options = ChromeOptions()
            if Config.HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        if browser == "firefox":
            options = FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        raise ValueError(f"Browser nao suportado: {browser}")
