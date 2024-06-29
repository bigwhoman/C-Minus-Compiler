from typing import Union
import scanner
from enum import Enum, IntEnum

class Constants(IntEnum):
    INT_TYPE = 1
    VOID_TYPE = 2

class VariableScope(Enum):
    GLOBAL_VARIABLE = 1
    LOCAL_VARIABLE = 2

class MathOperator(Enum):
    PLUS = 1
    MINUS = 2
    MULT = 3
    LESS_THAN = 4
    EQUALS = 5

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

    def __str__(self):
        return str(self.name)
    
    def __repr__(self) -> str:
        return str(self.name)

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
    
    def is_global_variable(self, lexeme: str) -> bool:
        """
        Checks if a variable is a global variable or not.
        It simply checks if it has been declared in the first scope stack or not.
        """
        for entry in self.scope_stack[0]:
            if lexeme == entry.lexeme:
                return True
        return False

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
        return tmp_address


class ProgramBlock:
    def __init__(self):
        self.program_block: list[ThreeAddressInstruction] = []
        self.pc = 1
        # Create a file for program blocks
        self.program = open("./PB.txt","w")

    def add_instruction(self,ThreeAddressInstruction, i=None, empty=None):
        if empty != None :
            self.pc += 1
            return 
        print(self.pc, ThreeAddressInstruction)
        # Add instruction to program block 
        if i == None :
            self.program_block.append(ThreeAddressInstruction)
            self.pc += 1
        else :
            self.program_block[i] = ThreeAddressInstruction

    
    def get_pc(self) -> int :
        return self.pc

class StackPointer():
    TOP_STACK_ADDRESS = 100000
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

class ARG_MEM():
    "A place to store arguments"
    ADDR = 2000
    def __init__(self):
        self.address = self.ADDR
    def reset(self) : 
        self.address = self.ADDR
class TempRegisters():
    """
    Temp registers required for variable address calculations
    """
    TEMP_R1 = 112
    TEMP_R2 = 116
    TEMP_R3 = 120
    TEMP_R4 = 124

class PC():
    "General purpose register"
    PC_ADDRESS = 128
    def __init__(self):
        self.address = self.PC_ADDRESS

class CodeGenerator:
    FIRST_GLOBAL_VARIABLE_ADDRESS = 100
    FIRST_TEMP_VARIABLE_ADDRESS = 500


    def __init__(self, scanner: scanner.Scanner):
        self.ss: list[int] = [12, 22]  # Semantic stack
        self.scanner = scanner
        self.semantic_analyzer = SemanticAnalyzer()
        self.param_leftover = []
        self.program_block = ProgramBlock()
        self.func_params = 0
        self.arg_mem = ARG_MEM()
        self.arg_num = 0
        # We always define stack pointer the first global variable
        self.declared_global_variables = 10
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
        # Setup temp registers
        self.temp_registers = TempRegisters()
        # Each time we want to push an address into ss, we push if it's global or local
        # in this stack
        self.pid_scope_stack: list[VariableScope] = []
        # Each time we want to push an operator in the stack, instead of pushing it into ss
        # we push it here to make everything clear
        self.operator_stack: list[MathOperator] = []
        # Setup PC
        self.pc = PC()
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
            self.program_block.add_instruction(
                                ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                            [ThreeAddressInstructionOperand(0,ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                ThreeAddressInstructionOperand(self.pc.address,ThreeAddressInstructionNumberType.DIRECT_ADDRESS)]))
           
    
    def find_absolute_address(self, address: int, scope: VariableScope, temp_register: int):
        """
        This function is intended to generate runtime code to move the address of a variable to
        a temporary register.
        """
        if scope == VariableScope.GLOBAL_VARIABLE:
            # In this case, just generate code to move the address to temp register
            self.program_block.add_instruction(ThreeAddressInstruction(
                    # TEMP_REG = #Address
                    ThreeAddressInstructionOpcode.ASSIGN,
                    [
                        ThreeAddressInstructionOperand(address, ThreeAddressInstructionNumberType.IMMEDIATE),
                        ThreeAddressInstructionOperand(temp_register, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                    ]))
        else:
            # Add the stack pointer to the register address and boom
            self.program_block.add_instruction(ThreeAddressInstruction(
                    # TEMP_REG = SP + #Address
                    ThreeAddressInstructionOpcode.ADD,
                    [
                        ThreeAddressInstructionOperand(address, ThreeAddressInstructionNumberType.IMMEDIATE),
                        ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                        ThreeAddressInstructionOperand(temp_register, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                    ]))


    def int_type(self):
        self.ss.append(int(Constants.INT_TYPE))

    def void_type(self):
        self.ss.append(int(Constants.VOID_TYPE))

    def declaring_pid(self):
        """
        Declaring pid is called when we are declaring a new variable. In this case,
        we should keep the pid as string in order to define the variable later.
        """
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
        print("Start Func ----------------")
        self.func_params = 0
        self.param_leftover = []
        # Sp points to the pc 
        self.sp.pointer -= 8
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(8, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        

        # Save the last pc for later use
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.pc.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
        self.sp.pointer -= 4
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))

        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                                                                                ThreeAddressInstructionOperand(self.rax.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        # Add memory to stack 
        self.sp.pointer -= 100
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(100, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))



                
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.rax.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        self.sp.pointer += 4  
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] )) 
              
        # TODO : Needs to be completed      
        # self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
        #                                                                 [ThreeAddressInstructionOperand(return_pc, ThreeAddressInstructionNumberType.IMMEDIATE),
        #                                                                     ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
        
        # Skip a block for return value
        self.sp.pointer += 8  
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(8, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        
        
        print("Shoomb Start +++++++++++++++++++++++++++")
        # Now the stack pointer is pointing at the first local variable
    
    def return_func(self) : 
        "Return value from a fuction"
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))        

        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.ss.pop(), ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                            ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))

        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
    def push_param(self) :
        self.func_params += 1

    def call(self):
        print("Call aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.arg_mem.reset()
        fixed_args = []
        print(self.ss)
        
        for i in range(self.arg_num) :
            fixed_args.append(self.ss.pop())
            # print("sag ", self.pid_scope_stack.pop())
        print(self.ss)
        print(self.pid_scope_stack)
        for i in range(self.arg_num) : 
            self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(fixed_args[len(fixed_args) - 1 - i], ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.arg_mem.address + 4 * i, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))            
        # self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
        #                                                             [ThreeAddressInstructionOperand(self.program_block.get_pc() + 2, ThreeAddressInstructionNumberType.IMMEDIATE),
        #                                                                 ThreeAddressInstructionOperand(self.pc.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))            

        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.program_block.get_pc() + 2, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                            ThreeAddressInstructionOperand(self.pc.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.JP,
                                                                        [ThreeAddressInstructionOperand(self.ss.pop(), ThreeAddressInstructionNumberType.IMMEDIATE)]  ))        
        # print("sag2",self.pid_scope_stack.pop())
        self.arg_num = 0
        print("Shoomb Call aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def push_arg(self):
        self.arg_num += 1
        

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
        print("Func par end 4444444444444444444444444444")
        assert self.declaring_function_params != None
        self.semantic_analyzer.declare_old_function_arguments(self.declaring_function_params)
        self.declaring_function_params = None # reset everything
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.rax.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))  
        for i in range(self.func_params) :
            self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.arg_mem.address + 4 * i, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.rax.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)] ))
                        
            self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ADD,
                                                                        [ThreeAddressInstructionOperand(self.rax.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE), 
                                                                              ThreeAddressInstructionOperand(self.rax.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)]    ))   
        print("Shoomb param end")
    def function_end(self):
        """
        When the function ends, we pop the scope and remove the
        block from stack
        """
        print("Shoomb END ++++++++++++++++++++++++++++")
        self.semantic_analyzer.exit_scope()
        self.sp.pointer -= 4
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.SUB,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(4, ThreeAddressInstructionNumberType.IMMEDIATE),
                                                                                ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        
        # Put the return value in EAX register
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.ASSIGN,
                                                                        [ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                                                                            ThreeAddressInstructionOperand(self.eax.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
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
                                                                                ThreeAddressInstructionOperand(self.pc.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS)] ))
        print(self.sp.pointer)
        self.program_block.add_instruction(ThreeAddressInstruction(ThreeAddressInstructionOpcode.JP,
                                                                        [ThreeAddressInstructionOperand(self.pc.address, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS)])) 
        print("End func -------------------")
    def pop_int_type(self):
        assert self.ss.pop() == int(Constants.INT_TYPE)

    def variables_declared(self):
        """
        When the statement of a function is being parsed, after the very first of it, we have declared every
        variable and thus we can assign addresses to them.
        """
        self.semantic_analyzer.assign_scope_addresses()
        print("DECLARING VARS BEGIN")
        # Generate code to assign the address of arrays
        for variable in self.semantic_analyzer.scope_stack[-1]:
            # TODO: should this be > 0 or >= 0?
            if variable.var_type == VariableType.INT_ARRAY and variable.parameters > 0:
                # Find the address of the array pointer
                self.program_block.add_instruction(ThreeAddressInstruction(
                    # R1 = SP + address
                    ThreeAddressInstructionOpcode.ADD,
                    [
                        ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                        ThreeAddressInstructionOperand(variable.address, ThreeAddressInstructionNumberType.IMMEDIATE),
                        ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                    ]))
                # Set the array pointer to first data
                self.program_block.add_instruction(ThreeAddressInstruction(
                    # [R1] = SP + address + 4
                    ThreeAddressInstructionOpcode.ADD,
                    [
                        ThreeAddressInstructionOperand(self.sp.address, ThreeAddressInstructionNumberType.DIRECT_ADDRESS),
                        # Skip the pointer itself and point to data
                        ThreeAddressInstructionOperand(variable.address + 4, ThreeAddressInstructionNumberType.IMMEDIATE),
                        # Put it in the 
                        ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ]))
        print("DECLARING VARS END")

    def pid(self):
        """
        Push the PID in stack and check if it actually exists
        """
        assert self.scanner.lookahead_token[0] == scanner.TokenType.ID
        # Get the entry from semantic analyzer
        variable = self.semantic_analyzer.get_entry(self.scanner.lookahead_token[1])
        if variable == None:
            self.semantic_analyzer.error_list.append(f"#{self.scanner.line_number}: Semantic Error! '{self.scanner.lookahead_token[1]}' is not defined")
            return
        # Get the address of variable
        global_variable = self.semantic_analyzer.is_global_variable(self.scanner.lookahead_token[1])
        if global_variable:
            self.pid_scope_stack.append(VariableScope.GLOBAL_VARIABLE)
        else:
            self.pid_scope_stack.append(VariableScope.LOCAL_VARIABLE)
        self.ss.append(variable.address)
        print(variable.lexeme, variable.address)

    def save_operator(self):
        """
        Save the next operator in scanner into 
        """
        if self.scanner.lookahead_token[1] == "+":
            self.operator_stack.append(MathOperator.PLUS)
        elif self.scanner.lookahead_token[1] == "-":
            self.operator_stack.append(MathOperator.MINUS)
        elif self.scanner.lookahead_token[1] == "*":
            self.operator_stack.append(MathOperator.MULT)
        elif self.scanner.lookahead_token[1] == "<":
            self.operator_stack.append(MathOperator.LESS_THAN)
        elif self.scanner.lookahead_token[1] == "==":
            self.operator_stack.append(MathOperator.EQUALS)
        else:
            raise Exception("SHASH AZIM")
    
    def assign(self):
        """
        In assign, the top of the stack should be the right hand side variable.
        The value below it is the left hand side.

        After this function executes, we will leave a pointer to result in the stack.
        (we will not pop the value below it.)
        """
        print("ASSIGN")
        # Get the source
        src_address = self.ss.pop()
        src_scope = self.pid_scope_stack.pop()
        # Get the dest
        dst_address = self.ss[-1]
        dst_scope = self.pid_scope_stack[-1]
        # Put the addresses in temp variables
        self.find_absolute_address(src_address, src_scope, self.temp_registers.TEMP_R1)
        self.find_absolute_address(dst_address, dst_scope, self.temp_registers.TEMP_R2)
        # [R2] = [R1]
        self.program_block.add_instruction(ThreeAddressInstruction(
            ThreeAddressInstructionOpcode.ASSIGN,
            [
                ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
            ]))

    def immediate(self):
        """
        Generates code to put an immediate value in the stack in a temporary.
        I will also get the temporary and push the address in the ss.
        """
        print("IMMEDIATE")
        assert self.scanner.lookahead_token[0] == scanner.TokenType.NUM
        # Create a variable
        tmp_address = self.semantic_analyzer.get_temp()
        # Put the address in R1
        self.find_absolute_address(tmp_address, VariableScope.LOCAL_VARIABLE, self.temp_registers.TEMP_R1)
        # Create the code
        # [R1] = #Number
        self.program_block.add_instruction(ThreeAddressInstruction(
            ThreeAddressInstructionOpcode.ASSIGN,
            [
                ThreeAddressInstructionOperand(int(self.scanner.lookahead_token[1]), ThreeAddressInstructionNumberType.IMMEDIATE),
                ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
            ]))
        # Put data in the stack
        self.ss.append(tmp_address)
        self.pid_scope_stack.append(VariableScope.LOCAL_VARIABLE)

    def calculate(self):
        """
        Calculate will calculate the result of a mathematical expression

        Will leave the address of result in stack.
        """
        # Get variables from stack
        s2_address = self.ss.pop()
        s2_scope = self.pid_scope_stack.pop()
        s1_address = self.ss.pop()
        s1_scope = self.pid_scope_stack.pop()
        tmp_variable = self.semantic_analyzer.get_temp()
        # Generate codes to put the address in temp variables
        self.find_absolute_address(s1_address, s1_scope, self.temp_registers.TEMP_R1)
        self.find_absolute_address(s2_address, s2_scope, self.temp_registers.TEMP_R2)
        self.find_absolute_address(tmp_variable, VariableScope.LOCAL_VARIABLE, self.temp_registers.TEMP_R3)
        # Do the thing needed
        operation = self.operator_stack.pop()
        if operation == MathOperator.PLUS:
            self.program_block.add_instruction(ThreeAddressInstruction(
                ThreeAddressInstructionOpcode.ADD,
                [
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R3, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ]))
        elif operation == MathOperator.MINUS:
            self.program_block.add_instruction(ThreeAddressInstruction(
                ThreeAddressInstructionOpcode.SUB,
                [
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R3, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ]))
        elif operation == MathOperator.MULT:
            self.program_block.add_instruction(ThreeAddressInstruction(
                ThreeAddressInstructionOpcode.MULT,
                [
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R3, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ]))
        elif operation == MathOperator.LESS_THAN:
            self.program_block.add_instruction(ThreeAddressInstruction(
                ThreeAddressInstructionOpcode.LT,
                [
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R3, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ]))
        elif operation == MathOperator.EQUALS:
            self.program_block.add_instruction(ThreeAddressInstruction(
                ThreeAddressInstructionOpcode.EQ,
                [
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                    ThreeAddressInstructionOperand(self.temp_registers.TEMP_R3, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ]))
        else:
            raise Exception("SHASH")
        # Add the result to stack
        self.ss.append(tmp_variable)
        self.pid_scope_stack.append(VariableScope.LOCAL_VARIABLE)
                
    def negate(self):
        """
        Negate will get the value on top of the stack,
        negate it,
        and push it back
        """
        # Get the addresses
        address = self.ss.pop()
        scope = self.pid_scope_stack.pop()
        tmp_variable = self.semantic_analyzer.get_temp()
        # Move the address to array
        self.find_absolute_address(address, scope, self.temp_registers.TEMP_R1)
        self.find_absolute_address(tmp_variable, VariableScope.LOCAL_VARIABLE, self.temp_registers.TEMP_R2)
        # Negate it
        self.program_block.add_instruction(ThreeAddressInstruction(
            # [R2] = 0 - [R1]
            ThreeAddressInstructionOpcode.SUB,
            [
                ThreeAddressInstructionOperand(0, ThreeAddressInstructionNumberType.IMMEDIATE),
                ThreeAddressInstructionOperand(self.temp_registers.TEMP_R1, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
                ThreeAddressInstructionOperand(self.temp_registers.TEMP_R2, ThreeAddressInstructionNumberType.INDIRECT_ADDRESS),
            ]))
        # Push back the result
        self.ss.append(tmp_variable)
        self.pid_scope_stack.append(VariableScope.LOCAL_VARIABLE)

    def array(self):
        pass

    def pop_expression(self):
        """
        Pops the result of an expression from stack
        """
        self.ss.pop()
        self.pid_scope_stack.pop()
        print("SIZE", self.pid_scope_stack, self.ss, self.operator_stack)