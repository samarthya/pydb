# Import the created classes
from config import TableConfig
from db import DatabaseManager

# Initialize table configuration and database manager
config = TableConfig('config.json')
db_manager = DatabaseManager('example.db')

# Get table details from the configuration
table_name = config.get_table_name()
columns = config.get_columns()

# Create table
db_manager.create_table(table_name, columns)

# Insert data into the table
data_to_insert = [
    ('John', 'John@example.com'),
    ('Doe', 'Doe@example.com')
]

# db_manager.insert_data(table_name, data_to_insert)
db_manager.insert_data_unique(table_name, data_to_insert)

# Retrieve and display data from the table
rows = db_manager.fetch_data(table_name)
for row in rows:
    print(row)

# Close the connection
db_manager.close_connection()
