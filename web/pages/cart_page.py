from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def items(self) -> list:
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAME)]

    def items_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
