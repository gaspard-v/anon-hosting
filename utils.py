import os


def get_encrypted_filepath(filename: str) -> str:
    encrypted_file_storage = os.environ.get("ENCRYPTED_FILE_STORAGE")
    if not os.path.exists(encrypted_file_storage):
        os.mkdir(encrypted_file_storage)
    if encrypted_file_storage:
        return os.path.join(encrypted_file_storage, filename)
    return os.path.join(filename)
