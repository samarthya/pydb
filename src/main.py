"""Main entry point for the program"""
import argparse
import os
import base64
import logging
import binascii
import sys

# Import the created classes
from config import TableConfig
from db import DatabaseManager
from encrypt import DatabaseEncryptor
from Crypto.Cipher import AES

CONFIG_FILE="config.json"
AES_KEY_LENGTH = AES.key_size # AES key length in bytes (for AES-256)

EMD5="emd5"
PMD5="pmd5"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()  # Send logs to the console
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def generate_encoded_key():
    """generate encoded key
    Returns:
        str: Base64 encoded key
    """
    return base64.b64encode(os.urandom(AES_KEY_LENGTH)).decode('utf-8')

def display_records(rows):
    """Displays the records read from the Database

    Args:
        rows: Information that was read
    """
    if not rows:
        print("No records found.")
    else:
        print("Records:")
        for row in rows:
            print(row)

def parser_initializer(parser):
    """Initializes parser params

    Args:
        parser: Arg parser initialization
    """
    parser.add_argument('--action', choices=['menu', 'add', 'delete', 'list'],
                        default='menu', help='Choose action mode: menu, add, delete, list')
    parser.add_argument('--name', help='Name for adding a record')
    parser.add_argument('--email', help='Email for adding/deleting a record')
    parser.add_argument('--all', action='store_true', help='Delete all records')
    return parser.parse_args()

def check_config():
    """Checks if the config file exists
    """
    if not os.path.exists(CONFIG_FILE):
        logger.error("Config file is absent")
        sys.exit(1)

def menu():
    """Displays menu"""
    print("\nMenu:")
    print("1. Add a record")
    print("2. Delete a record")
    print("3. List all records")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def main():
    """main function"""
    logger.debug("main: execution begins")

    parser = argparse.ArgumentParser(description='Database Operations')
    args = parser_initializer(parser)

    logger.info("main: config file is present: %s", CONFIG_FILE)

    table_config = TableConfig(CONFIG_FILE)
    table_name = table_config.get("table_name")
    database_name = table_config.get("database_name")
    encryption_key = table_config.get("encryption_key")

    logger.debug("Table: %s Databse: %s Key: %s", table_name, database_name, encryption_key)

    if database_name:
        logger.debug("Database file operations in progress")

        if not encryption_key:
            logger.info("No encryption key found, generating a new one")
            # Generate a base64-encoded key if it's missing
            encryption_key = generate_encoded_key()
            logger.info("Generated a new key")
            table_config.set("encryption_key", encryption_key)

            logger.info("Saving the new new key to the configuration")
            table_config.overwrite()

        # The key will always in base64 format in the config.json
        try:
            logger.debug("Decoding the key")
            encryption_key=base64.b64decode(encryption_key)
        except binascii.Error:
            logger.error(" Not B64 encoded key")
            sys.exit(1)

        # Create DatabaseEncryption instance
        db_encryption = DatabaseEncryptor(encryption_key)

        # Database file. database_name is the name of the file
        if os.path.exists(database_name):
            logger.debug("File %s exists", database_name)
            # Decrypt the database file (Example: For verification purposes)
            database_name, plainmd5, encryptedmd5 = db_encryption.decrypt_database(database_name)
            if len(table_config.get(EMD5)) > 0:
                if encryptedmd5 != table_config.get(EMD5):
                    logger.debug("The checksum failed for the encrypted file")
                    sys.exit(2)
                logger.info("Checksum verification success %s", encryptedmd5)

            logger.debug("Decrypted '%s', Digest: %s", database_name, plainmd5)

            # create_encrypted_database(database_name, encryption_key)
            db_manager = DatabaseManager(database_name)
        else:
            # It is running a fresh instance
            logger.debug("Running DB setup.")
            db_manager = DatabaseManager(database_name)
            columns = table_config.get_columns()
            db_manager.create_table(table_name, columns)
    else:
        print("Database Name is must have. (Full path) ")
        sys.exit(1)

    if args.action == 'menu':
        while True:
            choice = menu()

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

    # Now encrypt before exiting
    logger.debug("Encrypt file")

    # # Encrypt the database file
    database_name, encryptedmd5, pmd5 = db_encryption.encrypt_database(database_name)
    logger.debug("Database file: %s encrypted MD5: %s", database_name, encryptedmd5)

    table_config.set(EMD5, encryptedmd5)
    table_config.set(PMD5, pmd5)
    table_config.overwrite()


if __name__ == "__main__":
    main()
