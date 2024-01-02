# Import the created classes
from config import TableConfig
from db import DatabaseManager
import argparse

def display_records(rows):
    if not rows:
        print("No records found.")
    else:
        print("Records:")
        for row in rows:
            print(row)

def main():
    parser = argparse.ArgumentParser(description='Database Operations')
    parser.add_argument('--action', choices=['menu', 'add', 'delete', 'list'], default='menu', help='Choose action mode: menu, add, delete, list')
    parser.add_argument('--name', help='Name for adding a record')
    parser.add_argument('--email', help='Email for adding/deleting a record')
    parser.add_argument('--all', action='store_true', help='Delete all records')
    args = parser.parse_args()


    config = TableConfig('config.json')
    db_manager = DatabaseManager('example.db')
    table_name = config.get_table_name()

    if args.action == 'menu':
        while True:
            print("\nMenu:")
            print("1. Add a record")
            print("2. Delete a record")
            print("3. List all records")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                name = input("Enter name: ")
                email = input("Enter email: ")
                db_manager.insert_data_unique(table_name, [(name, email)])
                print("Record added successfully!")

            elif choice == '2':
                email_to_delete = input("Enter email to delete: ")
                delete_query = f"DELETE FROM {table_name} WHERE email = ?"
                db_manager.cursor.execute(delete_query, (email_to_delete,))
                if db_manager.cursor.rowcount == 0:
                    print("Record not found.")
                else:
                    db_manager.conn.commit()
                    print("Record deleted successfully!")

            elif choice == '3':
                rows = db_manager.fetch_data(table_name)
                display_records(rows)

            elif choice == '4':
                break

            else:
                print("Invalid choice. Please enter a valid option.")

    elif args.action == 'add':
        if args.name and args.email:
            db_manager.insert_data_unique(table_name, [(args.name, args.email)])
            print("Record added successfully!")
        else:
            print("Please provide both name and email.")

    elif args.action == 'delete':
        if args.all:
            delete_query = f"DELETE FROM {table_name}"
            db_manager.cursor.execute(delete_query)
            db_manager.conn.commit()
            print("All records deleted successfully!")
        elif args.email:
            delete_query = f"DELETE FROM {table_name} WHERE email = ?"
            db_manager.cursor.execute(delete_query, (args.email,))
            if db_manager.cursor.rowcount == 0:
                print("Record not found.")
            else:
                db_manager.conn.commit()
                print("Record deleted successfully!")
        else:
            print("Please provide an email or use --all for deletion.")

    elif args.action == 'list':
        rows = db_manager.fetch_data(table_name)
        display_records(rows)

    db_manager.close_connection()

if __name__ == "__main__":
    main()