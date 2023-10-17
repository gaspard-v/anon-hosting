from flask import Flask, render_template
from dotenv import load_dotenv
from upload import handle as upload_handle
from download import handle as download_handle
from flask_wtf.csrf import CSRFProtect
import os

load_dotenv()
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html", **os.environ)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return upload_handle()


@app.route("/download", methods=["GET", "POST"])
def download():
    return download_handle()
