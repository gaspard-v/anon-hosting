from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", **os.environ)

@app.route("/upload")
def upload():
    return