from flask import Flask, render_template
from dotenv import load_dotenv
from upload import handle as upload_handle
from download import handle as download_handle
import os

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", **os.environ)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return upload_handle()


@app.route("/download", methods=["GET", "POST"])
def download():
    return download_handle()
