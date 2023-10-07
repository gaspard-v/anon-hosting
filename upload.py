from flask import request, render_template
import os
from Exceptions import NoFilesUploaded

def _post_file() -> bool:
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        raise NoFilesUploaded("file")
    # TODO add a file stream handler
    return True

def handle():
    if request.method == "POST":
        _post_file()
    return render_template("upload.html", **os.environ)