from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import Config


class DriverFactory:
    """Cria instancias de WebDriver com base na configuracao.

    Suporta Chrome e Firefox, modo visual ou headless. Delega a
    resolucao do driver ao Selenium Manager (embutido no Selenium
    4.6+), que baixa automaticamente a versao compativel com o
    browser instalado.
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
            return webdriver.Chrome(options=options)
        if browser == "firefox":
            options = FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument("--headless")
            return webdriver.Firefox(options=options)
        raise ValueError(f"Browser nao suportado: {browser}")
