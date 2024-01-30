from dataclasses import dataclass, fields
from datetime import datetime
from PySide6.QtCore import (QSortFilterProxyModel,
                            Qt,
                            QAbstractTableModel,
                            QModelIndex)

from db.database import Database


@dataclass
class Transaction:
    amount: int
    description: str
    date: str
    type: str
    category: str
    person: str

    # def __post_init__(self):
    #     db.create_tables()

    @staticmethod
    def _fields():
        return tuple(fs.name for fs in fields(Transaction))

    def __getitem__(self, index):
        return getattr(self, str(self._fields()[index]))

    def __setitem__(self, index, value):
        return setattr(self, str(self._fields()[index]), value)


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Person:
    id: int
    name: str


class TransactionAbstractModel(QAbstractTableModel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._transactions: list[Transaction] = []

    # def __getitem__(self, index: int) -> Transaction:
    #     if 0 <= index <= len(self._transactions):
    #         return self._transactions[index]
    #     raise IndexError("Transaction list index out of range")

    def data(self, index, role) -> str | None:
        if role == Qt.DisplayRole:
            value = self._transactions[index.row()][index.column()]
            # value = getattr(self._transactions[index.row()], str(
            #     Transaction._fields()[index.column()]))
            return str(value)
        elif role == Qt.EditRole:
            value = self._transactions[index.row()][index.column()]
            # value = getattr(self._transactions[index.row()], str(
            #     Transaction._fields()[index.column()]))
            return str(value)
        elif role == Qt.UserRole:
            return None
        else:
            return None
            raise NotImplementedError("Not implemented role!")

    def setData(self, index, value, role=Qt.EditRole) -> bool:
        self.dataChanged.emit(index, index)
        self.blockSignals(True)

        if role == Qt.EditRole:
            self._transactions[index.row()][index.column()] = value
            self.blockSignals(False)
            return True
        self.blockSignals(False)
        return False

    def rowCount(self, index) -> int:
        return len(self._transactions)

    def columnCount(self, index) -> int:
        return len(Transaction._fields())

    def flags(self, index):
        if index.column() == Transaction._fields().index("category"):
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsEnabled

    def add_transaction(self, transaction: Transaction):
        self.beginInsertRows(QModelIndex(), len(
            self._transactions), len(self._transactions))
        self._transactions.append(transaction)
        self.endInsertRows()

    def remove_transaction(self, row: int):
        if 0 <= row < len(self._transactions):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._transactions[row]
            self.endRemoveRows()


class TransactionModel(TransactionAbstractModel):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def get_data_by_category(self, category) -> list[Transaction]:
        raise NotImplementedError()

    @property
    def transactions(self):
        transactions = self.db.get_all_transactions()
        self._transactions = [
            Transaction(**t) for t in transactions]
        return self._transactions

    def add_transaction(self, transaction: Transaction):
        self.db.add_transaction(transaction.amount,
                                transaction.description,
                                transaction.date,
                                transaction.type,
                                transaction.category,
                                transaction.person)
        super().add_transaction(transaction)

    def remove_transaction(self, transaction_to_remove: Transaction):
        if not isinstance(transaction_to_remove, Transaction):
            raise TypeError(f"Transaction must be {Transaction} instead of {
                            type(transaction_to_remove)}")
        for idx, transaction in enumerate(self._transactions):
            if transaction != transaction_to_remove:
                continue

            # db.remove_transaction(transaction.amount,
            #                       transaction.description,
            #                       transaction.date,
            #                       transaction.category,
            #                       transaction.person)
            super().remove_transaction(idx)


class TransactionFilterProxyModel(QSortFilterProxyModel):
    """This is for filter out the displayed transactions by the selected
    category."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_category = "Összes"

    def setFilterCategory(self, category):
        self.filter_category = category
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        transaction = source_model.transactions[index.row()]
        if self.filter_category == "Összes":
            return True
        else:
            return transaction.category == self.filter_category
