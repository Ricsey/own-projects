from tests.base_test import product_page
from pages.product_page import ProductPage
import allure

class TestProductPage:
    
    @allure.description("Verify product name")
    @allure.story("---.---")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_name(self, product_page: ProductPage):
        with allure.step("Check product title"):
            assert product_page.get_product_name() == 'Vízipisztoly' , "Product name is not correct"
        
    @allure.description("Verify product description")
    @allure.story("---.---")
    @allure.severity(allure.severity_level.NORMAL)   
    def test_product_description(self, product_page: ProductPage):
        with allure.step("Check product description"):
            assert product_page.get_description() == 'A gyerekek és a felnőttek régen kedvelt, generációkon átívelő játékai közé tartozik a buborékfújó.\nEgy igazi nyári szórakozás már régóta mely még ma is garantálja a jókedvet és a mókát.\nEzek a buborékfújók úgy vannak kialakítva mintha igazi pisztolyok lennének így a gyerkőcök biztosan szeretni fogják ezeket a játékokat.' == 'A gyerekek és a felnőttek régen kedvelt, generációkon átívelő játékai közé tartozik a buborékfújó.\nEgy igazi nyári szórakozás már régóta mely még ma is garantálja a jókedvet és a mókát.\nEzek a buborékfújók úgy vannak kialakítva mintha igazi pisztolyok lennének így a gyerkőcök biztosan szeretni fogják ezeket a játékokat.'
        
    @allure.description("Verify page title")
    @allure.story("---.---")
    @allure.severity(allure.severity_level.CRITICAL)   
    def test_page_title(self, product_page: ProductPage):
        with allure.step("Check page title"):
            assert product_page.get_title() == 'Vízipisztoly | REGIO JÁTÉK Webáruház', "Title is not correct"

    @allure.description("Verify product image visibility")
    @allure.story("---.---")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_image_displayed(self, product_page: ProductPage):
        with allure.step("Check product image visibility"):
            assert product_page.get_image().is_displayed() , "Picture is not displayed"
        