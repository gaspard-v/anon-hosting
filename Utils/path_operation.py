import os


def get_encrypted_filepath(filename: str) -> str:
    encrypted_file_storage = os.environ.get("ENCRYPTED_FILE_STORAGE")
    if not os.path.exists(encrypted_file_storage):
        os.mkdir(encrypted_file_storage)
    if encrypted_file_storage:
        return os.path.join(encrypted_file_storage, filename)
    return os.path.join(filename)


def bytes_to_humans_readable(number: int) -> str:
    unites = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = 0
    while number >= 1000 and i < len(unites) - 1:
        number /= 1000.0
        i += 1
    return f"{number:.2f} {unites[i]}"
