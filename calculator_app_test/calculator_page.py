class CalculatorPage:
    def __init__(self, app) -> None:
        self.app = app
    
    def input_number(self, number: int) -> None:
        self.app.child_window(auto_id=f"num{number}Button", control_type="Button").click()
        
    def input_operation(self, operation: str) -> None:
        self.app.child_window(auto_id=f"{operation}Button", control_type="Button").click()
        
    def click_equal(self) -> None:
        self.app.child_window(auto_id=f"equalButton", control_type="Button").click()
        
    def get_result(self) -> None:
        result_display_control = self.app.child_window(auto_id="CalculatorResults")
        return result_display_control.window_text().replace("Megjelenített érték: ", "")