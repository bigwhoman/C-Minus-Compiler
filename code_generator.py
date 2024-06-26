from scanner import Scanner
from enum import Enum


class VariableType(Enum):
    """
    Type of the variable in symbol table
    """

    INT = 1
    INT_ARRAY = 2

class SymbolTableEntry:
    """
    Each entry in the symbol table has this type
    """

    def __init__(self, lexeme: str, var_type: VariableType):
        self.lexeme = lexeme
        self.var_type = var_type

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


class CodeGenerator:
    FIRST_GLOBAL_VARIABLE_ADDRESS = 100
    FIRST_TEMP_VARIABLE_ADDRESS = 500
    TOP_STACK_ADDRESS = 1000

    def __init__(self, scanner: Scanner):
        self.ss: list[int] = []  # Semantic stack
        self.scanner = scanner
        self.scope_stack: list[int] = []
        self.symbol_table: list[SymbolTableEntry] = []
        # We always define stack pointer the first global variable
        self.declared_global_variables = 1
        self.pc = 1  # Program counter
        self.program_block: list[ThreeAddressInstruction] = []
