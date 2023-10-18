from Dataclass import UploadedFileDataStructure, FileMetadata
import os
from Utils.path_operation import get_encrypted_filepath, bytes_to_humans_readable


def get_file_metadata(jwt: UploadedFileDataStructure) -> FileMetadata:
    filepath = get_encrypted_filepath(jwt.stored_filename)
    size = os.stat(filepath).st_size
    metadata = FileMetadata(
        original_filename=jwt.original_filename,
        content_type=jwt.content_type,
        readable_size=bytes_to_humans_readable(size),
        size=size,
    )
    return metadata
