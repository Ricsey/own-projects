import csv
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QComboBox, QItemDelegate, QAbstractItemView, QStyledItemDelegate
from resources.transactions_ui import Ui_Form
from db.database import Database
from db.models import Transaction, TransactionModel, TransactionFilterProxyModel


class IntToCurrencyFormatDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        return f"{int(float(value)):,}"


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, db: Database, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.db = db

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.db.get_all_categories())
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setCurrentText(value)

        editor.setObjectName("comboBox")
        editor.setStyleSheet(
            """
            #comboBox {
                background-color: #313a46;
                color: white;
                border: 1px solid;
                border-radius: 4px;
                padding-left: 5px;
            }

            #comboBox::drop-down{
                border: 0px;
            }

            #comboBox:on {
                border: 2px solid #c2dbfe;
            }

            #comboBox QListView {
                color: white;
                border: 1px solid rgba(0,0,0,10%);
                border-radius: 10px;
                padding: 5px;
                background-color: #313a46;
                outline: 0px;
            }

            /*
            #comboBox QListView::item {
                padding-left: 30px;
                background-color: rgba( 86, 101, 115, 0.5);
                border: 10px solid rgba(0,0,0,10%);
            }


            #comboBox QListView::item:hover {
                background-color: rgba( 86, 101, 115, 0.5);
            }

            #comboBox QListView::item:selected {
                background-color: rgba( 86, 101, 115, 0.5);
            }
            */

            QComboBox QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color:  rgba( 86, 101, 115, 0.5);
            }
            """
        )
        # logger.debug(
        #     f"Editor Cell ({index.row()}, {index.column()}) value changed to {value}")

    def setModelData(self, editor, model, index):
        value = editor.currentText()

        source_model = model.sourceModel()
        proxy_index = model.mapToSource(index).row()
        transaction = source_model.transactions[proxy_index]
        self.db.update_transaction_category(transaction.amount,
                                            transaction.description,
                                            transaction.date,
                                            transaction.person,
                                            value)
        # print("------------------")
        # print(f"updating {transaction}")
        # print(f"from {transaction.category}")
        # print(f"to {value}")
        # print("------------------")

        model.setData(index, value, Qt.EditRole)
        model.dataChanged.emit(index, index)

        # logger.debug(
        #     f"Model Cell ({index.row()}, {index.column()}) value changed to {value}")

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class EsztiTransactions(QWidget, Ui_Form):
    def __init__(self, db: Database) -> None:
        super().__init__()

        self.db = db

        self.setupUi(self)
        self.refresh_ui()

        self.model = TransactionModel(self.db)
        combobox_delegate = ComboBoxDelegate(self.db, self)
        int_to_currency_format = IntToCurrencyFormatDelegate()

        self.load_data(r'D:\Ricsi\budget\szamlatortenet_20231201_20231228.csv')

        self.proxy_model = TransactionFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(
            Transaction._fields().index("category"))
        self.proxy_model.dataChanged.connect(self.category_changed)
        self.proxy_model.dataChanged.connect(self.display_sum_of_category)
        self.proxy_model.dataChanged.connect(self.update_database)

        self.comboBox.currentTextChanged.connect(self.category_changed)
        self.comboBox.currentTextChanged.connect(self.display_sum_of_category)

        self.tableView.setModel(self.proxy_model)
        self.tableView.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableView.setItemDelegateForColumn(
            Transaction._fields().index("category"), combobox_delegate)
        self.tableView.setItemDelegateForColumn(
            Transaction._fields().index("amount"), int_to_currency_format)
        self.tableView.setShowGrid(False)
        self.tableView.resizeColumnsToContents()
        # self.tableView.clicked.connect(self.display_one_transcation)

        # "Dummy" transcations

    def refresh_ui(self):
        self.comboBox.clear()
        self.comboBox.addItems(self.categories)

    @property
    def categories(self):
        return self.db.get_all_categories()

    def category_changed(self):
        self.proxy_model.setFilterCategory(self.comboBox.currentText())

    def display_sum_of_category(self):
        model: TransactionModel = self.proxy_model.sourceModel()
        selected_category = self.comboBox.currentText()
        self.categoryname_label.setText(self.comboBox.currentText())
        sum_category = sum(float(t.amount)
                           for t in model.transactions)
        if selected_category != "Összes":
            sum_category = sum(
                float(t.amount) for t in model.transactions if t.category == selected_category)
        self.categorysum_label.setText(f"{int(sum_category):,} HUF")

    def load_data(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter="\t")

            next(csv_reader)  # jump header row

            for row in csv_reader:
                date = row[0]
                description = row[6]
                amount = int(row[7])
                type = row[2]

                transcation = Transaction(amount=amount,
                                          description=description,
                                          date=date,
                                          type=type,
                                          category="Egyéb",
                                          person="Eszti")
                if not self.db.transaction_in_database(transcation.amount,
                                                       transcation.description,
                                                       transcation.date,
                                                       transcation.type):
                    self.model.add_transaction(transcation)
            self.model.transactions

    def update_database(self, index):
        ...
