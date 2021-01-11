from Braces import Braces

with open("test.brace", "r") as f:
    code = f.read()
    brace = Braces(code)
    brace.gen_tokens()
    print(brace.tokens)
    