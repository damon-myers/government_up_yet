from flask import Flask
app = Flask(__name__)


@app.route("/")
def is_it_up():
    return "No."
