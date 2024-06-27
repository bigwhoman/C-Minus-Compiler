from typing import Union
import scanner
from enum import Enum

class Constants(Enum):
    INT_TYPE = 1
    VOID_TYPE = 2

class VariableType(Enum):
    """
    Type of the variable in symbol table
    """

    INT = 1
    INT_ARRAY = 2
    VOID_FUNCTION = 3
    INT_FUNCTION = 4

class SymbolTableEntry:
    """
    Each entry in the symbol table has this type
    """

    def __init__(self, lexeme: str, var_type: VariableType, parameters: Union[list[VariableType], int, None]):
        self.lexeme = lexeme
        self.var_type = var_type
        # List of parameters for function or the size of array
        self.parameters = parameters
        # The address is either the absolute address if this is global variable.
        # Otherwise it is the offset of this variable from top of the stack.
        self.address = 0

class ThreeAddressInstructionNumberType(Enum):
    DIRECT_ADDRESS = 1
    IMMEDIATE = 2
    INDIRECT_ADDRESS = 3

class ThreeAddressInstructionOperand:
    """
    Each operand of each instruction must be this type
    """
    def __init__(self, value: int, number_type: ThreeAddressInstructionNumberType):
        self.value = value
        self.number_type = number_type

    def __str__(self) -> str:
        if self.number_type == ThreeAddressInstructionNumberType.DIRECT_ADDRESS:
            return str(self.value)
        elif self.number_type == ThreeAddressInstructionNumberType.IMMEDIATE:
            return "#" + str(self.value)
        elif self.number_type == ThreeAddressInstructionNumberType.INDIRECT_ADDRESS:
            return "@" + str(self.value)

class ThreeAddressInstructionOpcode(Enum):
    ADD = 1
    MULT = 2
    SUB = 3
    EQ = 4
    LT = 5
    ASSIGN = 6
    JPF = 7
    JP = 8
    PRINT = 9

class ThreeAddressInstruction:
    """
    Each emitted instruction should be this type
    """

    def __init__(
        self,
        opcode: ThreeAddressInstructionOpcode,
        operands: list[ThreeAddressInstructionOperand],
    ):
        self.opcode = opcode
        self.operands = operands

    def __str__(self) -> str:
        to_join = [str(self.opcode)]
        for operand in self.operands:
            to_join.append(str(operand))
        while len(to_join) != 4:
            to_join.append("")
        return "(" + ", ".join(to_join) + ")"

class SemanticAnalyzer:
    def __init__(self):
        # A stack which each entry contains a list of variables in a scope
        self.scope_stack: list[list[SymbolTableEntry]] = []
        self.error_list: list[str] = []

    def enter_scope(self):
        self.scope_stack.append({})
    
    def exit_scope(self):
        self.scope_stack.pop()

    def declared_before(self, lexeme: str) -> Union[SymbolTableEntry, None]:
        """
        Checks if a lexeme has been defined before and returns it if it has
        """
        for scope in self.scope_stack:
            for entry in scope:
                if lexeme == entry.lexeme:
                    return entry
        return None

    def declare_variable(self, name: str):
        """
        Declare a new int variable in the current scope
        """
        assert not self.declared_before(name)
        self.scope_stack[-1].append(SymbolTableEntry(name, VariableType.INT, None))
    
    def declare_array(self, name: str, size: int):
        """
        Declare a new int array in the current scope
        """
        assert not self.declared_before(name)
        self.scope_stack[-1].append(SymbolTableEntry(name, VariableType.INT_ARRAY, size))

    def declare_function(self, name: str, return_type: Constants, start_address: int):
        """
        Declare a new int array in the current scope
        """
        assert not self.declared_before(name)
        # Convert type on stack to function type
        if return_type == Constants.INT_TYPE:
            function_type = VariableType.INT_FUNCTION
        elif return_type == Constants.VOID_TYPE:
            function_type = VariableType.VOID_FUNCTION
        else:
            raise Exception("RIDEMAN BOZORG")
        # Create entry
        entry = SymbolTableEntry(name, function_type, [])
        entry.address = start_address
        self.scope_stack[-1].append(entry)

    def declare_old_function_arguments(self, arguments: list[VariableType]):
        """
        After the arguments of a function has been parsed, this method is called to fix them
        in the scope stack for semantic analyzer
        """
        # Check if everything is correct and we are actually modifying a function
        assert self.scope_stack[-2][-1].var_type in [VariableType.INT_FUNCTION, VariableType.VOID_FUNCTION]
        # Set the params
        self.scope_stack[-2][-1].parameters = arguments
    

class CodeGenerator:
    FIRST_GLOBAL_VARIABLE_ADDRESS = 100
    STACK_POINTER_ADDRESS = FIRST_GLOBAL_VARIABLE_ADDRESS
    FIRST_TEMP_VARIABLE_ADDRESS = 500
    TOP_STACK_ADDRESS = 1000

    def __init__(self, scanner: scanner.Scanner):
        self.ss: list[int] = []  # Semantic stack
        self.scanner = scanner
        self.semantic_analyzer = SemanticAnalyzer()
        # We always define stack pointer the first global variable
        self.declared_global_variables = 1
        self.pc = 1  # Program counter
        self.program_block: list[ThreeAddressInstruction] = []
        # Name of the variable we are declaring
        self.declaring_pid_value: Union[None, str] = None
        # List of parameters of function we are declaring
        self.declaring_function_params: Union[None, list[VariableType]] = None

    def int_type(self):
        self.ss.append(int(Constants.INT_TYPE))

    def void_type(self):
        self.ss.append(int(Constants.VOID_TYPE))

    def declaring_pid(self):
        assert self.scanner.lookahead_token[0] == scanner.TokenType.ID
        assert self.declaring_pid_value == None
        self.declaring_pid_value = self.scanner.lookahead_token[1]

    def variable_declared(self):
        assert self.declaring_pid_value != None
        # Top of the stack is the variable type
        if self.ss[-1] == int(Constants.INT_TYPE):
            self.semantic_analyzer.declare_variable(self.declaring_pid_value)
            if len(self.semantic_analyzer.scope_stack) == 1: # is this a global variable?
                # The addressing is absolute. Assign the address to it
                self.semantic_analyzer.scope_stack[0][self.declaring_pid_value].address = self.FIRST_GLOBAL_VARIABLE_ADDRESS + self.declared_global_variables * 4
                self.declared_global_variables += 1
        elif self.ss[-1] == int(Constants.VOID_TYPE):
            self.semantic_analyzer.error_list.append(f"#{self.scanner.line_number}: Semantic Error! Illegal type of void for '{self.declaring_pid_value}'")
        else:
            raise Exception("RIDEMAN BOZORG")
        # Empty stack
        self.ss.pop()
        self.declaring_pid_value = None

    def array_size(self):
        assert self.scanner.lookahead_token[0] == scanner.TokenType.NUM
        self.ss.append(self.scanner.lookahead_token[1])

    def array_declared(self):
        assert self.declaring_pid_value != None
        # Top of the stack is the size of array
        size_of_array = self.ss.pop()
        # Top of the stack is the variable type
        if self.ss[-1] == int(Constants.INT_TYPE):
            self.semantic_analyzer.declare_array(self.declaring_pid_value, size_of_array)
            if len(self.semantic_analyzer.scope_stack) == 1: # is this a global variable?
                raise Exception("TODO")
        elif self.ss[-1] == int(Constants.VOID_TYPE):
            self.semantic_analyzer.error_list.append(f"#{self.scanner.line_number}: Semantic Error! Illegal type of void for '{self.declaring_pid_value}'")
        else:
            raise Exception("RIDEMAN BOZORG")
        # Empty stack
        self.ss.pop()
        self.declaring_pid_value = None

    def function_start(self):
        """
        This language is simple and we only declare scopes in functions
        """
        assert self.declaring_pid_value != None
        assert self.declaring_function_params != None
        return_type = self.ss.pop()
        assert return_type in [int(Constants.INT_TYPE), int(Constants.VOID_TYPE)]
        self.semantic_analyzer.declare_function(self.declaring_pid_value, return_type)
        self.declaring_function_params = [] # create a fresh list of parameters
        self.semantic_analyzer.enter_scope()

    def scalar_param(self):
        """
        If we see an scalar parameter, just declare it as a variable.
        Everything is pass by reference
        """
        assert self.declaring_pid_value != None
        assert self.declaring_function_params != None
        self.semantic_analyzer.declare_variable(self.declaring_pid_value)
        self.declaring_function_params.append(VariableType.INT)
        self.declaring_pid_value = None

    def array_param(self):
        """
        If we see an array parameter, just declare it as a pointer to array.
        """
        assert self.declaring_pid_value != None
        assert self.declaring_function_params != None
        self.semantic_analyzer.declare_array(self.declaring_pid_value, 0) # 0 is N/A
        self.declaring_function_params.append(VariableType.INT_ARRAY)
        self.declaring_pid_value = None

    def function_params_end(self):
        """
        When the parameters end, we save the function in the symbol table
        """
        assert self.declaring_function_params != None
        self.semantic_analyzer.declare_old_function_arguments(self.declaring_function_params)
        self.declaring_function_params = None # reset everything
    
    def function_end(self):
        self.semantic_analyzer.exit_scope()

    def pop_int_type(self):
        assert self.ss.pop() == int(Constants.INT_TYPE)