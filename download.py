from flask import Response, request, render_template, abort
import os
import base64
from Utils.path_operation import get_encrypted_filepath
from Cryptography.JWT.JWE import JWEOperation
from Dataclass import UploadedFileDataStructure
from Cryptography import EncryptionOperation


def _get_jwt(download_key: str) -> UploadedFileDataStructure:
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
        filepath = get_encrypted_filepath(jwt.stored_filename)
    except:
        abort(400)
    if not os.path.exists(filepath):
        abort(404)
    encrypted_file = open(filepath, mode="rb")
    return Response(
        response=decryptor.stream_to_stream_decryptor(
            encrypted_file, close_stream=True
        ),
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
    jwt = _get_jwt(download_key)
    return _decrypt_file_and_generate_response(jwt)
