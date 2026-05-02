from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".inventory_item_name")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_loaded(self) -> bool:
        return self.is_visible(self.INVENTORY_LIST)

    def add_to_cart(self, product_name: str):
        button_id = "add-to-cart-" + product_name.lower().replace(" ", "-")
        self.click((By.ID, button_id))

    def remove_from_cart(self, product_name: str):
        button_id = "remove-" + product_name.lower().replace(" ", "-")
        self.click((By.ID, button_id))

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def sort_by(self, value: str):
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(value)

    def product_titles(self) -> list:
        return [el.text for el in self.driver.find_elements(*self.PRODUCT_TITLE)]

    def product_prices(self) -> list:
        return [float(el.text.replace("$", "")) for el in self.driver.find_elements(*self.PRODUCT_PRICE)]

    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
