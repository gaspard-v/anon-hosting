from werkzeug.datastructures import FileStorage
import random
from Utils.path_operation import get_encrypted_filepath
from Dataclass import UploadedFileDataStructure
from Cryptography import EncryptionOperation
import string
import base64


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
