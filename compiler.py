# Hooman Keshvari -- 99105667
# Hibod Behnam    -- 99171333

import scanner
import c_parser

def main():
    # Setup the scanner
    s = scanner.Scanner()
    s.get_input_file("input.txt")
    # Setup the parser
    c_parser.lookahead = s.get_lookahead_token()
    c_parser.get_next_token = s.get_lookahead_token
    c_parser.S()

if __name__ == "__main__":
    main()