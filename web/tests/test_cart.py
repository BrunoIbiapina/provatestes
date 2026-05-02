import allure
import pytest

from pages.cart_page import CartPage


@allure.epic("SauceDemo")
@allure.feature("Cart")
class TestCart:

    @allure.story("Adicionar produto ao carrinho")
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_single_product(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")
        assert logged_in.cart_count() == 1

    @allure.story("Adicionar varios produtos")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_products(self, logged_in):
        produtos = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        for p in produtos:
            logged_in.add_to_cart(p)
        assert logged_in.cart_count() == len(produtos)

    @allure.story("Remover produto do carrinho")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_product(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.remove_from_cart("Sauce Labs Backpack")
        assert logged_in.cart_count() == 0

    @allure.story("Carrinho preserva itens ao navegar")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_persists(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")
        logged_in.go_to_cart()

        cart = CartPage(driver)
        assert cart.items_count() == 2
        assert "Sauce Labs Backpack" in cart.items()

    @allure.story("Ordenar produtos por preco crescente")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_sort_price_low_high(self, logged_in):
        logged_in.sort_by("lohi")
        prices = logged_in.product_prices()
        assert prices == sorted(prices)
