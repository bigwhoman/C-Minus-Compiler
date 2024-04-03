# Hooman Keshvari -- 99105667
# Hibod Behnam    -- 99171333

# Define Tokens
import string


class Scanner():

    TOKEN_TYPES = {
        'NUM': list(string.digits),
        'KEYWORD': ["if", "else", "void", "int", "for",
                    "break", "return", "endif"],
        'SYMBOL': [';', ':', '[', ']', '(', ')', '{', '}', '+',
                   '-', '*', '=', '<'],
        'WHITESPACE': ['\n', '\r', '\t', '\v', '\f', ' '],
        'LETTER': list(string.ascii_letters)
    }

    def __init__(self) -> None:
        self.text = None
        return

    def get_input_file(self, input):
        self.pointer_start = 0
        self.pointer_end = 0
        file = open(input)
        self.text = file.read()

    def get_next_token(self) -> list:
        if self.text == None:
            print("No given input")
            return

        if self.pointer_end >= len(self.text):
            print("Reached end of input")
            return

        self.pointer_start = self.pointer_end
        if self.text[self.pointer_start] in self.TOKEN_TYPES['NUM']:
            self.pointer_end += 1
            token = self.NUM_DFA(self.text)
            return ('Number', token)

        elif self.text[self.pointer_start] in self.TOKEN_TYPES['LETTER']:
            self.pointer_end += 1
            token = self.ID_DFA(self.text)
            return ('Identifier', token)

        elif self.text[self.pointer_start] in self.TOKEN_TYPES['SYMBOL']:
            if self.text[self.pointer_start] == "=" :
                if self.text[self.pointer_start + 1] == "=" : 
                    self.pointer_end += 2
                    return ('Symbol', "==")
                else :
                    self.pointer_end += 1
                    return ('Symbol', "=")
            else :
                self.pointer_end += 1
                return ('Symbol', self.text[self.pointer_start])
        elif self.text[self.pointer_start] in self.TOKEN_TYPES['WHITESPACE']:
            token = self.text[self.pointer_end]
            self.pointer_end += 1 
            return ('Whitespace', token)

        elif self.text[self.pointer_start] == '/' and \
                self.text[self.pointer_start + 1] == '*':
            self.pointer_end += 2
            token = self.COMMENT_DFA(self.text)
            return ('Comment', token)
        else:
            SyntaxError("Unrecgonized Character")

    def ID_DFA(self, text: str) -> str:
        while self.pointer_end < len(text):
            if text[self.pointer_end] in self.TOKEN_TYPES['LETTER'] or \
                    text[self.pointer_end] in self.TOKEN_TYPES['NUM']:
                self.pointer_end += 1
            else:
                break

        return text[self.pointer_start:
                    self.pointer_end]

    def NUM_DFA(self, text: str) -> str:
        while self.pointer_end < len(text):
            if text[self.pointer_end] in self.TOKEN_TYPES['NUM']:
                self.pointer_end += 1
            else:
                break

        return text[self.pointer_start:
                    self.pointer_end]

    def WHITESPACE_DFA(self) -> list:
        pass

    def SYMBOL_DFA(self) -> list:
        pass

    def COMMENT_DFA(self, text) -> list:
        while self.pointer_end < len(text):
            self.pointer_end += 1
            if text[self.pointer_end] == '*' and \
                    text[self.pointer_end+1] == '/':
                self.pointer_end += 2
                break
        return text[self.pointer_start:
                    self.pointer_end]


# Example
code = """
int main() {
    int x = 5;
    return x;
}
"""
scanner = Scanner()
scanner.get_input_file("./input.txt")
while scanner.pointer_end < len(scanner.text):
    print(scanner.get_next_token())
# print(scanner.get_next_token())
# print(scanner.pointer_start)

# print(scanner.get_next_token())
# print(scanner.pointer_start)
# print(scanner.get_next_token())
# print(scanner.pointer_start)
# print(scanner.get_next_token())
# print(scanner.pointer_start)
# print(scanner.get_next_token())
# print(scanner.pointer_start)
# t = 'jao'
# print(t[0:0])
