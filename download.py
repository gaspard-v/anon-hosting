from flask import Response, request, render_template, abort
from encryption import JWEOperation
import os


def handle():
    if request.method == "GET":
        return render_template("download.html", **os.environ)
    download_key = request.form.get("download key")
    if not download_key:
        abort(400)
    jwt = JWEOperation(download_key)
    jwt.decode_jwt()
