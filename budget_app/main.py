from PySide6.QtWidgets import QApplication, QMainWindow
from gui.summary_dashboard import SummaryDashboard
from resources.mainwindow_ui import Ui_MainWindow
from gui.category_manager import CategoryManager
from gui.eszti_transactions import EsztiTransactions
from db.database import Database


class MyApp(QMainWindow):
    def __init__(self, db: Database):
        super().__init__()

        self.db = db

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.centralwidget.setMinimumSize(800, 600)
        self.ui.stackedWidget.setMinimumSize(800, 1000)

        category_manager_widget = CategoryManager(self.db)
        eszti_transactions_widget = EsztiTransactions(self.db)
        summary_dashboard_widget = SummaryDashboard(self.db)

        self.ui.stackedWidget.addWidget(eszti_transactions_widget)
        self.ui.stackedWidget.addWidget(category_manager_widget)
        self.ui.stackedWidget.addWidget(summary_dashboard_widget)

        self.ui.summary_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(summary_dashboard_widget))

        self.ui.category_manager_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(category_manager_widget))

        self.ui.eszti_transactions_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(eszti_transactions_widget))

        # Refresh every widget on "tab" change
        self.ui.stackedWidget.currentChanged.connect(
            self.update_current_widget)

    def update_current_widget(self, index):
        current_widget = self.ui.stackedWidget.widget(index)
        if isinstance(current_widget, EsztiTransactions):
            current_widget.refresh_ui()


def main():
    app = QApplication([])
    db = Database()
    db.create_tables()
    window = MyApp(db)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
