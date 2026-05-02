import allure
import pytest

from pages.inventory_page import InventoryPage
from config import Config


@allure.epic("SauceDemo")
@allure.feature("Login")
class TestLogin:

    @allure.story("Login com usuario padrao")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_standard_user_login(self, driver, login_page):
        login_page.login(Config.STANDARD_USER, Config.PASSWORD)
        assert InventoryPage(driver).is_loaded()
        assert "inventory" in driver.current_url

    @allure.story("Login bloqueado")
    @pytest.mark.negative
    @pytest.mark.login
    def test_locked_out_user(self, login_page):
        login_page.login(Config.LOCKED_USER, Config.PASSWORD)
        assert "locked out" in login_page.error_message().lower()

    @allure.story("Login com senha incorreta")
    @pytest.mark.negative
    @pytest.mark.login
    def test_wrong_password(self, login_page):
        login_page.login(Config.STANDARD_USER, "senha_errada")
        assert "do not match" in login_page.error_message().lower()

    @allure.story("Login com campos vazios")
    @pytest.mark.negative
    @pytest.mark.login
    def test_empty_fields(self, login_page):
        login_page.login("", "")
        assert "username is required" in login_page.error_message().lower()

    @allure.story("Logout")
    @pytest.mark.regression
    @pytest.mark.login
    def test_logout(self, logged_in, driver):
        logged_in.logout()
        assert driver.current_url.rstrip("/").endswith("saucedemo.com")
