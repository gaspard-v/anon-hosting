from flask import request, render_template, abort
import os
from Exceptions import NoFilesUploaded
from encryption import UploadedFileEncryption, JWTOperation


def _post_file() -> dict[str, str]:
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        raise NoFilesUploaded("file")
    uploaded_file_encryption = UploadedFileEncryption(uploaded_file)
    uploaded_file_encryption.encrypt_and_write_file()
    jwt_dict = uploaded_file_encryption.generate_json().to_dict()
    jwt = JWTOperation(jwt_dict)
    return jwt.generate_encrypted_jwt()


def handle():
    others = {}
    if request.method == "POST":
        try:
            others["file_metadata"] = _post_file()
        except NoFilesUploaded:
            abort(400)
    return render_template("upload.html", **os.environ, **others)
