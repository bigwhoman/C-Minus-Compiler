# Hooman Keshvari -- 99105667
# Hibod Behnam    -- 99171333

# Define Tokens
import string
from enum import Enum

class TokenType(Enum):
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6
    LETTER = -1

class Scanner():

    TOKEN_TYPES = {
        TokenType.NUM: list(string.digits),
        TokenType.KEYWORD: ["if", "else", "void", "int", "for",
                    "break", "return", "endif"],
        TokenType.SYMBOL: [';', ':', '[', ']', '(', ')', '{', '}', '+',
                   '-', '*', '=', '<'],
        TokenType.WHITESPACE: ['\n', '\r', '\t', '\v', '\f', ' '],
        TokenType.LETTER: list(string.ascii_letters)
    }

    def __init__(self) -> None:
        self.line_number = 0
        self.current_line = ""
        self.symbol_table = {k + 1: v for k, v in enumerate(self.TOKEN_TYPES[TokenType.KEYWORD])}

    def get_input_file(self, input: str):
        self.pointer_start = 0
        self.pointer_end = 0
        self.file = open(input)

    def get_next_token(self):
        # Check end of line
        if self.pointer_end >= len(self.current_line):
            # Read next line
            self.current_line = self.file.readline()
            if self.current_line == "": # end of file
                return None
            self.pointer_start = 0
            self.pointer_end = 0
            self.line_number += 1
            return self.get_next_token()

        self.pointer_start = self.pointer_end
        if self.current_line[self.pointer_start] in self.TOKEN_TYPES[TokenType.NUM]:
            self.pointer_end += 1
            token = self.NUM_DFA()
            return (TokenType.NUM, token)

        elif self.current_line[self.pointer_start] in self.TOKEN_TYPES[TokenType.LETTER]:
            self.pointer_end += 1
            token = self.ID_DFA()
            if token in self.TOKEN_TYPES[TokenType.KEYWORD]:
                return (TokenType.KEYWORD, token)
            else:
                if not token in self.symbol_table.values():
                    self.symbol_table[len(self.symbol_table) + 1] = token
                return (TokenType.ID, token)

        elif self.current_line[self.pointer_start] in self.TOKEN_TYPES[TokenType.SYMBOL]:
            return (TokenType.SYMBOL, self.SYMBOL_DFA())
        elif self.current_line[self.pointer_start] in self.TOKEN_TYPES[TokenType.WHITESPACE]:
            token = self.current_line[self.pointer_end]
            self.pointer_end += 1 
            return (TokenType.WHITESPACE, token)

        elif self.current_line[self.pointer_start] == '/' and \
                self.current_line[self.pointer_start + 1] == '*':
            self.pointer_end += 2
            token = self.COMMENT_DFA()
            return (TokenType.COMMENT, token)
        else:
            self.pointer_end += 1
            raise SyntaxError((self.current_line[self.pointer_start:
                                                     self.pointer_end], "Invalid input"))

    def ID_DFA(self) -> str:
        others = self.TOKEN_TYPES[TokenType.SYMBOL] + self.TOKEN_TYPES[TokenType.WHITESPACE]
        while self.pointer_end < len(self.current_line):
            if self.current_line[self.pointer_end] in self.TOKEN_TYPES[TokenType.LETTER] or \
                    self.current_line[self.pointer_end] in self.TOKEN_TYPES[TokenType.NUM]:
                self.pointer_end += 1
            elif self.current_line[self.pointer_end] in others:
                break
            else:
                self.pointer_end += 1
                raise SyntaxError((self.current_line[self.pointer_start], "Invalid input"))

        return self.current_line[self.pointer_start:
                                 self.pointer_end]

    def NUM_DFA(self) -> str:
        others = self.TOKEN_TYPES[TokenType.SYMBOL] + self.TOKEN_TYPES[TokenType.WHITESPACE]
        while self.pointer_end < len(self.current_line):
            if self.current_line[self.pointer_end] in self.TOKEN_TYPES[TokenType.NUM]:
                self.pointer_end += 1
            elif self.current_line[self.pointer_end] in others:
                break
            else:
                self.pointer_end += 1
                raise SyntaxError((self.current_line[self.pointer_start:
                                                     self.pointer_end], "Invalid number"))
                
        return self.current_line[self.pointer_start:
                    self.pointer_end]

    def WHITESPACE_DFA(self):
        pass

    def SYMBOL_DFA(self) -> str:
        if self.current_line[self.pointer_start] == "=" :
            if len(self.current_line) != self.pointer_start + 1 and self.current_line[self.pointer_start + 1] == "=" : 
                self.pointer_end += 2
                return "=="
            else:
                self.pointer_end += 1
                return "="
        elif len(self.current_line) != self.pointer_start + 1 and self.current_line[self.pointer_start:self.pointer_start + 1] == "*/":
            self.pointer_end += 2
            raise SyntaxError(("*/", "Invalid number"))
        else:
            self.pointer_end += 1
            return self.current_line[self.pointer_start]

    def COMMENT_DFA(self) -> str:
        while self.pointer_end < len(self.current_line):
            self.pointer_end += 1
            if self.current_line[self.pointer_end] == '*' and \
                    self.current_line[self.pointer_end+1] == '/':
                self.pointer_end += 2
                break
        return self.current_line[self.pointer_start:
                    self.pointer_end]


# Example
scanner = Scanner()
scanner.get_input_file("./input.txt")
while True:
    token = scanner.get_next_token()
    if token == None:
        break
    print(scanner.line_number, token)
print(scanner.symbol_table)