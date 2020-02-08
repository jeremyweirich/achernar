from flask import Flask


app = Flask(__name__)


@app.route("/")
def parse():
    return "parse"


if __name__ == "__main__":
    pass
