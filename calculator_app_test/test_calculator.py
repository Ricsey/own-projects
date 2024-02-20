import pytest
from pywinauto import Desktop
from subprocess import Popen
import allure


@pytest.fixture(scope="module")
def app():
    try:
        Popen("calc.exe")
        app = Desktop(backend="uia")["Számológép"]
        yield app
        app.close()
    except Exception as error:
        print(error)
        pytest.fail("Failed to start the application.")

@allure.story("Calculator test")
@allure.title("Checking all numbers working")
@allure.severity(severity_level=allure.severity_level.CRITICAL)
@allure.description("Input every value and check the output result")
def test_nums_working(app):
    all_integers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    with allure.step("Input"):
        for i in all_integers:
            app.child_window(auto_id=f"num{i}Button", control_type="Button").click()
        app.child_window(auto_id="equalButton", control_type="Button").click()

    with allure.step("Output"):
        result_display_control = app.child_window(auto_id="CalculatorResults")
        result = result_display_control.window_text().replace("Megjelenített érték: ", "")

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
def test_addition(app):
    with allure.step("Input"):
        app.child_window(auto_id="num1Button", control_type="Button").click()
        app.child_window(auto_id="plusButton", control_type="Button").click()
        app.child_window(auto_id="num2Button", control_type="Button").click()
        app.child_window(auto_id="equalButton", control_type="Button").click()

    with allure.step("Output"):
        result_display_control = app.child_window(auto_id="CalculatorResults")
        result = result_display_control.window_text().replace("Megjelenített érték: ", "")

        assert 3 == int(result), "Addition operation result is incorrect!"

@allure.story("Calculator test")
@allure.title("Checking - functionality")
@allure.severity(severity_level=allure.severity_level.NORMAL)
@allure.description("Checking 4-3=1")
def test_division(app):
    with allure.step("Input"):
        app.child_window(auto_id="num4Button", control_type="Button").click()
        app.child_window(auto_id="minusButton", control_type="Button").click()
        app.child_window(auto_id="num3Button", control_type="Button").click()
        app.child_window(auto_id="equalButton", control_type="Button").click()

    with allure.step("Output"):
        result_display_control = app.child_window(auto_id="CalculatorResults")
        result = result_display_control.window_text().replace("Megjelenített érték: ", "")

        assert 1 == int(result), "Substraction operation result is incorrect!"

@allure.story("Calculator test")
@allure.title("Checking zero division")
@allure.severity(severity_level=allure.severity_level.CRITICAL)
@allure.description("Check zero division functionality and output")
def test_division_by_zero(app):
    with allure.step("Input"):
        app.child_window(auto_id="num4Button", control_type="Button").click()
        app.child_window(auto_id="divideButton", control_type="Button").click()
        app.child_window(auto_id="num0Button", control_type="Button").click()
        app.child_window(auto_id="equalButton", control_type="Button").click()

    with allure.step("Output"):
        result_display_control = app.child_window(auto_id="CalculatorResults")
        result = result_display_control.window_text().replace("Megjelenített érték: ", "")

        assert "Nullával nem lehet osztani" == result, "Division by zero error message is incorrect!"

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
