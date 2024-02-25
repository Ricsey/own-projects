from tests.base_test import product_page
from pages.product_page import ProductPage
from pages.cart_page import CartPage
import allure
import pytest


class TestCartPage:

    @pytest.fixture(scope="module")
    def cart_page(self, product_page: ProductPage):
        return product_page.click_on_cart_button()

    @allure.description("Verify cart page title")
    @allure.story("*--.---")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test_basket_page_title(self, cart_page: CartPage):
        with allure.step("Check cart page title"):
            assert cart_page.get_page_title() == 'Minden nap gyereknap! | REGIO JÁTÉK Webáruház'

    @allure.description("Verify subtotal price 1 product")
    @allure.story("*--.---")
    @allure.severity(allure.severity_level.CRITICAL)            
    def test_subtotal_price(self, cart_page: CartPage):
        with allure.step("Check subtotal price"):
            assert cart_page.get_subtotal_price() == 3995