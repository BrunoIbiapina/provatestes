from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object da tela de carrinho (`/cart.html`)."""

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def items(self) -> list:
        """Lista de nomes dos produtos no carrinho."""
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAME)]

    def items_count(self) -> int:
        """Quantidade de itens no carrinho."""
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def go_to_checkout(self):
        """Inicia o fluxo de checkout."""
        self.click(self.CHECKOUT_BUTTON)
