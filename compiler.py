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
        'WHITESPACE': [' ', '\n', '\r', '\t', '\v', '\f'],
        'LETTER': list(string.ascii_letters)
    }

    def __init__(self) -> None:
        self.token_buffer = []
        self.pointer_start = 0
        self.pointer_end = 0
        return

    def get_next_token(self) -> list:
        if self.pointer_start in self.TOKEN_TYPES['NUM']:
            pass
        elif self.pointer_start in self.TOKEN_TYPES['LETTER']:
            pass
        elif self.pointer_start in self.TOKEN_TYPES['SYMBOL'] :
            pass 
        elif self.pointer_start in self.TOKEN_TYPES['WHITESPACE'] :
            pass
        elif self.pointer_start == '/' : 
            pass
        else :
            SyntaxError("Unrecgonized Character") 
         
    def ID_DFA(self) -> list:
        pass

    def NUM_DFA(self) -> list:
        pass

    def WHITESPACE_DFA(self) -> list:
        pass

    def SYMBOL_DFA(self) -> list:
        pass

    def COMMENT_DFA(self) -> list:
        pass


# Example
code = """
int main() {
    int x = 5;
    return x;
}
"""
