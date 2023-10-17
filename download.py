from flask import Response, request, render_template, abort
from encryption import JWEOperation, EncryptionOperation, UploadedFileDataStructure
import os
import base64
import utils


def _get_jwt(download_key) -> UploadedFileDataStructure:
    jwe = JWEOperation(download_key)
    try:
        jwt = jwe.decode_jwt()
        return UploadedFileDataStructure(**jwt)
    except:
        abort(400)


def _decrypt_file_and_generate_response(jwt: UploadedFileDataStructure) -> Response:
    key = base64.b64decode(jwt.key)
    tweak = base64.b64decode(jwt.tweak)
    decryptor = EncryptionOperation(key=key, tweak=tweak)
    try:
        filepath = utils.get_encrypted_filepath(jwt.stored_filename)
    except:
        abort(400)
    encrypted_file = open(filepath, mode="rb")
    return Response(
        response=decryptor.stream_to_stream_decryptor(encrypted_file),
        content_type=jwt.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={jwt.original_filename}"
        },
    )


def handle():
    if request.method == "GET":
        return render_template("download.html", **os.environ)
    download_key = request.form.get("download key")
    if not download_key:
        abort(400)
    jwt = _get_jwt()
    return _decrypt_file_and_generate_response(jwt)
