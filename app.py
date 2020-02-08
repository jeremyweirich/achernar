from flask import Flask
from flask import render_template
from flask import request

from .parser import text_to_ast


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def parse():
    if request.method == "POST":
        text = request.form["text"]
        ast = text_to_ast(text)
    return render_template("main.html", **locals())


if __name__ == "__main__":
    app.run(debug=True)
