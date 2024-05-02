# Hooman Keshvari -- 99105667
# Hibod Behnam    -- 99171333

import anytree
import c_parser
import scanner

def save_parse_tree(program: anytree.Node):
    with open("parse_tree.txt", "w", encoding="utf-8") as parse_tree:
        for pre, _, node in anytree.RenderTree(program):
            parse_tree.write("%s%s\n" % (pre, node.name))


def main():
    # Setup the scanner
    s = scanner.Scanner()
    s.get_input_file("input.txt")
    # Setup the parser
    c_parser.lookahead = s.get_lookahead_token()
    c_parser.get_next_token = s.get_lookahead_token
    c_parser.get_scanner_lookahead = s.get_current_scanner_lookahead_str
    main_program = anytree.Node("main")
    c_parser.S(main_program)
    # Save the parse tree but skip the first two children (main and S)
    save_parse_tree(main_program.children[0].children[0])

if __name__ == "__main__":
    main()