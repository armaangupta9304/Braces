from Braces import Braces
from Braces import Parser

with open("test.brace", "r") as f:
    code = f.read()
    brace = Braces(code)
    brace.gen_tokens()
    parser = Parser(brace.tokens)
    ast = parser.parse()
    print(ast)