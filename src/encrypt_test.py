import unittest
import os
import hashlib

from Crypto.Cipher import AES
from encrypt import DatabaseEncryptor


class TestDatabaseEncryptor(unittest.TestCase):
    """Testclass for database encryptor"""
    def setUp(self):
        self.test_key = b'test_key_16bytes'  # Assuming AES-128
        self.db_encryptor = DatabaseEncryptor(self.test_key)

        # Create temporary test files for encryption and decryption
        self.test_input_file = 'test_input.db'
        self.test_encrypted_file = 'test_input.db.enc'

        with open(self.test_input_file, 'wb', encoding='utf-8') as f:
            f.write(b'Test data for encryption')

    def tearDown(self):
        # Remove the temporary test files after each test
        os.remove(self.test_input_file)
        os.remove(self.test_encrypted_file)

    def test_get_encrypted_db_name(self):
        # Test the generation of encrypted file name
        expected_output = 'test_input.db.enc'
        result = self.db_encryptor.get_encrypted_db_name(self.test_input_file)
        self.assertEqual(result, expected_output)

    def test_encrypt_database(self):
        # Test encryption and MD5 calculation
        result = self.db_encryptor.encrypt_database(self.test_input_file)
        expected_output = (self.test_encrypted_file,
                           self._calculate_md5(self.test_encrypted_file),
                           self._calculate_md5(self.test_input_file))
        self.assertEqual(result, expected_output)

    def test_decrypt_database(self):
        # Test decryption and MD5 calculation
        self.db_encryptor.encrypt_database(self.test_input_file)
        result = self.db_encryptor.decrypt_database(self.test_encrypted_file)
        expected_output = (self.test_input_file,
                           self._calculate_md5(self.test_input_file),
                           self._calculate_md5(self.test_encrypted_file))
        self.assertEqual(result, expected_output)

    def _calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

if __name__ == '__main__':
    unittest.main()
