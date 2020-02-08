import lark
from flask import Flask
from flask import render_template
from flask import request


EXAMPLE = """{
    "name": "Achernar",
    "constellation": "Eridanus",
    "spectral_type": "B6 Vep",
    "properties": {
        "right_ascension": [1, 37, 42.84548],
        "declination": [-57, 14, 12.3101],
        "apparent_magnitude": 0.43
    }
}"""
JSON_GRAMMAR = """?value : dict
       | list
       | string
       | SIGNED_NUMBER -> number
       | "true"        -> true
       | "false"       -> false
       | "null"        -> null

string : ESCAPED_STRING
list : "[" [value ("," value)*] "]"
dict : "{" [pair ("," pair)*] "}"
pair : string ":" value

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS"""


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def parse():
    text = EXAMPLE
    grammar = JSON_GRAMMAR
    if request.method == "POST":
        text = request.form["text"]
        grammar = request.form["grammar"]
        parser = lark.Lark(grammar, start="value")
        try:
            ast = parser.parse(text).pretty()
        except lark.exceptions.UnexpectedCharacters as e:
            error = str(e)
    grammar_rows = grammar.count("\n") + 1
    text_rows = text.count("\n") + 1
    return render_template("main.html", **locals())


class TrueJsonTransformer(lark.Transformer):
    list = list
    pair = tuple
    dict = dict

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def number(self, n):
        (n,) = n
        return float(n)


if __name__ == "__main__":
    parser = lark.Lark(JSON_GRAMMAR, start="value")
    ast = parser.parse(EXAMPLE)
    print(ast.pretty())
    data = TrueJsonTransformer().transform(ast)
    for key, value in data.items():
        print(f"{key}: {value}")
