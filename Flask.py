from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world"

@app.route("/hello_flask")
def hello_flask():
    return render_template(
        "template.html",
        title = "Hello Flask",
        description = "This is my first website!")