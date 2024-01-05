import sqlite3
import unittest
from db import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.db_name = ":memory:"
        self.db_manager = DatabaseManager(self.db_name)

    def tearDown(self):
        # Close the database connection after each test
        self.db_manager.close_connection()

    def test_create_table(self):
        # Test creating a table
        table_name = "test_table"
        columns = [
            {"name": "id", "type": "INTEGER", "primary_key": True},
            {"name": "name", "type": "TEXT", "not_null": True},
            {"name": "email", "type": "TEXT", "unique": True}
        ]

        self.db_manager.create_table(table_name, columns)

        # Fetch table information from SQLite master table
        self.db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = self.db_manager.cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_insert_data(self):
        # Test inserting data into a table
        table_name = "test_table"
        columns = [
            {"name": "name", "type": "TEXT"},
            {"name": "email", "type": "TEXT"}
        ]
        data = [("John Doe", "john@example.com"), ("Alice", "alice@example.com")]

        self.db_manager.create_table(table_name, columns)
        self.db_manager.insert_data(table_name, data)

        # Fetch inserted data from the table
        result = self.db_manager.fetch_data(table_name)

        self.assertEqual(len(result), len(data))

    def test_insert_data_unique(self):
        # Test inserting unique data into a table
        table_name = "unique_table"
        columns = [
            {"name": "name", "type": "TEXT"},
            {"name": "email", "type": "TEXT", "unique": True}
        ]
        data = [("John Doe", "john@example.com"), ("Alice", "alice@example.com")]

        self.db_manager.create_table(table_name, columns)
        self.db_manager.insert_data_unique(table_name, data)
        self.db_manager.insert_data_unique(table_name, [("Alice1", "alice@example.com")])  # Update existing data

        # Fetch updated data from the table
        result = self.db_manager.fetch_data(table_name)

        self.assertEqual(len(result), len(data))
        self.assertIn(("Alice1", "alice@example.com"), result)

    def test_insert_data_unique_with_nounique(self):
        # Test inserting non-conflicting data into a table without unique constraints
        table_name = "non_unique_table"
        columns = [
            {"name": "name", "type": "TEXT"},
            {"name": "email", "type": "TEXT"}
        ]
        data = [("John Doe", "john@example.com"), ("Alice", "alice@example.com")]

        self.db_manager.create_table(table_name, columns)
        self.db_manager.insert_data_unique(table_name, data)
        self.db_manager.insert_data_unique(table_name, [("Bob", "bob@example.com")])  # Insert non-conflicting data

        # Fetch all data from the table
        result = self.db_manager.fetch_data(table_name)

        expected_data = data + [("Bob", "bob@example.com")]

        self.assertEqual(len(result), len(expected_data))
        self.assertCountEqual(result, expected_data)

if __name__ == '__main__':
    unittest.main()
