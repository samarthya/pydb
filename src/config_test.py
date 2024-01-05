"""Unit test for the TableConfig"""
import unittest
import json
import os
from config import TableConfig

class TestTableConfig(unittest.TestCase):
    """TestTableConfig class"""
    def setUp(self):
        # Create a temporary config file for testing
        self.config_file = "test_config.json"

        self.config_data = {
            "table_name": "users",
            "columns": ["id", "name", "email"],
            "primary_key": "id"
        }

        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(self.config_data, file, indent=4)

        # Initialize TableConfig instance for testing
        self.table_config = TableConfig(self.config_file)

    def tearDown(self):
        # Remove the temporary config file after testing
        os.remove(self.config_file)

    def test_get_table_name(self):
        self.assertEqual(self.table_config.get_table_name(), "users")

    def test_get_columns(self):
        self.assertEqual(self.table_config.get_columns(), ["id", "name", "email"])

    def test_get_existing_value(self):
        self.assertEqual(self.table_config.get("primary_key"), "id")

    def test_get_non_existing_value(self):
        self.assertEqual(self.table_config.get("non_existing_key"), "")

    def test_set_and_get_value(self):
        self.table_config.set("new_key", "new_value")
        self.assertEqual(self.table_config.get("new_key"), "new_value")

    def test_overwrite(self):
        new_config_data = {
            "table_name": "posts",
            "columns": ["id", "name", "email"],
            "primary_key": "id"
        }
        self.table_config.set("table_name", "posts")
        self.table_config.overwrite()

        # Read the modified config file and verify changes
        with open(self.config_file, encoding='utf-8') as file:
            updated_data = json.load(file)

        print(f"{updated_data} : {new_config_data}")
        self.assertEqual(updated_data, new_config_data)

if __name__ == '__main__':
    unittest.main()
