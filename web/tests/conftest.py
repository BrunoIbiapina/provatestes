import sys
import os
from pathlib import Path
from datetime import datetime

import pytest
import allure

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import Config

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots"


@pytest.fixture
def driver():
    drv = DriverFactory.create()
    drv.implicitly_wait(Config.IMPLICIT_WAIT)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).load()


@pytest.fixture
def logged_in(driver, login_page):
    login_page.login(Config.STANDARD_USER, Config.PASSWORD)
    inventory = InventoryPage(driver)
    assert inventory.is_loaded(), "Login falhou - pagina de inventario nao carregou"
    return inventory


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is None:
            return

        SCREENSHOT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = SCREENSHOT_DIR / f"{item.name}_{timestamp}.png"
        drv.save_screenshot(str(filename))

        with open(filename, "rb") as f:
            allure.attach(f.read(), name=item.name, attachment_type=allure.attachment_type.PNG)
