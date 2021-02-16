# Imports #
import os
import sys

'''------------------------CONSTANTS--------------------------------------'''
KEYWORDS = ["echo", "while", "for", "with", "iter"]
ALPHABETS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
NUMBERS = "1234567890."
IGNORE = [" ", "\t", "\n"]
OPERATORS = ["+", "-", "/", "*", "%"]
L_BRACKET = '('
R_BRACKET = ')'
SEMI_COLON = ";"

'''-----------------------------------------------------------------------'''
'''------------------------|GENERAL FUNCTIONS|------------------------------'''
'''-----------------------------------------------------------------------'''
def parse_numbers(brace):
    str_num = ""
    decimal_count = 0
    while brace.current_char in NUMBERS:
        str_num += brace.current_char
        if brace.current_char == ".":
            decimal_count += 1

        if decimal_count > 1:
            break

        brace.advance()

    num = None
    isFloat = False
    if decimal_count == 0:
        num = int(str_num)
    else:
        num = float(str_num)
        isFloat += 1

    return [num, isFloat]


'''---------------------------GENERAL CLASSES--------------------------------'''
class Token:
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f'[{self.type_} | {self.value}]'

class OperatorNode:
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value
    
    def __repr__(self):
        return f'[{self.type_} | {self.value}]'

class Error:
    def __init__(self, type_, message):
        self.type_, self.message = type_, message

    def activate(self):
        print(f'[  {self.type_} | {self.message}   ]')
        sys.exit(1)

class TypoError(Error):
    def __init__(self, char):
        super.__init__("Grammar Error", char, "This character is illegal")

    def activate(self):
        self.activate()

class Node:
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value
    def __repr__(self):
        return self.value

class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.op} {self.right})'

class NumberNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'{self.value}'

'''--------------------------MAIN BRACE CLASS--------------------------------'''
class Braces:
    def __init__(self, code):
        self.code = code
        self.current_index = 0
        self.current_char = self.code[self.current_index]
        self.text = ''
        self.tokens = []
        self.onString = False
        self.curr_string = ''
        self.Nodes = []

    def advance(self):
        self.current_index += 1
        if self.current_index <= len(self.code) - 1 and self.current_char != None:
            self.current_char = self.code[self.current_index]

        else:
            self.current_char = None
        
    def gen_tokens(self):
        while self.current_char != None:
            
            if self.text in KEYWORDS:
                self.tokens.append(Token(self.text, self.text))
            if self.current_char in IGNORE:
                self.text = ""
            if self.current_char in ALPHABETS:
                self.text += self.current_char
            
            if self.current_char == '\'' and self.onString == False:
                self.advance()
                self.onString = True
                while True and self.current_char != None:
                    if self.current_char == '\'':
                        self.curr_string.replace('\'', '')
                        break
                    else:
                        self.curr_string += self.current_char
                    self.advance()
                
                self.tokens.append(Token("String", self.curr_string))
                self.text = ''
                self.curr_string = ''
                self.onString = False

            if self.current_char in NUMBERS:
                [num, isFloat] = parse_numbers(self)
                if isFloat:
                    self.tokens.append(Token(type_="Float", value=num))
                else:
                    self.tokens.append(Token("Integer", value=num))

            if self.current_char in OPERATORS:
                self.text += self.current_char
                self.tokens.append(OperatorNode("Operator", self.current_char))

            if self.current_char == L_BRACKET:
                self.text += self.current_char
                self.tokens.append(Token("L_BRACKET", self.current_char))

            if self.current_char == R_BRACKET:
                self.text += self.current_char
                self.tokens.append(Token("R_BRACKET", self.current_char))
            
            if self.current_char == SEMI_COLON:
                self.text += self.current_char
                self.tokens.append(Token("SEMI_COLON", self.current_char))

            self.advance()

    def echo(self, string):
        print(string)


class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
        self.nodes = []

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.token_idx

    def factors(self):
        if self.current_token.type_ in ("Integer", "Float"):
            number = NumberNode(self.current_token)
            self.advance()
            return number
    
    def binary_op(self, func, ops):
        left = func()
        while self.current_token.value in ops:
            op = self.current_token
            self.advance()
            right = func()
            left = BinaryOp(op, left, right)

        return left

    def parse(self):
        return self.expr()

    def term(self):
        return self.binary_op(self.factors, ("*", "/"))

    def expr(self):
        return self.binary_op(self.term, ("+", "-"))

if __name__ == "__main__":
    while True:
        command = input("Brace $> ")
        if command == "exit":
            exit()
        brace = Braces(command)
        brace.gen_tokens()
        parser = Parser(brace.tokens)
        ast = parser.parse()
        print(ast)
        print(brace.tokens)
