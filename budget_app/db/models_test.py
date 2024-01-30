import unittest
from datetime import datetime
from models import Transaction, TransactionModel, TransactionFilterProxyModel
from database import Database


class TestTransactionModel(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')
        self.db.create_tables()
        self.model = TransactionModel()

    def tearDown(self):
        self.model = None
        self.db.close_connection()
        self.db = None

    def test_add_transaction(self):
        initial_count = len(self.model.transactions)
        transaction = Transaction(amount=100.0,
                                  description="Test",
                                  date=datetime.now(),
                                  category="Test Category",
                                  person="Test Person")
        self.model.add_transaction(transaction)
        new_count = len(self.model.transactions)
        self.assertEqual(new_count, initial_count + 1)

    def test_remove_transaction(self):
        transaction = Transaction(amount=100.0,
                                  description="Test",
                                  date=datetime.now(),
                                  category="Test Category",
                                  person="Test Person")
        self.model.add_transaction(transaction)
        initial_count = len(self.model.transactions)
        self.model.remove_transaction(transaction)
        new_count = len(self.model.transactions)
        self.assertEqual(new_count, initial_count - 1)


class TestTransactionFilterProxyModel(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.create_tables()
        self.model = TransactionModel()
        self.proxy_model = TransactionFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

    def tearDown(self):
        self.model = None
        self.proxy_model = None
        self.db.close_connection()
        self.db = None

    def test_filter_by_category(self):
        # Set up - add transactions to the model
        transaction1 = Transaction(amount=100.0,
                                   description="Test1",
                                   date=datetime.now(),
                                   category="Category1",
                                   person="Person1")
        transaction2 = Transaction(amount=200.0,
                                   description="Test2",
                                   date=datetime.now(),
                                   category="Category2",
                                   person="Person2")
        self.model.add_transaction(transaction1)
        self.model.add_transaction(transaction2)

        # Test filtering by a specific category
        self.proxy_model.setFilterCategory("Category1")
        self.assertEqual(self.proxy_model.rowCount(), 1)

        self.proxy_model.setFilterCategory("Category2")
        self.assertEqual(self.proxy_model.rowCount(), 1)

        # Test filtering with "Összes" (All) category
        self.proxy_model.setFilterCategory("Összes")
        self.assertEqual(self.proxy_model.rowCount(), 2)


if __name__ == '__main__':
    unittest.main()
