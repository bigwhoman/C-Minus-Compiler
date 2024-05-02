lookahead = ""
def dummy_get_next_token():
	raise Exception("Please implement")
get_next_token = dummy_get_next_token # override this first class function

def Match(expected_token : str) :
    global lookahead
    print("Matching", expected_token)
    if lookahead == expected_token :
        lookahead = get_next_token()
    else :
        print("Missing input ...")

def S() :
	global lookahead
    
	if lookahead in ['$', 'int', 'void'] :
		Program()
		Match('$')


	if lookahead in ['ID', ';', '[', 'NUM', ']', '(', ')', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		S()


    

def Program() :
	global lookahead
    
	if lookahead in ['$', 'int', 'void'] :
		Declaration_list()


	if lookahead in ['ID', ';', '[', 'NUM', ']', '(', ')', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Program()


    

def Declaration_list() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		return


	if lookahead in ['[', ']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Declaration_list()


	if lookahead in ['int', 'void'] :
		Declaration()
		Declaration_list()


    

def Declaration() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['[', ']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Declaration()


	if lookahead in ['int', 'void'] :
		Declaration_initial()
		Declaration_prime()


    

def Declaration_initial() :
	global lookahead
    
	if lookahead in ['$', 'ID', 'NUM', ']', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Declaration_initial()


	if lookahead in [';', '[', '(', ')', ','] :

		print('Missing character at ...')
		return


	if lookahead in ['int', 'void'] :
		Type_specifier()
		Match('ID')


    

def Declaration_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in [';', '['] :
		Var_declaration_prime()


	if lookahead in [']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Declaration_prime()


	if lookahead in ['('] :
		Fun_declaration_prime()


    

def Var_declaration_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in [';'] :
		Match(';')


	if lookahead in ['['] :
		Match('[')
		Match('NUM')
		Match(']')
		Match(';')


	if lookahead in [']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Var_declaration_prime()


    

def Fun_declaration_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['[', ']', ')', ',', 'endif', 'else', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Fun_declaration_prime()


	if lookahead in ['('] :
		Match('(')
		Params()
		Match(')')
		Compound_stmt()


    

def Type_specifier() :
	global lookahead
    
	if lookahead in ['$', ';', '[', 'NUM', ']', '(', ')', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Type_specifier()


	if lookahead in ['ID'] :

		print('Missing character at ...')
		return


	if lookahead in ['int'] :
		Match('int')


	if lookahead in ['void'] :
		Match('void')


    

def Params() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Params()


	if lookahead in [')'] :

		print('Missing character at ...')
		return


	if lookahead in ['int'] :
		Match('int')
		Match('ID')
		Param_prime()
		Param_list()


	if lookahead in ['void'] :
		Match('void')


    

def Param_list() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Param_list()


	if lookahead in [')'] :

		return


	if lookahead in [','] :
		Param()
		Param_list()


    

def Param() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Param()


	if lookahead in [')', ','] :

		print('Missing character at ...')
		return


	if lookahead in ['int', 'void'] :
		Declaration_initial()
		Param_prime()


    

def Param_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', 'NUM', ']', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Param_prime()


	if lookahead in ['['] :
		Match('[')
		Match(']')


	if lookahead in [')', ','] :

		return


    

def Compound_stmt() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['[', ']', ')', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Compound_stmt()


	if lookahead in ['{'] :
		Match('{')
		Declaration_list()
		Statement_list()
		Match('}')


    

def Statement_list() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', 'endif', 'else', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Statement_list()


	if lookahead in ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'for', 'return', '+', '-'] :
		Statement()
		Statement_list()


	if lookahead in ['}'] :

		return


    

def Statement() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Statement()


	if lookahead in ['ID', ';', 'NUM', '(', 'break', '+', '-'] :
		Expression_stmt()


	if lookahead in ['{'] :
		Compound_stmt()


	if lookahead in ['}', 'endif', 'else'] :

		print('Missing character at ...')
		return


	if lookahead in ['if'] :
		Selection_stmt()


	if lookahead in ['for'] :
		Iteration_stmt()


	if lookahead in ['return'] :
		Return_stmt()


    

def Expression_stmt() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Expression_stmt()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Expression()
		Match(';')


	if lookahead in [';'] :
		Match(';')


	if lookahead in ['{', '}', 'if', 'endif', 'else', 'for', 'return'] :

		print('Missing character at ...')
		return


	if lookahead in ['break'] :
		Match('break')
		Match(';')


    

def Selection_stmt() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Selection_stmt()


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'endif', 'else', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['if'] :
		Match('if')
		Match('(')
		Expression()
		Match(')')
		Statement()
		Else_stmt()


    

def Else_stmt() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Else_stmt()


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['endif'] :
		Match('endif')


	if lookahead in ['else'] :
		Match('else')
		Statement()
		Match('endif')


    

def Iteration_stmt() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Iteration_stmt()


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'return', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['for'] :
		Match('for')
		Match('(')
		Expression()
		Match(';')
		Expression()
		Match(';')
		Expression()
		Match(')')
		Statement()


    

def Return_stmt() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Return_stmt()


	if lookahead in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'for', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['return'] :
		Match('return')
		Return_stmt_prime()


    

def Return_stmt_prime() :
	global lookahead
    
	if lookahead in ['$', '[', ']', ')', 'int', 'void', ',', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Return_stmt_prime()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Expression()
		Match(';')


	if lookahead in [';'] :
		Match(';')


	if lookahead in ['{', '}', 'break', 'if', 'endif', 'else', 'for', 'return'] :

		print('Missing character at ...')
		return


    

def Expression() :
	global lookahead
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Expression()


	if lookahead in ['ID'] :
		Match('ID')
		B()


	if lookahead in [';', ']', ')', ','] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Simple_expression_zegond()


    

def B() :
	global lookahead
    
	if lookahead in ['$', 'ID', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		B()


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Simple_expression_prime()


	if lookahead in ['['] :
		Match('[')
		Expression()
		Match(']')
		H()


	if lookahead in ['='] :
		Match('=')
		Expression()


    

def H() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		H()


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :
		G()
		D()
		C()


	if lookahead in ['='] :
		Match('=')
		Expression()


    

def Simple_expression_zegond() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Simple_expression_zegond()


	if lookahead in [';', ']', ')', ','] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Additive_expression_zegond()
		C()


    

def Simple_expression_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Simple_expression_prime()


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Additive_expression_prime()
		C()


    

def C() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		C()


	if lookahead in [';', ']', ')', ','] :

		return


	if lookahead in ['<', '=='] :
		Relop()
		Additive_expression()


    

def Relop() :
	global lookahead
    
	if lookahead in ['$', ';', '[', ']', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Relop()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :

		print('Missing character at ...')
		return


	if lookahead in ['<'] :
		Match('<')


	if lookahead in ['=='] :
		Match('==')


    

def Additive_expression() :
	global lookahead
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Additive_expression()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Term()
		D()


	if lookahead in [';', ']', ')', ','] :

		print('Missing character at ...')
		return


    

def Additive_expression_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Additive_expression_prime()


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Term_prime()
		D()


    

def Additive_expression_zegond() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Additive_expression_zegond()


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Term_zegond()
		D()


    

def D() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		D()


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		return


	if lookahead in ['+', '-'] :
		Addop()
		Term()
		D()


    

def Addop() :
	global lookahead
    
	if lookahead in ['$', ';', '[', ']', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Addop()


	if lookahead in ['ID', 'NUM', '('] :

		print('Missing character at ...')
		return


	if lookahead in ['+'] :
		Match('+')


	if lookahead in ['-'] :
		Match('-')


    

def Term() :
	global lookahead
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Term()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Signed_factor()
		G()


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		print('Missing character at ...')
		return


    

def Term_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Term_prime()


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Signed_factor_prime()
		G()


    

def Term_zegond() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Term_zegond()


	if lookahead in [';', ']', ')', ',', '<', '=='] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM', '(', '+', '-'] :
		Signed_factor_zegond()
		G()


    

def G() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		G()


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-'] :

		return


	if lookahead in ['*'] :
		Match('*')
		Signed_factor()
		G()


    

def Signed_factor() :
	global lookahead
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Signed_factor()


	if lookahead in ['ID', 'NUM', '('] :
		Factor()


	if lookahead in [';', ']', ')', ',', '<', '==', '*'] :

		print('Missing character at ...')
		return


	if lookahead in ['+'] :
		Match('+')
		Factor()


	if lookahead in ['-'] :
		Match('-')
		Factor()


    

def Signed_factor_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Signed_factor_prime()


	if lookahead in [';', ']', '(', ')', ',', '<', '==', '+', '-', '*'] :
		Factor_prime()


    

def Signed_factor_zegond() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Signed_factor_zegond()


	if lookahead in [';', ']', ')', ',', '<', '==', '*'] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM', '('] :
		Factor_zegond()


	if lookahead in ['+'] :
		Match('+')
		Factor()


	if lookahead in ['-'] :
		Match('-')
		Factor()


    

def Factor() :
	global lookahead
    
	if lookahead in ['$', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Factor()


	if lookahead in ['ID'] :
		Match('ID')
		Var_call_prime()


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM'] :
		Match('NUM')


	if lookahead in ['('] :
		Match('(')
		Expression()
		Match(')')


    

def Var_call_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Var_call_prime()


	if lookahead in [';', '[', ']', ')', ',', '<', '==', '+', '-', '*'] :
		Var_prime()


	if lookahead in ['('] :
		Match('(')
		Args()
		Match(')')


    

def Var_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Var_prime()


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		return


	if lookahead in ['['] :
		Match('[')
		Expression()
		Match(']')


    

def Factor_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'NUM', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Factor_prime()


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		return


	if lookahead in ['('] :
		Match('(')
		Args()
		Match(')')


    

def Factor_zegond() :
	global lookahead
    
	if lookahead in ['$', 'ID', '[', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '='] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Factor_zegond()


	if lookahead in [';', ']', ')', ',', '<', '==', '+', '-', '*'] :

		print('Missing character at ...')
		return


	if lookahead in ['NUM'] :
		Match('NUM')


	if lookahead in ['('] :
		Match('(')
		Expression()
		Match(')')


    

def Args() :
	global lookahead
    
	if lookahead in ['$', ';', '[', ']', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Args()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Arg_list()


	if lookahead in [')'] :

		return


    

def Arg_list() :
	global lookahead
    
	if lookahead in ['$', ';', '[', ']', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Arg_list()


	if lookahead in ['ID', 'NUM', '(', '+', '-'] :
		Expression()
		Arg_list_prime()


	if lookahead in [')'] :

		print('Missing character at ...')
		return


    

def Arg_list_prime() :
	global lookahead
    
	if lookahead in ['$', 'ID', ';', '[', 'NUM', ']', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*'] :

		print('Invalid character at ...')
		lookahead = get_next_token()
		Arg_list_prime()


	if lookahead in [')'] :

		return


	if lookahead in [','] :
		Expression()
		Arg_list_prime()


    
