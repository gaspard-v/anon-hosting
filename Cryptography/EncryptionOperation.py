from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import IO
from io import BufferedWriter, BufferedReader
import os


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
        self,
        source_stream: BufferedReader,
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
        *,
        close_stream=False
    ):
        while True:
            chunk = source_stream.read(chunk_size)
            if not chunk:
                break
            yield self._decryptor.update(chunk)
        if close_stream:
            source_stream.close()
        yield self._decryptor.finalize()

    @staticmethod
    def generate_key():
        return os.urandom(32)

    @staticmethod
    def generate_tweak():
        return os.urandom(16)
