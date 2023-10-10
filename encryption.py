from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from werkzeug.datastructures import FileStorage
import random
import string
import os
import base64
from utils import get_encrypted_filepath
from typing import IO, Any
from io import BufferedWriter, BufferedReader
import jwt
from Exceptions import EnvVariableNotDefined
import time


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


class JWTOperation:
    def __init__(self, data: dict[str, Any] | str | bytes):
        if not os.environ.get("SECRET_KEY"):
            raise EnvVariableNotDefined("SECRET_KEY")
        self._key = os.environ["SECRET_KEY"]
        self._algorithm = "HS256"
        self._options = {
            "verify_signature": True,
            "require": ["iat", "nbf"],
            "verify_nbf": "verify_signature",
        }
        epoch_time = int(time.time())
        if isinstance(data, dict):
            claims = {"iat": epoch_time, "nbf": epoch_time}
            self._data = data.update(claims)
        self._data = data

    def generate_jwt(self) -> str:
        if not isinstance(self._data, dict):
            raise ValueError("Data must be a dict")
        return jwt.encode(self._data, algorithms=self._algorithm)

    def generate_encrypted_jwt(self) -> str:
        if not isinstance(self._data, dict):
            raise ValueError("Data must be a dict")
        return jwt.encode(self._data, key=self._key, algorithm=self._algorithm)

    def decode_jwt(self) -> str:
        if not isinstance(self._data, (str, bytes)):
            raise ValueError("Data must be an str or bytes")
        return jwt.decode(
            self._data,
            algorithms=self._algorithm,
            options=self._options,
        )

    def decode_encrypted_jwt(self) -> str:
        if not isinstance(self._data, (str, bytes)):
            raise ValueError("Data must be an str or bytes")
        return jwt.decode(
            self._data,
            key=self._key,
            algorithms=self._algorithm,
            options=self._options,
        )


class EncryptionOperation:
    _DEFAULT_CHUNK_SIZE = 1204 * 1024 * 4  # 4 MB

    def __init__(self, key: bytes = None, **kwargs) -> None:
        self._kwargs = kwargs
        if not key:
            key = EncryptionOperation.generate_key()
        self._key = key
        if not kwargs.get("tweak"):
            self._kwargs["tweak"] = EncryptionOperation.generate_tweak()
        self._cipher = Cipher(
            algorithm=algorithms.AES(self._key), mode=modes.XTS(self._kwargs["tweak"])
        )
        self._encryptor = self._cipher.encryptor()
        self._decryptor = self._cipher.decryptor()

    def get_key(self) -> bytes:
        return self._key

    def get_other(self, key: str):
        return self._kwargs.get(key)

    def stream_to_stream_encryption(
        self,
        source_stream: IO[bytes],
        dest_stream: BufferedWriter,
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
    ) -> int:
        total_write = 0
        while True:
            chunk = source_stream.read(chunk_size)
            if not chunk:
                break
            total_write += dest_stream.write(self._encryptor.update(chunk))
        total_write += dest_stream.write(self._encryptor.finalize())
        return total_write

    def stream_to_stream_decryptor(
        self, source_stream: BufferedReader, chunk_size: int = _DEFAULT_CHUNK_SIZE
    ):
        while True:
            chunk = source_stream.read(chunk_size)
            if not chunk:
                break
            yield self._decryptor.update(chunk)
        yield self._decryptor.finalize()

    @staticmethod
    def generate_key():
        return os.urandom(32)

    @staticmethod
    def generate_tweak():
        return os.urandom(16)


class UploadedFileEncryption:
    def __init__(self, file: FileStorage) -> None:
        self._file = file
        self._orignal_filename = self._file.filename
        self._stored_filename = self._generate_random_filename()
        self._encryptor = EncryptionOperation()

    def _generate_random_filename(self) -> str:
        char_dict = string.ascii_letters + string.digits
        filename_length = 20
        random_filename = "".join(
            random.choice(char_dict) for _ in range(filename_length)
        )
        return random_filename

    def encrypt_and_write_file(self) -> int:
        encrypted_filepath = get_encrypted_filepath(self._stored_filename)
        with open(
            encrypted_filepath, "wb"
        ) as encrypted_file, self._file.stream as stream:
            return self._encryptor.stream_to_stream_encryption(stream, encrypted_file)
        # TODO : implement
        # functionnal file decryption
        # with open(encrypted_filepath, "rb") as encrypted_file, open(
        #     "lol.png", "wb"
        # ) as lol:
        #     for decrypted_chunk in self._encryptor.stream_to_stream_decryptor(
        #         encrypted_file
        #     ):
        #         lol.write(decrypted_chunk)
        # return 1

    def generate_json(self) -> UploadedFileDataStructure:
        key = base64.b64encode(self._encryptor.get_key()).decode()
        tweak = base64.b64encode(self._encryptor.get_other("tweak")).decode()
        return UploadedFileDataStructure(
            key, tweak, self._orignal_filename, self._stored_filename
        )
