from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object da tela de catalogo (`/inventory.html`).

    Expoe acoes de adicionar/remover produto, ordenacao, navegacao
    para o carrinho e logout via menu.
    """

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
        """True se a lista de produtos esta visivel (autenticacao OK)."""
        return self.is_visible(self.INVENTORY_LIST)

    def add_to_cart(self, product_name: str):
        """Clica em 'Add to cart' do produto. Resolve o ID a partir do nome."""
        button_id = "add-to-cart-" + product_name.lower().replace(" ", "-")
        self.click((By.ID, button_id))

    def remove_from_cart(self, product_name: str):
        """Clica em 'Remove' do produto. Resolve o ID a partir do nome."""
        button_id = "remove-" + product_name.lower().replace(" ", "-")
        self.click((By.ID, button_id))

    def cart_count(self) -> int:
        """Quantidade exibida no badge do carrinho (0 se nao houver badge)."""
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def go_to_cart(self):
        """Navega para a tela do carrinho."""
        self.click(self.CART_LINK)

    def sort_by(self, value: str):
        """Aplica ordenacao no dropdown (ex.: `lohi`, `hilo`, `az`, `za`)."""
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(value)

    def product_titles(self) -> list:
        """Lista de titulos dos produtos visiveis."""
        return [el.text for el in self.driver.find_elements(*self.PRODUCT_TITLE)]

    def product_prices(self) -> list:
        """Lista de precos como floats, na ordem que aparecem na tela."""
        return [float(el.text.replace("$", "")) for el in self.driver.find_elements(*self.PRODUCT_PRICE)]

    def logout(self):
        """Abre o menu lateral e desloga."""
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
