import os
import sys
'''------------------------CONSTANTS--------------------------------------'''
KEYWORDS = ["echo", "while", "for", "with", "iter"]
ALPHABETS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
NUMBERS = "1234567890."
IGNORE = [" ", "\t", "\n"]
OPERATORS = ["+", "-", "/", "*", "%"]
'''-----------------------------------------------------------------------'''
'''------------------------GENERAL FUNCTIONS------------------------------'''
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
        return f'[Type: {self.type_} | Value: {self.value}]'

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
                self.tokens.append(Token("Operator", self.current_char))

            self.advance()
