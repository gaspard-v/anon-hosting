from flask import Response, request, render_template, abort
import os
import base64
from Utils.path_operation import get_encrypted_filepath
from Cryptography.JWT.JWE import JWEOperation
from Dataclass import UploadedFileDataStructure
from Cryptography import EncryptionOperation
from flask_wtf.csrf import validate_csrf, generate_csrf, ValidationError
from Cryptography.encrypted_file import get_file_metadata


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


def _return_metadata(jwt: UploadedFileDataStructure, download_key: str) -> str:
    csrf_token = generate_csrf()
    metadata = get_file_metadata(jwt)
    try:
        filepath = get_encrypted_filepath(jwt.stored_filename)
    except:
        abort(400)
    if not os.path.exists(filepath):
        abort(404)
    return render_template(
        "download.html",
        csrf_token=csrf_token,
        file_metadata=True,
        download_key=download_key,
        **metadata.to_dict(),
        **os.environ,
    )


def handle():
    if request.method == "GET":
        csrf_token = generate_csrf()
        return render_template("download.html", csrf_token=csrf_token, **os.environ)
    try:
        validate_csrf(request.form.get("csrf_token"))
    except ValidationError:
        abort(400)
    download_key = request.form.get("download_key")
    if not download_key:
        abort(400)
    jwt = _get_jwt(download_key)

    if request.form.get("download_confirm"):
        return _decrypt_file_and_generate_response(jwt)
    return _return_metadata(jwt, download_key)
