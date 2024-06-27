# Hooman Keshvari -- 99105667
# Hibod Behnam    -- 99171333

import anytree
import c_parser
import code_generator
import scanner

def main():
    # Setup the scanner
    s = scanner.Scanner()
    s.get_input_file("input.txt")
    # Setup the parser
    c_parser.lookahead = s.get_lookahead_token()
    c_parser.get_next_token = s.get_lookahead_token
    c_parser.get_scanner_lookahead = s.get_current_scanner_lookahead_str
    c_parser.get_current_line = s.get_current_line_number
    c_parser.code_generator = code_generator.CodeGenerator(s)
    main_program = anytree.Node("main")
    try:
        c_parser.S(main_program)
    except SyntaxError as e: # TODO: use something else. For example self made class
        pass # Unexpected EOF

if __name__ == "__main__":
    main()