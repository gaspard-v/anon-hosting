from flask import Response, request, render_template, abort
from encryption import JWEOperation, EncryptionOperation, UploadedFileDataStructure
import os
import base64
import utils
import mimetypes


def handle():
    if request.method == "GET":
        return render_template("download.html", **os.environ)
    download_key = request.form.get("download key")
    if not download_key:
        abort(400)
    jwe = JWEOperation(download_key)
    jwt = jwe.decode_jwt()
    key = base64.b64decode(jwt["key"])
    tweak = base64.b64decode(jwt["tweak"])
    stored_filename = jwt["stored_filename"]
    original_filename = jwt["original_filename"]
    [content_type, _] = mimetypes.guess_type(original_filename, strict=False)
    if not type:
        content_type = "application/octet-stream"
    decryptor = EncryptionOperation(key=key, tweak=tweak)
    filepath = utils.get_encrypted_filepath(stored_filename)
    encrypted_file = open(filepath, "rb")
    return Response(
        response=decryptor.stream_to_stream_decryptor(encrypted_file),
        content_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={original_filename}"},
    )
