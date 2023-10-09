from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from werkzeug.datastructures import FileStorage
import random
import string
import os
import base64
from utils import get_encrypted_filepath
from typing import IO
from io import BufferedWriter


class UploadedFileDataStructure:
    def __init__(
        self, key: str, tweak: str, original_filename: str, stored_filename: str
    ) -> None:
        self.key = key
        self.tweak = tweak
        self.original_filename = original_filename
        self.stored_filename = stored_filename

    def to_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "tweak": self.tweak,
            "original_filename": self.original_filename,
            "stored_filename": self.stored_filename,
        }


class EncryptionOperation:
    def __init__(self, key: bytes = None, **kwargs) -> None:
        self._kwargs = kwargs
        if not key:
            key = EncryptionOperation.generate_key()
        self._key = key
        if not kwargs.get("tweak"):
            self._kwargs.tweak = EncryptionOperation.generate_tweak()
        self._cipher = Cipher(
            algorithm=algorithms.AES(self._key), mode=modes.XTS(self._kwargs.tweak)
        )
        self._encryptor = self._cipher.encryptor()

    def get_key(self) -> bytes:
        return self._key

    def get_other(self, key: str):
        return self._kwargs.get(key)

    def stream_to_stream_encryption(
        self,
        source_stream: IO[bytes],
        dest_stream: BufferedWriter,
        chunk_size: int = 1024 * 1024,
    ) -> int:
        total_write = 0
        while True:
            chunk = source_stream.read(chunk_size)
            if not chunk:
                break
            total_write += dest_stream.write(self._encryptor.update(chunk))
        total_write += dest_stream.write(self._encryptor.finalize())
        return total_write

    @staticmethod
    def generate_key():
        return os.urandom(32)

    @staticmethod
    def generate_tweak():
        return os.urandom(16)


class UploadedFileEncryption:
    def __init__(self, file: FileStorage) -> None:
        self._key = os.urandom(32)
        self._tweak = os.urandom(16)
        self._file = file
        self._orignal_filename = self._file.filename
        self._stored_filename = self._generate_random_filename()
        self._cipher = Cipher(
            algorithm=algorithms.AES(self._key), mode=modes.XTS(self._tweak)
        )
        self._encryptor = self._cipher.encryptor()

    def _generate_random_filename(self) -> str:
        char_dict = string.ascii_letters + string.digits
        filename_length = 20
        random_filename = "".join(
            random.choice(char_dict) for _ in range(filename_length)
        )
        return random_filename

    def encrypt_and_write_file(self):
        chunk_size = 1024 * 1024
        encrypted_filepath = get_encrypted_filepath(self._stored_filename)
        with open(
            encrypted_filepath, "wb"
        ) as encrypted_file, self._file.stream as stream:
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                encrypted_file.write(self._encryptor.update(chunk))
            encrypted_file.write(self._encryptor.finalize())

    def generate_json(self) -> UploadedFileDataStructure:
        key = base64.b64encode(self._key).decode()
        tweak = base64.b64encode(self._tweak).decode()
        return UploadedFileDataStructure(
            key, tweak, self._orignal_filename, self._stored_filename
        )
