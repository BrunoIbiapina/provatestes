import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.epic("SauceDemo")
@allure.feature("Checkout")
class TestCheckout:

    @allure.story("Checkout completo - fluxo E2E feliz")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_full_checkout(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")
        logged_in.go_to_cart()

        cart = CartPage(driver)
        assert cart.items_count() == 2
        cart.go_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_info("Bruno", "Ibiapina", "60000-000")
        assert "Total" in checkout.total_text()

        checkout.finish()
        assert "Thank you for your order" in checkout.confirmation_message()

    @allure.story("Checkout sem nome")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_missing_first_name(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.go_to_cart()

        CartPage(driver).go_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info("", "Ibiapina", "60000-000")

        assert "First Name is required" in checkout.error_message()

    @allure.story("Checkout sem CEP")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_missing_postal(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.go_to_cart()

        CartPage(driver).go_to_checkout()
        checkout = CheckoutPage(driver)
        checkout.fill_info("Bruno", "Ibiapina", "")

        assert "Postal Code is required" in checkout.error_message()
