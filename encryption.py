from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from werkzeug.datastructures import FileStorage
import random
import string
import os
import base64
from typing import IO, Any
from io import BufferedWriter, BufferedReader
import jwt
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode
from Exceptions import EnvVariableNotDefined
import time
import json
from Dataclass import UploadedFileDataStructure
from Utils.path_operation import get_encrypted_filepath


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
        source_stream.close()
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
        self._content_type = self._file.content_type
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

    def generate_json(self) -> UploadedFileDataStructure:
        key = base64.b64encode(self._encryptor.get_key()).decode()
        tweak = base64.b64encode(self._encryptor.get_other("tweak")).decode()
        return UploadedFileDataStructure(
            key,
            tweak,
            self._orignal_filename,
            self._stored_filename,
            self._content_type,
        )
