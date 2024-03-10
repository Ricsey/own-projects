import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class CartPage:
    BASKET_HEADER = (By.CSS_SELECTOR, 'div.cart-container h1')
    CART_SUBTOTAL = (By.CSS_SELECTOR, 'div.cart-subtotal>span.nowrap')
    
    def __init__(self, driver):
        self.driver: Chrome = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.wait.until(EC.text_to_be_present_in_element(self.BASKET_HEADER, 'Kosár tartalma ('))

    def get_page_title(self) -> str:
        return self.driver.title
    
    def get_subtotal_price(self) -> int:
        subtotal_label: WebElement = self.driver.find_element(*self.CART_SUBTOTAL)
        subtotal_price = int(subtotal_label.text.removesuffix(" Ft").replace(" ", ""))
        return subtotal_price
        