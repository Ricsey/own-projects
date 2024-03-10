import pytest
from pages.product_page import ProductPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


    
@pytest.fixture(scope="module")
def product_page():
    options = Options()

    options.add_argument("start-maximized")
    options.add_argument("disable-extensions")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    main_page = ProductPage(driver)
    main_page.open("https://www.regiojatek.hu/termek-62956-vizipisztoly.html")
    yield main_page
    driver.quit() 