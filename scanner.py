import string
from enum import Enum

# Define Tokens
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
        TokenType.SYMBOL: [';', ':', ',', '[', ']', '(', ')', '{', '}', '+',
                   '-', '*', '=', '<'],
        TokenType.WHITESPACE: ['\n', '\r', '\t', '\v', '\f', ' '],
        TokenType.COMMENT: ['/'],
        TokenType.LETTER: list(string.ascii_letters)
    }

    def __init__(self) -> None:
        self.line_number = 0
        self.current_line = ""
        self.lookahead_token = None
        self.symbol_table = {k + 1: v for k, v in enumerate(self.TOKEN_TYPES[TokenType.KEYWORD])}

    def get_input_file(self, input: str):
        self.pointer_start = 0
        self.pointer_end = 0
        self.file = open(input)

    def get_current_scanner_lookahead_str(self) -> str:
        if self.lookahead_token == None:
            return "$"
        return f"({self.lookahead_token[0].name}, {self.lookahead_token[1]})"

    def get_lookahead_token(self) -> str:
        try:
            self.lookahead_token = self.get_next_token()
        except SyntaxError:
            return self.get_lookahead_token()
        if self.lookahead_token == None:
            return "$" # EOF
        if self.lookahead_token[0] == TokenType.NUM:
            return "NUM"
        if self.lookahead_token[0] == TokenType.ID:
            return "ID"
        if self.lookahead_token[0] == TokenType.KEYWORD:
            return self.lookahead_token[1]
        if self.lookahead_token[0] == TokenType.SYMBOL:
            return self.lookahead_token[1]
        # Whitespace or comment. Skip it and get the next token
        return self.get_lookahead_token()

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
            self.pointer_end += 1
            token = self.COMMENT_DFA()
            return (TokenType.COMMENT, token)
        else:
            self.pointer_end += 1
            raise SyntaxError((self.current_line[self.pointer_start:
                                                     self.pointer_end], "Invalid input"))

    def ID_DFA(self) -> str:
        others = self.TOKEN_TYPES[TokenType.SYMBOL] + self.TOKEN_TYPES[TokenType.WHITESPACE] + self.TOKEN_TYPES[TokenType.COMMENT]
        while self.pointer_end < len(self.current_line):
            if self.current_line[self.pointer_end] in self.TOKEN_TYPES[TokenType.LETTER] or \
                    self.current_line[self.pointer_end] in self.TOKEN_TYPES[TokenType.NUM]:
                self.pointer_end += 1
            elif self.current_line[self.pointer_end] in others:
                break
            else:
                self.pointer_end += 1
                raise SyntaxError((self.current_line[self.pointer_start:
                                 self.pointer_end], "Invalid input"))

        return self.current_line[self.pointer_start:
                                 self.pointer_end]

    def NUM_DFA(self) -> str:
        others = self.TOKEN_TYPES[TokenType.SYMBOL] + self.TOKEN_TYPES[TokenType.WHITESPACE] + self.TOKEN_TYPES[TokenType.COMMENT]
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
        # Check end of the line early
        if len(self.current_line) == self.pointer_start + 1:
            self.pointer_end += 1
            return self.current_line[self.pointer_start]
        # We are not at the end of the line
        if self.current_line[self.pointer_start:self.pointer_start + 2] == "==":
            self.pointer_end += 2
            return "=="
        elif self.current_line[self.pointer_start:self.pointer_start + 2] == "*/":
            self.pointer_end += 2
            raise SyntaxError(("*/", "Unmatched comment"))
        else:
            self.pointer_end += 1
            return self.current_line[self.pointer_start]

    def COMMENT_DFA(self) -> str:
        initial_line_number = self.line_number
        comment = "/*"
        while True:
            self.pointer_end += 1
            # Read next line if needed
            if self.pointer_end >= len(self.current_line):
                self.current_line = self.file.readline()
                if self.current_line == "": # end of file
                    trimmed_comment = comment
                    if len(trimmed_comment) > 7:
                        trimmed_comment = comment[:7] + "..."
                    self.line_number = initial_line_number
                    raise SyntaxError((trimmed_comment, "Unclosed comment"))
                self.pointer_start = 0
                self.pointer_end = -1
                self.line_number += 1
                continue
            comment += self.current_line[self.pointer_end]
            if len(self.current_line) != self.pointer_start + 1 and self.current_line[self.pointer_end] == '*' and \
                    self.current_line[self.pointer_end+1] == '/':
                self.pointer_end += 2
                comment += "/"
                break
        return comment