import json
import sqlite3

# Read the table configuration from JSON file
with open('config.json', encoding='utf-8') as config_file:
    table_config = json.load(config_file)

# Extract table details from the configuration
table_name = table_config["table_name"]
columns = table_config["columns"]

# Connect to an SQLite database or create it if it doesn't exist
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create the table based on the configuration
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

for column in columns:
    column_name = column["name"]
    column_type = column["type"]
    create_table_query += f"{column_name} {column_type}"

    if column.get("not_null"):
        create_table_query += " NOT NULL"

    if column.get("primary_key"):
        create_table_query += " PRIMARY KEY"

    create_table_query += ","

create_table_query = create_table_query.rstrip(",") + ")"
cursor.execute(create_table_query)

# Insert data into the table
data_to_insert = [
    ('John', 'John@example.com'),
    ('Doe', 'Doe@example.com')
]
insert_query = f"INSERT INTO {table_name} (name, email) VALUES (?, ?)"
cursor.executemany(insert_query, data_to_insert)
conn.commit()

# Retrieve and display data from the table
cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
