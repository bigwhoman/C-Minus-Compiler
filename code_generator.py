from typing import Union
import scanner
from enum import Enum, IntEnum

class Constants(IntEnum):
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
        self.address = -1

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"({self.lexeme}, {self.var_type}, {self.parameters}, {self.address})"

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
    
    def __repr__(self) -> str:
        return str(self)

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
        self.scope_stack: list[list[SymbolTableEntry]] = [[]]
        self.error_list: list[str] = []

    def enter_scope(self):
        self.scope_stack.append([])
    
    def exit_scope(self):
        self.scope_stack.pop()

    def get_entry(self, lexeme: str) -> Union[SymbolTableEntry, None]:
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
        assert not self.get_entry(name)
        self.scope_stack[-1].append(SymbolTableEntry(name, VariableType.INT, None))
    
    def declare_array(self, name: str, size: int):
        """
        Declare a new int array in the current scope
        """
        assert not self.get_entry(name)
        self.scope_stack[-1].append(SymbolTableEntry(name, VariableType.INT_ARRAY, size))

    def declare_function(self, name: str, return_type: Constants, start_address: int):
        """
        Declare a new int array in the current scope
        """
        assert not self.get_entry(name)
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

    def assign_scope_addresses(self):
        """
        Assign the addresses to scope variables.

        This is done by iterating over all previous variables and increasing an offset
        """
        scope = self.scope_stack[-1]
        if len(scope) == 0: # welp...
            return
        if scope[0].address != -1: # we have already assigned the addresses
            # We reach here in for/if statements
            return
        # We should assign addresses
        declared_variable_count = 0
        for entry in scope:
            assert entry.address == -1 # nothing should be assigned
            if entry.var_type == VariableType.INT:
                entry.address = declared_variable_count * 4 # each variable is 4 bytes
                declared_variable_count += 1
            elif entry.var_type == VariableType.INT_ARRAY:
                # In case of array we should declare a space for array pointer
                entry.address = declared_variable_count * 4 # pointer is 4 bytes
                declared_variable_count += 1
                if entry.parameters != -1: # -1 is when this is the argument
                    declared_variable_count += entry.parameters # get space just after the pointer
            else:
                raise Exception("SHASH AZIM")
    
    def get_temp(self) -> int:
        """
        Gets the offset of a temporary variables from top of the stack
        """
        if len(self.scope_stack[-1]) == 0:
            tmp_address = 0
        else:
            tmp_address = self.scope_stack[-1][-1].address + 4
        self.scope_stack[-1].append(SymbolTableEntry("_temp_var", VariableType.INT, None))
        self.scope_stack[-1][-1].address = tmp_address


class ProgramBlock:
    def __init__(self):
        self.program_block: list[ThreeAddressInstruction] = []
        self.pc = 1
        # Create a file for program blocks
        self.program = open("./PB.txt","w")

    def add_instruction(self,ThreeAddressInstruction, i=None):
        print(ThreeAddressInstruction)
        # Add instruction to program block 
        if i == None :
            self.program_block.append(ThreeAddressInstruction)
            self.pc += 1
        else :
            self.program_block[i] = ThreeAddressInstruction

    
    def get_pc(self) -> int :
        return self.pc

class StackPointer():
    TOP_STACK_ADDRESS = 2000
    STACK_POINTER_ADDRESS = 100
    def __init__(self):
        self.pointer = self.TOP_STACK_ADDRESS
        self.address = self.STACK_POINTER_ADDRESS

class EAX():
    "General purpose register used for return values"
    EAX_ADDRESS = 104
    def __init__(self):
        self.address = self.EAX_ADDRESS

class RAX():
    "General purpose register"
    RAX_ADDRESS = 108
    def __init__(self):
        self.address = self.RAX_ADDRESS

class CodeGenerator:
    FIRST_GLOBAL_VARIABLE_ADDRESS = 100
    FIRST_TEMP_VARIABLE_ADDRESS = 500


    def __init__(self, scanner: scanner.Scanner):
        self.ss: list[int] = []  # Semantic stack
        self.scanner = scanner
        self.semantic_analyzer = SemanticAnalyzer()
        self.program_block = ProgramBlock()
        # We always define stack pointer the first global variable
        self.declared_global_variables = 1
        # Name of the variable we are declaring
        self.declaring_pid_value: Union[None, str] = None
        # List of parameters of function we are declaring
        self.declaring_function_params: Union[None, list[VariableType]] = None
        # Setup Stack Pointer
        self.sp = StackPointer()
        # Setup EAX 
        self.eax = EAX()
        # Setup RAX
        self.rax = RAX()
        # initiallize Stack pointer and EAX
        self.initiallize()

    def initiallize(self) :
            self.program_block.add_instruction(
                                ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                            [ThreeAddressInstructionOperand(self.sp.pointer,ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                ThreeAddressInstructionOperand(self.sp.address,ThreeAddressInstructionNumberType.DIRECT_ADDRESS)]))
            self.program_block.add_instruction(
                                ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                            [ThreeAddressInstructionOperand(0,ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                ThreeAddressInstructionOperand(self.eax.address,ThreeAddressInstructionNumberType.DIRECT_ADDRESS)]))
            self.program_block.add_instruction(
                                ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                            [ThreeAddressInstructionOperand(0,ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                ThreeAddressInstructionOperand(self.rax.address,ThreeAddressInstructionNumberType.DIRECT_ADDRESS)]))

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
                self.semantic_analyzer.get_entry(self.declaring_pid_value).address = self.FIRST_GLOBAL_VARIABLE_ADDRESS + self.declared_global_variables * 4
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
        assert self.declaring_function_params == None
        return_type = self.ss.pop()
        assert return_type in [int(Constants.INT_TYPE), int(Constants.VOID_TYPE)]
        self.semantic_analyzer.declare_function(self.declaring_pid_value, return_type, self.program_block.get_pc())
        self.declaring_pid_value = None
        self.declaring_function_params = [] # create a fresh list of parameters
        self.semantic_analyzer.enter_scope()

        # When a function starts, we need to modify the stack and stack pointer first
        # We first save the return address and the return program block
        # TODO : When get temp is completed do this 

        # Sp points to the pc 
        self.sp.pointer -= 8
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(8, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        

        # Save the last pc for later use
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.program_block.get_pc(), ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                            ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
        self.sp.pointer -= 4
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        

        # Add memory to stack 
        self.sp.pointer -= 100
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(100, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        return_sp = self.sp.pointer
        return_pc = self.program_block.get_pc() + 1

        
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(return_sp, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                            ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
        self.sp.pointer += 4  
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] )) 
              
        # TODO : Needs to be completed      
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(return_pc, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                            ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
        
        # Skip a block for return value
        self.sp.pointer += 8  
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(8, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
         
        print(self.sp.pointer)
        # Now the stack pointer is pointing at the first local variable
             
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
        """
        When the function ends, we pop the scope and remove the
        block from stack
        """
        self.semantic_analyzer.exit_scope()
        self.sp.pointer -= 4
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        
        # Put the return value in EAX register
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.eax.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
        self.sp.pointer -= 8
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(8, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        
        # Remove the stack block   
        self.sp.pointer += 100
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] )) 
        
         
        self.sp.pointer += 4 
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        print(self.sp.pointer)
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.JP,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)])) 

    def pop_int_type(self):
        assert self.ss.pop() == int(Constants.INT_TYPE)

    def variables_declared(self):
        """
        When the statement of a function is being parsed, after the very first of it, we have declared every
        variable and thus we can assign addresses to them.
        """
        self.semantic_analyzer.assign_scope_addresses()
        # TODO: generate code to assign the address of arrays
