from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from config import Config


class DriverFactory:
    @staticmethod
    def create():
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
