from flask import request, render_template, abort
import os
from Exceptions import NoFilesUploaded
from Cryptography.flask import UploadedFileEncryption
from Cryptography.JWT.JWE import JWEOperation
from flask_wtf.csrf import validate_csrf, generate_csrf, ValidationError


def _post_file() -> dict[str, str]:
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        raise NoFilesUploaded("file")
    uploaded_file_encryption = UploadedFileEncryption(uploaded_file)
    uploaded_file_encryption.encrypt_and_write_file()
    jwt_dict = uploaded_file_encryption.generate_json().to_dict()
    jwe = JWEOperation(jwt_dict)
    return jwe.generate_jwt()


def handle():
    others = {}
    if request.method == "POST":
        try:
            validate_csrf(request.form.get("csrf_token"))
            others["file_metadata"] = _post_file()
        except (NoFilesUploaded, ValidationError):
            abort(400)
    others["csrf_token"] = generate_csrf()
    return render_template("upload.html", **os.environ, **others)
