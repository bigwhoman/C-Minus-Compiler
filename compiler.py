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
        TokenType.SYMBOL: [';', ':', ',', '[', ']', '(', ')', '{', '}', '+',
                   '-', '*', '=', '<'],
        TokenType.WHITESPACE: ['\n', '\r', '\t', '\v', '\f', ' '],
        TokenType.COMMENT: ['/'],
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
        other = self.TOKEN_TYPES[TokenType.NUM] + self.TOKEN_TYPES[TokenType.LETTER] + self.TOKEN_TYPES[TokenType.SYMBOL] + self.TOKEN_TYPES[TokenType.COMMENT] + self.TOKEN_TYPES[TokenType.WHITESPACE]
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
        elif not self.current_line[self.pointer_start + 1] in other:
            self.pointer_end += 2
            raise SyntaxError((self.current_line[self.pointer_start:self.pointer_start + 2], "Invalid input"))
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

def main():
    scanner = Scanner()
    scanner.get_input_file("./input.txt")
    # line number to list of tokens or errors
    tokens: dict[int, list[tuple[TokenType, str]]] = {}
    errors: dict[int, list[tuple[str, str]]] = {}
    # Parse the input
    while True:
        try:
            token = scanner.get_next_token()
            if token == None:
                break
            if token[0] == TokenType.WHITESPACE or token[0] == TokenType.COMMENT:
                    continue # skip whitespace and comment
            if not scanner.line_number in tokens:
                tokens[scanner.line_number] = []
            tokens[scanner.line_number].append(token)
        except SyntaxError as e:
            if not scanner.line_number in errors:
                errors[scanner.line_number] = []
            errors[scanner.line_number].append(e.args[0])
    # Write the result in file
    with open("tokens.txt", "w") as tokens_file:
        for line_number, token_list in sorted(tokens.items()):
            tokens_file.write(f"{line_number}.\t")
            for token in token_list:
                tokens_file.write(f"({token[0].name}, {token[1]}) ")
            tokens_file.write("\n")
    with open("lexical_errors.txt", "w") as lexical_errors_file:
        if len(errors) == 0:
            lexical_errors_file.write("There is no lexical error.")
        else:
            for line_number, errors_list in sorted(errors.items()):
                lexical_errors_file.write(f"{line_number}.\t")
                for error in errors_list:
                    lexical_errors_file.write(f"({error[0]}, {error[1]}) ")
                lexical_errors_file.write("\n")
    with open("symbol_table.txt", "w") as symbol_table_file:
        for index, symbol in sorted(scanner.symbol_table.items()):
            symbol_table_file.write(f"{index}.\t{symbol}\n")

if __name__ == "__main__":
    main()