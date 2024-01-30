import unittest
from datetime import datetime
from database import Database


class TestTransactionModel(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')
        self.db.create_tables()

    def tearDown(self):
        self.db.close_connection()

    def test_add_transaction(self):
        initial_count = len(self.db.get_all_transactions())

        amount = 100.0
        description = "Test"
        date = datetime.now().strftime('%Y.%m.%d')
        category = "Test Category"
        person = "Test Person"
        self.db.add_transaction(amount, description, date, category, person)

        updated_count = len(self.db.get_all_transactions())
        self.assertEqual(updated_count, initial_count + 1)

    def test_remove_transaction(self):
        amount = 100.0
        description = "Test"
        date = datetime.now().strftime('%Y.%m.%d')
        category = "Test Category"
        person = "Test Person"

        self.db.add_transaction(amount, description, date, category, person)
        initial_count = len(self.db.get_all_transactions())
        self.db.remove_transaction(amount, description, date, category, person)
        new_count = len(self.db.get_all_transactions())
        self.assertEqual(new_count, initial_count - 1)

    def test_add_category(self):
        test_category = "Test Category"

        initial_count = len(self.db.get_all_categories())
        self.db.add_category(test_category)
        new_count = len(self.db.get_all_categories())
        self.assertEqual(new_count, initial_count + 1)

    def test_remove_category(self):
        test_category = "Test Category"

        self.db.add_category(test_category)
        initial_count = len(self.db.get_all_categories())
        self.db.remove_category(test_category)
        new_count = len(self.db.get_all_categories())
        self.assertEqual(new_count, initial_count - 1)


if __name__ == '__main__':
    unittest.main()
