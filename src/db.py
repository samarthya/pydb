"""Database Manager class """
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in columns:
            column_name = column["name"]
            column_type = column["type"]
            create_table_query += f"{column_name} {column_type}"

            if column.get("not_null"):
                create_table_query += " NOT NULL"

            if column.get("primary_key"):
                create_table_query += " PRIMARY KEY"

            if column.get("unique"):
                create_table_query += " UNIQUE"

            create_table_query += ","
        create_table_query = create_table_query.rstrip(",") + ")"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        insert_query = f"INSERT INTO {table_name} (name, email) VALUES (?, ?)"
        self.cursor.executemany(insert_query, data)
        self.conn.commit()

    def insert_data_unique(self, table_name, data):
        insert_query = f"INSERT OR REPLACE INTO {table_name} (name, email) VALUES (?, ?)"
        self.cursor.executemany(insert_query, data)
        self.conn.commit()

    def fetch_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
