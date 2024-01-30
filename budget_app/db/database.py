from datetime import datetime
import sqlite3


class Database:
    def __init__(self, db_name="transactions.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                amount REAL,
                description TEXT,
                date TEXT,
                type TEXT,
                category TEXT,
                person TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.connection.commit()

    def transaction_in_database(self, amount, description, date, type) -> bool:
        select_query = '''
            SELECT * FROM transactions
            WHERE amount = ? AND
                description = ? AND
                date = ? AND
                type = ?
        '''
        self.cursor.execute(select_query, (amount,
                                           description,
                                           date,
                                           type))
        existing_record = self.cursor.fetchone()
        if existing_record:
            return True
        return False

    def add_transaction(self, amount, description, date, type, category, person):
        query = '''
            INSERT INTO transactions (amount,
                                      description,
                                      date,
                                      type,
                                      category,
                                      person)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (amount,
                                    description,
                                    date,
                                    type,
                                    category,
                                    person))
        self.connection.commit()

    def remove_transaction(self, amount, description, date, category, person):
        query = '''
            DELETE FROM transactions WHERE amount = ? AND
                                           description = ? AND
                                           date = ? AND
                                           category = ? AND
                                           person = ?
        '''
        self.cursor.execute(
            query, (amount, description, date, category, person))
        self.connection.commit()

    def update_transaction_category(self, amount, description, date, person, new_category):
        query = '''
            UPDATE transactions
            SET category = ?
            WHERE amount = ? AND
                description = ? AND
                date = ? AND
                person = ?
        '''
        self.cursor.execute(
            query, (new_category, amount, description, date, person))
        self.connection.commit()

    def get_all_transactions(self):
        query = 'SELECT * FROM transactions'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        transactions_data = []
        for row in rows:
            transaction_data = {
                'amount': row[1],
                'description': row[2],
                'date': row[3],
                'type': row[4],
                'category': row[5],
                'person': row[6]
            }
            transactions_data.append(transaction_data)

        return transactions_data

    def add_category(self, category):
        existing_categories = self.get_all_categories()
        if category in existing_categories:
            return

        query = '''
            INSERT INTO categories (name)
            VALUES (?)
        '''
        self.cursor.execute(query, (category,))
        self.connection.commit()

    def remove_category(self, category):
        query = 'DELETE FROM categories WHERE name = ?'
        self.cursor.execute(query, (category,))
        self.connection.commit()

    def update_category(self, old_name, new_name):
        query = 'UPDATE categories SET name = ? WHERE name = ?'
        self.cursor.execute(query, (new_name, old_name))
        self.connection.commit()

    def get_all_categories(self) -> list[str]:
        query = 'SELECT * FROM categories'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        categories = [row[1] for row in rows]
        return categories

    def close_connection(self):
        self.connection.close()
