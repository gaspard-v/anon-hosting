from flask import request, render_template, abort
import os
from Exceptions import NoFilesUploaded
from typing import IO
from encryption import UploadedFileEncryption


def _post_file() -> bool:
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        raise NoFilesUploaded("file")
    uploaded_file_encryption = UploadedFileEncryption(uploaded_file)
    uploaded_file_encryption.encrypt_and_write_file()
    print(uploaded_file_encryption.generate_json().to_dict())
    return True


def handle():
    if request.method == "POST":
        try:
            _post_file()
        except NoFilesUploaded:
            abort(400)
    return render_template("upload.html", **os.environ)
