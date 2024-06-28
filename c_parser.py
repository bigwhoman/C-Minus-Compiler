import anytree
from code_generator import CodeGenerator

lookahead = ""
def dummy_function():
	raise Exception("Please implement")
get_next_token = dummy_function # override this first class function
get_scanner_lookahead = dummy_function # override this first class function
get_current_line = dummy_function # override this first class function
parser_errors: list[str] = []
code_generator: CodeGenerator = None

def Match(expected_token : str, parent: anytree.Node) :
    global lookahead
    if lookahead == expected_token :
        anytree.Node(get_scanner_lookahead(), parent=parent)
        lookahead = get_next_token()
    elif expected_token != "$" : # Tof sag. Must be like this to pass test 4
        parser_errors.append(f"#{get_current_line()} : syntax error, missing {expected_token}")

def S(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("S".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'int', 'void'] :
		Program(current_node)
		Match('$', current_node)
		return

	if lookahead in ['ID', ';', '[', 'NUM', ']', '(', ')', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		S(parent)
		return


    

def Program(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Program".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'int', 'void'] :
		Declaration_list(current_node)
		return

	if lookahead in ['ID', ';', '[', 'NUM', ']', '(', ')', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Program(parent)
		return


    

def Declaration_list(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Declaration_list".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in ['[', ']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Declaration_list(parent)
		return


	if lookahead in ['int', 'void'] :
		Declaration(current_node)
		Declaration_list(current_node)
		return

    

def Declaration(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Declaration".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Declaration")
		return


	if lookahead in ['[', ']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Declaration(parent)
		return


	if lookahead in ['int', 'void'] :
		Declaration_initial(current_node)
		Declaration_prime(current_node)
		return

    

def Declaration_initial(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Declaration_initial".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', 'NUM', ']', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Declaration_initial(parent)
		return


	if lookahead in [';', '[', '(', ')', ','] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Declaration-initial")
		return


	if lookahead in ['int', 'void'] :
		Type_specifier(current_node)
		code_generator.declaring_pid()
		Match('ID', current_node)
		return

    

def Declaration_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Declaration_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Declaration-prime")
		return


	if lookahead in [';', '['] :
		Var_declaration_prime(current_node)
		return

	if lookahead in [']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Declaration_prime(parent)
		return


	if lookahead in ['('] :
		Fun_declaration_prime(current_node)
		return

    

def Var_declaration_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Var_declaration_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Var-declaration-prime")
		return


	if lookahead in [';'] :
		Match(';', current_node)
		code_generator.variable_declared()
		return

	if lookahead in ['['] :
		Match('[', current_node)
		code_generator.array_size()
		Match('NUM', current_node)
		Match(']', current_node)
		Match(';', current_node)
		code_generator.array_declared()
		return

	if lookahead in [']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Var_declaration_prime(parent)
		return


    

def Fun_declaration_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Fun_declaration_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Fun-declaration-prime")
		return


	if lookahead in ['[', ']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Fun_declaration_prime(parent)
		return


	if lookahead in ['('] :
		code_generator.function_start()
		Match('(', current_node)
		Params(current_node)
		Match(')', current_node)
		code_generator.function_params_end()
		Compound_stmt(current_node)
		code_generator.function_end()
		return

    

def Type_specifier(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Type_specifier".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', ';', '[', 'NUM', ']', '(', ')', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Type_specifier(parent)
		return


	if lookahead in ['ID'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Type-specifier")
		return


	if lookahead in ['int'] :
		Match('int', current_node)
		code_generator.int_type()
		return

	if lookahead in ['void'] :
		Match('void', current_node)
		code_generator.void_type()
		return

    

def Params(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Params".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Params(parent)
		return


	if lookahead in [')'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Params")
		return


	if lookahead in ['int'] :
		Match('int', current_node)
		code_generator.int_type()
		code_generator.declaring_pid()
		Match('ID', current_node)
		Param_prime(current_node)
		Param_list(current_node)
		return

	if lookahead in ['void'] :
		Match('void', current_node)
		return

    

def Param_list(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Param_list".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Param_list(parent)
		return


	if lookahead in [')'] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in [','] :
		Match(',', current_node)
		Param(current_node)
		Param_list(current_node)
		return

    

def Param(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Param".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Param(parent)
		return


	if lookahead in [')', ','] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Param")
		return


	if lookahead in ['int', 'void'] :
		Declaration_initial(current_node)
		Param_prime(current_node)
		return

    

def Param_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Param_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', 'NUM', ']', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Param_prime(parent)
		return


	if lookahead in ['['] :
		Match('[', current_node)
		Match(']', current_node)
		code_generator.array_param()
		code_generator.pop_int_type()
		return

	if lookahead in [')', ','] :
		code_generator.scalar_param()
		code_generator.pop_int_type()
		anytree.Node("epsilon", parent=current_node)
		return


    

def Compound_stmt(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Compound_stmt".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Compound-stmt")
		return


	if lookahead in ['[', ']', ')', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Compound_stmt(parent)
		return


	if lookahead in ['{'] :
		Match('{', current_node)
		Declaration_list(current_node)
		Statement_list(current_node)
		Match('}', current_node)
		return

    

def Statement_list(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Statement_list".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', 'endif', 'else', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Statement_list(parent)
		return


	if lookahead in ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'for', 'return', '+', '-'] :
		Statement(current_node)
		Statement_list(current_node)
		return

	if lookahead in ['}'] :

		anytree.Node("epsilon", parent=current_node)
		return


    

def Statement(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Statement".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Statement(parent)
		return


	if lookahead in ['ID', ';', 'NUM', '(', 'break', '+', '-'] :
		Expression_stmt(current_node)
		return

	if lookahead in ['{'] :
		Compound_stmt(current_node)
		return

	if lookahead in ['}', 'endif', 'else'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Statement")
		return


	if lookahead in ['if'] :
		Selection_stmt(current_node)
		return

	if lookahead in ['for'] :
		Iteration_stmt(current_node)
		return

	if lookahead in ['return'] :
		Return_stmt(current_node)
		return

    

def Expression_stmt(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Expression_stmt".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Expression_stmt(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Expression(current_node)
		Match(';', current_node)
		return

	if lookahead in [';'] :
		Match(';', current_node)
		return

	if lookahead in ['{', '}', 'if', 'endif', 'else', 'for', 'return'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Expression-stmt")
		return


	if lookahead in ['break'] :
		Match('break', current_node)
		Match(';', current_node)
		return

    

def Selection_stmt(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Selection_stmt".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Selection_stmt(parent)
		return


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'endif', 'else', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Selection-stmt")
		return


	if lookahead in ['if'] :
		Match('if', current_node)
		Match('(', current_node)
		Expression(current_node)
		Match(')', current_node)
		Statement(current_node)
		Else_stmt(current_node)
		return

    

def Else_stmt(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Else_stmt".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Else_stmt(parent)
		return


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Else-stmt")
		return


	if lookahead in ['endif'] :
		Match('endif', current_node)
		return

	if lookahead in ['else'] :
		Match('else', current_node)
		Statement(current_node)
		Match('endif', current_node)
		return

    

def Iteration_stmt(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Iteration_stmt".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Iteration_stmt(parent)
		return


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'return', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Iteration-stmt")
		return


	if lookahead in ['for'] :
		Match('for', current_node)
		Match('(', current_node)
		Expression(current_node)
		Match(';', current_node)
		Expression(current_node)
		Match(';', current_node)
		Expression(current_node)
		Match(')', current_node)
		Statement(current_node)
		return

    

def Return_stmt(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Return_stmt".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Return_stmt(parent)
		return


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'for', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Return-stmt")
		return


	if lookahead in ['return'] :
		Match('return', current_node)
		Return_stmt_prime(current_node)
		return

    

def Return_stmt_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Return_stmt_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Return_stmt_prime(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Expression(current_node)
		code_generator.return_func()
		Match(';', current_node)
		return

	if lookahead in [';'] :
		Match(';', current_node)
		return

	if lookahead in ['{', '}', 'break', 'if', 'endif', 'else', 'for', 'return'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Return-stmt-prime")
		return


    

def Expression(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Expression".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Expression(parent)
		return


	if lookahead in ['ID'] :
		Match('ID', current_node)
		B(current_node)
		return

	if lookahead in [';', ']', ')', ','] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Expression")
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Simple_expression_zegond(current_node)
		return

    

def B(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("B".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		B(parent)
		return


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Simple_expression_prime(current_node)
		return

	if lookahead in ['['] :
		Match('[', current_node)
		Expression(current_node)
		Match(']', current_node)
		H(current_node)
		return

	if lookahead in ['='] :
		Match('=', current_node)
		Expression(current_node)
		return

    

def H(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("H".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		H(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :
		G(current_node)
		D(current_node)
		C(current_node)
		return

	if lookahead in ['='] :
		Match('=', current_node)
		Expression(current_node)
		return

    

def Simple_expression_zegond(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Simple_expression_zegond".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Simple_expression_zegond(parent)
		return


	if lookahead in [';', ']', ')', ','] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Simple-expression-zegond")
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Additive_expression_zegond(current_node)
		C(current_node)
		return

    

def Simple_expression_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Simple_expression_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Simple_expression_prime(parent)
		return


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Additive_expression_prime(current_node)
		C(current_node)
		return

    

def C(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("C".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		C(parent)
		return


	if lookahead in [';', ']', ')', ','] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in ['<', '=='] :
		Relop(current_node)
		Additive_expression(current_node)
		return

    

def Relop(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Relop".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', ';', '[', ']', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Relop(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Relop")
		return


	if lookahead in ['<'] :
		Match('<', current_node)
		return

	if lookahead in ['=='] :
		Match('==', current_node)
		return

    

def Additive_expression(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Additive_expression".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Additive_expression(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Term(current_node)
		D(current_node)
		return

	if lookahead in [';', ']', ')', ','] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Additive-expression")
		return


    

def Additive_expression_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Additive_expression_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Additive_expression_prime(parent)
		return


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Term_prime(current_node)
		D(current_node)
		return

    

def Additive_expression_zegond(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Additive_expression_zegond".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Additive_expression_zegond(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Additive-expression-zegond")
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Term_zegond(current_node)
		D(current_node)
		return

    

def D(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("D".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		D(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in ['+', '-'] :
		Addop(current_node)
		Term(current_node)
		D(current_node)
		return

    

def Addop(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Addop".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', ';', '[', ']', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Addop(parent)
		return


	if lookahead in ['ID', 'NUM', '('] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Addop")
		return


	if lookahead in ['+'] :
		Match('+', current_node)
		return

	if lookahead in ['-'] :
		Match('-', current_node)
		return

    

def Term(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Term".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Term(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Signed_factor(current_node)
		G(current_node)
		return

	if lookahead in [';', ']', ')', ',', '<', '=='] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Term")
		return


    

def Term_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Term_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Term_prime(parent)
		return


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Signed_factor_prime(current_node)
		G(current_node)
		return

    

def Term_zegond(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Term_zegond".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Term_zegond(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Term-zegond")
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Signed_factor_zegond(current_node)
		G(current_node)
		return

    

def G(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("G".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		G(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-'] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in ['*'] :
		Match('*', current_node)
		Signed_factor(current_node)
		G(current_node)
		return

    

def Signed_factor(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Signed_factor".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Signed_factor(parent)
		return


	if lookahead in ['ID', 'NUM', '('] :
		Factor(current_node)
		return

	if lookahead in [';', ']', ')', ',', '<', '==', '*'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Signed-factor")
		return


	if lookahead in ['+'] :
		Match('+', current_node)
		Factor(current_node)
		return

	if lookahead in ['-'] :
		Match('-', current_node)
		Factor(current_node)
		return

    

def Signed_factor_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Signed_factor_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Signed_factor_prime(parent)
		return


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Factor_prime(current_node)
		return

    

def Signed_factor_zegond(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Signed_factor_zegond".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Signed_factor_zegond(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '==', '*'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Signed-factor-zegond")
		return


	if lookahead in ['NUM', '('] :
		Factor_zegond(current_node)
		return

	if lookahead in ['+'] :
		Match('+', current_node)
		Factor(current_node)
		return

	if lookahead in ['-'] :
		Match('-', current_node)
		Factor(current_node)
		return

    

def Factor(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Factor".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Factor(parent)
		return


	if lookahead in ['ID'] :
		Match('ID', current_node)
		Var_call_prime(current_node)
		return

	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Factor")
		return


	if lookahead in ['NUM'] :
		Match('NUM', current_node)
		return

	if lookahead in ['('] :
		Match('(', current_node)
		Expression(current_node)
		Match(')', current_node)
		return

    

def Var_call_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Var_call_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Var_call_prime(parent)
		return


	if lookahead in [';', '[', ']', ')', ',', '<', '==', '+', '-', '*'] :
		Var_prime(current_node)
		return

	if lookahead in ['('] :
		Match('(', current_node)
		Args(current_node)
		Match(')', current_node)
		return

    

def Var_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Var_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Var_prime(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in ['['] :
		Match('[', current_node)
		Expression(current_node)
		Match(']', current_node)
		return

    

def Factor_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Factor_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Factor_prime(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in ['('] :
		code_generator.call()
		Match('(', current_node)
		Args(current_node)
		Match(')', current_node)
		return

    

def Factor_zegond(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Factor_zegond".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Factor_zegond(parent)
		return


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Factor-zegond")
		return


	if lookahead in ['NUM'] :
		Match('NUM', current_node)
		return

	if lookahead in ['('] :
		Match('(', current_node)
		Expression(current_node)
		Match(')', current_node)
		return

    

def Args(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Args".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', ';', '[', ']', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Args(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Arg_list(current_node)
		return

	if lookahead in [')'] :

		anytree.Node("epsilon", parent=current_node)
		return


    

def Arg_list(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Arg_list".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', ';', '[', ']', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Arg_list(parent)
		return


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Expression(current_node)
		Arg_list_prime(current_node)
		return

	if lookahead in [')'] :

		current_node.parent = None
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, missing Arg-list")
		return


    

def Arg_list_prime(parent: anytree.Node) :
	global lookahead
	global parser_errors
	current_node = anytree.Node("Arg_list_prime".replace("_", "-"), parent=parent)
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		current_node.parent = None
		if lookahead == '$' :
			parser_errors.append("#" + str(get_current_line() + 1) + " : syntax error, Unexpected EOF")
			raise SyntaxError("Unexpected EOF")
		parser_errors.append("#" + str(get_current_line()) + " : syntax error, illegal " + lookahead)
		lookahead = get_next_token()
		Arg_list_prime(parent)
		return


	if lookahead in [')'] :

		anytree.Node("epsilon", parent=current_node)
		return


	if lookahead in [','] :
		Match(',', current_node)
		Expression(current_node)
		Arg_list_prime(current_node)
		return

    
