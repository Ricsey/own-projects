from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from pages.cart_page import CartPage

class ProductPage:
    PICTURE = (By.CSS_SELECTOR, "img[alt='Vízipisztoly']")
    PRODUCT_NAME = (By.CSS_SELECTOR, "span[property='rdfs:label']")
    DESCRIPTION = (By.CSS_SELECTOR, "div.prodduct-description")
    BASKET_BUTTON = (By.CSS_SELECTOR, "button.btn-add-to-cart")
    
    def __init__(self, driver):
        self.driver: Chrome = driver
        self.wait = WebDriverWait(self.driver, 5)

    def open(self, url):
        self.driver.get(url)
        
    def get_image(self) -> WebElement:
        return self.driver.find_element(*self.PICTURE)
        
    def get_product_name(self) -> str:
        product_name_label: WebElement = self.driver.find_element(*self.PRODUCT_NAME)
        return product_name_label.text
        
    def get_title(self) -> str:
        return self.driver.title
    
    def get_description(self) -> str:
        description: WebElement = self.driver.find_element(*self.DESCRIPTION)
        print(description.text)
        return description.text

    def click_on_cart_button(self) -> CartPage:
        button: WebElement = self.driver.find_element(*self.BASKET_BUTTON)
        button.click()
        return CartPage(self.driver)
        