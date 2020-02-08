from lark import Lark
from lark import Transformer

true_json_EBNF = """
    ?value : dict
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
    %ignore WS
"""
true_json_parser = Lark(true_json_EBNF, start="value")


def text_to_ast(text):
    return true_json_parser.parse(text)


class TrueJsonTransformer(Transformer):
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
    text = '{"name": "Achernar", "constellation": "Eridanus", "right_ascension": [1, 37, 42.84548], "declination": [-57, 14, 12.3101], "apparent_magnitude": 0.43, "spectral_type": "B6 Vep", "U-B color index": -0.66, "B-V color index": -0.16}'
    ast = true_json_parser.parse(text)
    print(ast.pretty())
    data = TrueJsonTransformer().transform(ast)
    for key, value in data.items():
        print(f"{key}: {value}")
