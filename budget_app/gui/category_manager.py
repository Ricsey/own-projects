from db.database import Database
from resources.category_manager_ui import Ui_Form
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QMessageBox, QDialog,
                               QVBoxLayout, QLineEdit, QLabel,
                               QDialogButtonBox, QListWidgetItem)


class CategoryEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kategória szerkesztése")

        layout = QVBoxLayout()

        self.label = QLabel("Írd át a kategória nevét:")
        self.edit_field = QLineEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.edit_field)

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_new_name(self):
        return self.edit_field.text()


class CategoryManager(QWidget):
    def __init__(self, db: Database):
        super().__init__()

        self.db = db

        self.default_categories = ['Egyéb', 'Bevétel']
        for default_category in self.default_categories:
            self.db.add_category(default_category)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_categories()

        self.ui.add_button.clicked.connect(self.add_category)
        self.ui.edit_button.clicked.connect(self.edit_category)
        self.ui.remove_button.clicked.connect(self.delete_category)

    def load_categories(self):

        self.categories = self.db.get_all_categories()
        for category in self.categories:
            item = QListWidgetItem(category)
            self.ui.category_list.addItem(item)

            if category in self.default_categories:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setForeground(Qt.gray)

    def add_category(self):
        new_category = self.ui.new_category_input.text()
        if not new_category:
            return

        if new_category not in self.categories:
            self.categories.append(new_category)
            self.db.add_category(new_category)
            self.ui.category_list.addItem(new_category)
            self.ui.new_category_input.clear()
        else:
            QMessageBox.warning(self, "Figyelem!",
                                "Ez a kategória már létezik!")

    def edit_category(self):
        selected_item = self.ui.category_list.currentItem()

        if selected_item.text() in self.default_categories:
            return

        if selected_item:
            editor = CategoryEditor(self)
            if not editor.exec():
                return

            new_name = editor.get_new_name()
            index = self.ui.category_list.currentRow()

            if new_name != selected_item.text():
                if new_name not in self.categories:
                    # Frissítsük az adatbázist az új névvel
                    old_name = selected_item.text()
                    self.db.update_category(old_name, new_name)

                    # Frissítsük a kategóriát az UI-ban és a listában
                    selected_item.setText(new_name)
                    self.categories[index] = new_name
                else:
                    QMessageBox.warning(self, "Figyelem!",
                                        "Ez a kategória már létezik!")

    def delete_category(self):
        selected_item = self.ui.category_list.currentItem()

        if selected_item.text() in self.default_categories:
            return

        if selected_item:
            selected_item_text = self.ui.category_list.currentItem().text()

            transactions = self.db.get_all_transactions()
            default_category = 'Egyéb'
            for transaction in transactions:
                if transaction.get('category') != selected_item_text:
                    continue
                self.db.update_transaction_category(transaction.get("amount"),
                                                    transaction.get(
                                                        "description"),
                                                    transaction.get("date"),
                                                    transaction.get("person"),
                                                    default_category)

            self.db.remove_category(selected_item_text)

            # del self.categories[index]
            self.ui.category_list.takeItem(self.ui.category_list.currentRow())
