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
    c_parser.code_generator.program_block.dump()
    with open("semantic_errors.txt", "w") as semantic_errors:
        for error in c_parser.code_generator.semantic_analyzer.error_list:
            semantic_errors.write(error)
            semantic_errors.write("\n")
        if len(c_parser.code_generator.semantic_analyzer.error_list) == 0:
            semantic_errors.write("The input program is semantically correct.\n")

if __name__ == "__main__":
    main()