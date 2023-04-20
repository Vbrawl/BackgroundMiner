from cryptography.hazmat.primitives.ciphers.algorithms import AES256
from cryptography.hazmat.primitives.ciphers import Cipher, modes as CipherModes
from lib.TempManager import TempManager
import os
import base64



class Encryptor:
    BLOCK_SIZE = AES256.block_size
    KEY_SIZE = AES256.key_size


    @staticmethod
    def generate_bytes(size:int) -> bytes:
        # NOTE: size must be KEY_SIZE or BLOCK_SIZE
        return base64.b64encode(os.urandom(size//8))



    def __init__(self, KEY: bytes, IV: bytes):
        self.cipher = Cipher(
            AES256(base64.b64decode(KEY)),
            CipherModes.CBC(base64.b64decode(IV))
        )

        self.IV = IV
        self.encryptor = self.cipher.encryptor()
        self.decryptor = self.cipher.decryptor()
    
    def encrypt(self, filepath: str):
        cipherfile_path = TempManager.get_path(os.path.split(filepath)[1])

        plainfile = open(filepath, 'rb')
        cipherfile = TempManager.open_file(cipherfile_path, 'w')

        total_data = 0

        while (plaindata:=plainfile.read(self.BLOCK_SIZE)) != b'':
            total_data += len(plaindata)
            plaindata:bytes = plaindata + b'0' * (self.BLOCK_SIZE - len(plaindata))
            cipherdata = base64.b64encode(self.encryptor.update(plaindata)).decode("UTF-8")
            cipherfile.write(cipherdata + '\n')
        
        cipherfile.write(base64.b64encode(self.encryptor.finalize()).decode("UTF-8"))
        plainfile.close()
        cipherfile.close()

        plainfile = open(filepath, 'w')
        cipherfile = TempManager.open_file(cipherfile_path, 'r')

        # HEADERS
        plainfile.write(str(total_data) + '\n')

        for line in cipherfile:
            plainfile.write(line)
        
        plainfile.close()
        cipherfile.close()
    
    def decrypt(self, filepath: str):
        plainfile_path = TempManager.get_path(os.path.split(filepath)[1])

        cipherfile = open(filepath, 'r')
        plainfile = TempManager.open_file(plainfile_path, 'wb')

        total_bytes = int(cipherfile.readline())
        parsed_bytes = 0

        for line in cipherfile:
            plaindata = self.decryptor.update(base64.b64decode(line))
            plainfile.write(plaindata[:total_bytes - parsed_bytes])

            parsed_bytes += len(plaindata)
        
        plainfile.close()
        cipherfile.close()

        plaintempFile = open(plainfile_path, 'rb')
        plainfile = open(filepath, 'wb')

        while (plaindata:=plaintempFile.read(self.BLOCK_SIZE)) != b'':
            plainfile.write(plaindata)
        
        plaintempFile.close()
        plainfile.close()