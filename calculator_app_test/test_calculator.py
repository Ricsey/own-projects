import pytest
import allure
from pywinauto import Desktop
from subprocess import Popen
from calculator_page import CalculatorPage

@pytest.fixture(scope="module")
def calculator_page():
    try:
        Popen("calc.exe")
        app = Desktop(backend="uia")["Számológép"]
        yield CalculatorPage(app)
        app.close()
    except Exception as error:
        print(error)
        pytest.fail("Failed to start the application.")

@allure.story("Calculator test")
@allure.title("Checking all numbers working")
@allure.severity(severity_level=allure.severity_level.CRITICAL)
@allure.description("Input every value and check the output result")
def test_nums_working(calculator_page):
    all_integers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    with allure.step("Input"):
        for i in all_integers:
            calculator_page.input_number(i)
        calculator_page.click_equal()

    with allure.step("Output"):
        result = calculator_page.get_result()

        if result != "1234567890":
            missing_elements = set()
            for i in all_integers:
                if str(i) not in result:
                    missing_elements.add(i)
            if missing_elements:
                assert False, f"The following numbers are not working as expected: {', '.join(missing_elements)}"

@allure.story("Calculator test")
@allure.title("Checking + functionality")
@allure.severity(severity_level=allure.severity_level.NORMAL)
@allure.description("Check if 1+2=3")
def test_addition(calculator_page):
    with allure.step("Input"):
        calculator_page.input_number(1)
        calculator_page.input_operation("plus")
        calculator_page.input_number(2)
        calculator_page.click_equal()

    with allure.step("Output"):
        result = calculator_page.get_result()

        assert 3 == int(result), "Addition operation result is incorrect!"

@allure.story("Calculator test")
@allure.title("Checking - functionality")
@allure.severity(severity_level=allure.severity_level.NORMAL)
@allure.description("Checking 4-3=1")
def test_division(calculator_page):
    with allure.step("Input"):
        calculator_page.input_number(4)
        calculator_page.input_operation("minus")
        calculator_page.input_number(3)
        calculator_page.click_equal()

    with allure.step("Output"):
        result = calculator_page.get_result()
        raise Exception("Cannot read result")
        assert 1 == int(result), "Substraction operation result is incorrect!"

@allure.story("Calculator test")
@allure.title("Checking zero division")
@allure.severity(severity_level=allure.severity_level.CRITICAL)
@allure.description("Check zero division functionality and output")
def test_division_by_zero(calculator_page):
    with allure.step("Input"):
        calculator_page.input_number(4)
        calculator_page.input_operation("divide")
        calculator_page.input_number(0)
        calculator_page.click_equal()

    with allure.step("Output"):
        result = calculator_page.get_result()

        assert "Nullával lehet osztani" == result, "Division by zero error message is incorrect!"

# TODO
# szorzas
# muveletek sorrendiseg ellenorzese
# aritmetikai muveletek racionalis szamokkal (float)
# negativ szamok ellenorzese:
#   inputban mukodik-e
#   negativ szamokkal muveletek (+,-,*,/,sqrt)
# C, CE funkciok mukodese
# Memoria funkciok:
#   M+
#   M-
#   MS
#   MR
#   MC
# sqrt es ^2
# 1/x funkcio
# %
# backspace gomb
# "Előzmények" ellenőrzése
#   megjelennek-e az új eredmények
#   rákattintva visszahozza-e az akkori műveletet
#   egyik elemére jobb egér -> Törlésre törlődik-e

# tesztesetek kibovitese billentyu nyomassal


if __name__ == "__main__":
    pytest.main()
