from flask import request, render_template, abort
import os
from Exceptions import NoFilesUploaded
from typing import IO


def __handle_stream(uploaded_stream: IO[bytes]):
    chunk_size = 1024 * 1024
    while True:
        chunk = uploaded_stream.read(chunk_size)
        if not chunk:
            break
        print(f"chunk {chunk.hex()}\n\n\n")


def _post_file() -> bool:
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        raise NoFilesUploaded("file")
    # TODO add a file stream handler
    with uploaded_file.stream as upload_stream:
        __handle_stream(upload_stream)
    return True


def handle():
    if request.method == "POST":
        try:
            _post_file()
        except NoFilesUploaded:
            abort(400)
    return render_template("upload.html", **os.environ)
