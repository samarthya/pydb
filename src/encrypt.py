"""Exposes cryptography functions"""
import shutil
import os
import hashlib

from Crypto.Cipher import AES

class DatabaseEncryptor:
    """Database file encryptor"""
    def __init__(self, key):
        self.key = key
        self.block_size = AES.block_size
        self.logger = None

    def set_logger(self, logger):
        """Sets the logger"""
        self.logger = logger

    def _pad(self, data):
        padding_length = self.block_size - len(data) % self.block_size
        padding = bytes([padding_length]) * padding_length
        return data + padding

    def _unpad(self, data):
        padding_length = data[-1]
        if padding_length < 1 or padding_length > self.block_size:
            raise ValueError("Invalid padding")
        return data[:-padding_length]

    def get_encrypted_db_name(self, db_file):
        """Returns a new filename based on the inputfile

        Args:
            db_file : Existing file

        Returns:
            encrypted file path
        """
        if db_file.endswith(".enc"):
            return db_file
        file_path, file_name = os.path.split(db_file)
        output_file = file_name + ".enc"
        encrypted_file_path = os.path.join(file_path, output_file)
        return encrypted_file_path

    def encrypt_database(self, db_file):
        """Encrypts database file

        Args:
            db_file : Input file to be read

        Returns:
            Encrypted file informtation
        """
        # db_file is unencrypted file and output_file is the encrypted file
        # identifying file and path
        plain_md5 = self.calculate_md5(db_file)
        encrypted_file_path = self.get_encrypted_db_name(db_file)
        self.encrypt_file_in_memory(encrypted_file_path)
        encrypted_md5 = self.calculate_md5(encrypted_file_path)
        if self.logger:
            self.logger.log_info(f"MD5 of Encrypted File: {encrypted_md5} & Plain Text: {plain_md5}")
        else:
            print(f"MD5 of Encrypted File: {encrypted_md5} & Plain Text: {plain_md5}")
        return encrypted_file_path, encrypted_md5, plain_md5


    def decrypt_database(self, db_file):
        """Decrypt database file

        Args:
            db_file: Path to the DB_file

        Returns:
            decrypted_file, plainmd5, encryptedmd5
        """
        # db_file is unencrypted file and output_file is the encrypted file
        # identifying file and path

        encrypted_file_path = self.get_encrypted_db_name(db_file)
        encrypted_md5 = self.calculate_md5(encrypted_file_path)
        self.decrypt_file_in_memory(encrypted_file_path)
        plain_md5 = self.calculate_md5(encrypted_file_path)
        if not self.logger:
            print(f"MD5 of Encrypted File: {encrypted_md5} & Plain Text: {plain_md5}")
        else:
            self.logger.log_info(f"MD5 of Encrypted File: {encrypted_md5} & Plain Text: {plain_md5}")
        return db_file, plain_md5, encrypted_md5

    #################################################
    def encrypt_file_in_memory(self, file_path):
        with open(file_path, 'rb') as file:
            plaintext = file.read()

        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_plaintext = self._pad(plaintext)
        encrypted_data = cipher.encrypt(padded_plaintext)

        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        return file_path

    def decrypt_file_in_memory(self, file_path):
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_data = cipher.decrypt(encrypted_data)
        unpadded_data = self._unpad(decrypted_data)

        with open(file_path, 'wb') as file:
            file.write(unpadded_data)
        return file_path

    ####################################################
    def encrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            plaintext = file.read()

        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_plaintext = self._pad(plaintext)
        encrypted_data = cipher.encrypt(padded_plaintext)

        with open(output_file, 'wb') as file:
            file.write(encrypted_data)
        return output_file

    def decrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            encrypted_data = file.read()

        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_data = cipher.decrypt(encrypted_data)
        unpadded_data = self._unpad(decrypted_data)

        with open(output_file, 'wb') as file:
            file.write(unpadded_data)

        return output_file

    def calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()