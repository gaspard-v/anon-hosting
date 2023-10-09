import os


def get_encrypted_filepath(filename: str) -> str:
    encrypted_file_storage = os.environ.get("ENCRYPTED_FILE_STORAGE")
    if encrypted_file_storage:
        return os.path.join(encrypted_file_storage, filename)
    return os.path.join(filename)
