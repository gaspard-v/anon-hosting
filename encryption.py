from cryptography.fernet import Fernet
from werkzeug.datastructures import FileStorage
import random
import string


class UploadedFileDateStructure:
    def __init__(self, key: str, original_filename: str, stored_filename: str) -> None:
        self.key = key
        self.original_filename = original_filename
        self.stored_filename = stored_filename

    def to_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "original_filename": self.original_filename,
            "stored_filename": self.stored_filename,
        }


class UploadedFileEncryption:
    def __init__(self, file: FileStorage) -> None:
        self._key = Fernet.generate_key()
        self._file = file
        self._orignal_filename = self._file.filename
        self._stored_filename = self._generate_random_filename()

    def _generate_random_filename(self) -> str:
        char_dict = string.ascii_letters + string.digits
        filename_length = 20
        random_filename = "".join(
            random.choice(char_dict) for _ in range(filename_length)
        )
        return random_filename

    def generate_json(self) -> UploadedFileDateStructure:
        key = self._key.decode()
        return UploadedFileDateStructure(
            key, self._orignal_filename, self._stored_filename
        )
