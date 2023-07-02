# write functions for action symbols
# management stack and ...
# semantic
# change symbol table generated by scanner in the SymbolTable class
# parse change to call semantic analyzer and code generator
# create output file
"""
1    assign             done
1    declare_id         done
1    declare_array      done
1    push_type          done
2    do_op              done
2    mult               done
2    push_op            done
1    label              done
1    until              done
2    array_calc         done
2    jpf_save           done
2    save               done
2    jp                 done
1    print              done
1    push_num           done
2    id                 done
    add_scope ***
    counter ***
    counter_up ***
    break ***
    end_scope ***
    check_not_void ***
    end_func ***
    add_param ***
    end_func_params ***
"""

from symbol_table import SymbolTable
from heap_manager import HeapManager

kind_key = "kind"
type_key = "type"
address_key = "address"
scope_key = "scope"
attributes_key = "attributes"
lexeme_key = "lexeme"


def semantic_error(type_error="error", first_op="", second_op="", third_op=""):
    print(f"semantic error: {first_op}, {second_op}, {third_op}")


class CodeGenerator:

    def __init__(self, symbol_table: SymbolTable, heap: HeapManager):
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.PB = []
        # pc shows the next line of program block to be filled (i in slides)
        self.PC = 0
        self.scope_stack = [0]
        self.heap_manager = heap

    def code_gen(self, action_symbol, token):
        action_symbol = action_symbol[1:]
        if action_symbol == "declare_id":
            self.declare_id(token)
        elif action_symbol == "declare_array":
            self.declare_array(token)
        elif action_symbol == "push_type":
            self.push_type(token)
        elif action_symbol == "do_op":
            self.do_op(token)
        elif action_symbol == "mult":
            self.mult(token)
        elif action_symbol == "push_op":
            self.push_op(token)
        elif action_symbol == "label":
            self.label(token)
        elif action_symbol == "until":
            self.until(token)
        elif action_symbol == "array_calc":
            self.array_calc(token)
        elif action_symbol == "jpf_save":
            self.jpf_save(token)
        elif action_symbol == "save":
            self.save(token)
        elif action_symbol == "jp":
            self.jp(token)
        elif action_symbol == "print":
            self.print(token)
        elif action_symbol == "push_num":
            self.push_num(token)
        elif action_symbol == "id":
            self.id(token)
        elif action_symbol == "assign":
            self.assign(token)
        elif action_symbol == "push_eq":
            self.push_eq(token)
        elif action_symbol == "break":
            self.break_check(token)

    def pop_last_n(self, n):
        # pop last n elements from semantic stack
        for _ in range(n):
            self.semantic_stack.pop()

    @staticmethod
    def get_pb_line(line_index, operation, first_op=" ", second_op=" ", third_op=" "):
        return f'{line_index}\t({operation}, {first_op}, {second_op}, {third_op} )'

    def program_block_insert(self, operation, first_op=" ", second_op=" ", third_op=" "):
        # insert to program block
        operation = self.get_operation_by_symbol(operation)
        self.PB.append(self.get_pb_line(len(self.PB), operation, first_op, second_op, third_op))
        self.PC += 1

    def program_block_modification(self, index, operation, first_op="", second_op="", third_op=""):
        # modify a passed line of program block and add the code
        operation = self.get_operation_by_symbol(operation)
        self.PB[index] = self.get_pb_line(index, operation, first_op, second_op, third_op)

    def program_block_insert_empty(self):
        # TODO change back
        # self.PB.append("")
        self.program_block_insert(operation=":=", first_op="#0", second_op="0")
        # self.PC += 1

    @staticmethod
    def get_operation_by_symbol(symbol):
        if symbol == '+':
            return "ADD"
        elif symbol == '-':
            return "SUB"
        elif symbol == '*':
            return "MULT"
        elif symbol == "==":
            return "EQ"
        elif symbol == "<":
            return "LT"
        elif symbol == ":=":
            return "ASSIGN"
        else:
            return symbol.upper()

    def push_type(self, token):
        # push type to stack
        if token == "int" or token == "void":
            self.semantic_stack.append(token)
        else:
            raise Exception("type not supported")

    def push_num(self, token):
        # push number to stack
        self.semantic_stack.append(str("#" + token.strip()))

    def print(self, token):
        self.program_block_insert(operation="print", first_op=self.semantic_stack[-1])
        self.semantic_stack.pop()

    def break_check(self, token):
        # TODO check if we are in a repeat until statement
        # push PC counter so that it can be filled in the #until action symbol to jump out
        # self.semantic_stack.insert(0, self.PC)
        self.semantic_stack.append(self.PC)
        self.program_block_insert_empty()
        # self.semantic_stack.insert(1, "break")
        self.semantic_stack.append("break")

    def declare_id(self, token, kind="var"):
        # search in symbol table
        # if found in current scope raise error
        # if not found
        # add to symbol table
        # token will be the lexeme of the variable
        if self.symbol_table.lookup(token, self.scope_stack[-1], True) != None:
            raise Exception("variable already declared")
        else:
            self.symbol_table.modify_last_row(kind=kind, type=self.semantic_stack[-1])
            self.program_block_insert(
                operation=":=",
                first_op="#0",
                second_op=self.symbol_table.get_last_row()[address_key],
            )
            self.semantic_stack.pop()

    def declare_array(self, token):
        # search in symbol table
        # if found in current scope raise error
        # if not found
        # add to symbol table
        if self.symbol_table.lookup(token, self.scope_stack[-1], True) != None:
            raise Exception("variable already declared")
        else:
            self.symbol_table.modify_attributes_last_row(num_attributes=self.semantic_stack[-1])
            self.semantic_stack.pop()

    def assign(self, token):
        # stack:
        # -1: source
        # -2: =
        # -3: destination
        answer = self.semantic_stack[-3]
        self.program_block_insert(operation=":=", first_op=self.semantic_stack[-1], second_op=self.semantic_stack[-3])
        self.pop_last_n(3)
        if len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "=":
            # means there was a nested assignment and we should push the result to the stack
            self.semantic_stack.append(answer)

    def label(self, token):
        # declare where to jump back after until in repeat-until
        self.semantic_stack.append(self.PC)

    def until(self, token):
        # jump back to label if condition is true
        # also check if there were any break statements before
        temp_until_condition = self.semantic_stack.pop()  # the value that until should decide to jump based on it
        # check breaks
        while len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "break":
            self.program_block_modification(self.semantic_stack[-2], operation="JP", first_op=self.PC + 1)
            self.pop_last_n(2)
        # jump back
        self.program_block_insert(operation="JPF", first_op=temp_until_condition,
                                  second_op=self.semantic_stack[-1])
        self.pop_last_n(1)

    def mult(self, token):
        # multiply two numbers from top of the stack and push the result
        first_op = self.semantic_stack[-1]
        second_op = self.semantic_stack[-2]
        # todo semantic: check operands type
        op_type = self.get_operand_type(first_op)
        temp = self.heap_manager.get_temp(op_type)
        self.program_block_insert(operation="*", first_op=first_op, second_op=second_op, third_op=temp)
        self.pop_last_n(2)
        self.semantic_stack.append(temp)

    def array_calc(self, token):
        # calculate the address of the index of the array
        # the index is on top of the stack and the address of array is the second element
        # pop those two and push the address of calculated address to the stack
        array_address = self.semantic_stack[-2]
        # array_type = self.symbol_table.get_row_by_address(array_address)[type_key]
        array_type = self.get_operand_type(array_address)
        temp = self.heap_manager.get_temp(array_type)
        self.program_block_insert(
            operation="*",
            first_op=self.semantic_stack[-1],
            second_op="#" + str(self.heap_manager.get_length_by_type(array_type)),
            third_op=temp
        )
        self.program_block_insert(
            operation="+",
            first_op=str('#' + str(array_address)),
            second_op=temp,
            third_op=temp
        )
        self.pop_last_n(2)
        self.semantic_stack.append(str('@' + str(temp)))

    def push_op(self, token):
        # push operator to stack
        self.semantic_stack.append(token)

    def do_op(self, token):
        # do the operation
        # pop the operator and operands from the stack
        # push the result to the stack
        op = self.semantic_stack[-2]
        first_op = self.semantic_stack[-3]
        second_op = self.semantic_stack[-1]
        self.pop_last_n(3)
        # todo semantic: check operands type
        operands_type = self.get_operand_type(first_op)
        temp = self.heap_manager.get_temp(operands_type)
        self.program_block_insert(operation=op, first_op=first_op, second_op=second_op, third_op=temp)
        self.semantic_stack.append(temp)

    def jpf_save(self, token):
        # jpf
        index_before_break = -1
        # remove breaks
        while self.semantic_stack[index_before_break] == "break":
            index_before_break -= 2
        breaks = []
        if index_before_break != -1:
            breaks = self.semantic_stack[index_before_break + 1:]
            self.semantic_stack = self.semantic_stack[:index_before_break + 1]

        self.program_block_modification(
            index=self.semantic_stack[-1],
            operation="JPF",
            first_op=self.semantic_stack[-2],
            second_op=str(self.PC + 1)
        )
        self.pop_last_n(2)
        # then save current pc
        self.semantic_stack.append(self.PC)
        self.program_block_insert_empty()
        # add back breaks
        self.semantic_stack.extend(breaks)

    def save(self, toke):
        # save the current PC
        self.semantic_stack.append(self.PC)
        self.program_block_insert_empty()

    def jp(self, token):
        # jump to a label

        index_before_break = -1
        while self.semantic_stack[index_before_break] == "break":
            index_before_break -= 2
        breaks = []
        # remove breaks
        if index_before_break != -1:
            breaks = self.semantic_stack[index_before_break + 1:]
            self.semantic_stack = self.semantic_stack[:index_before_break + 1]

        self.program_block_modification(
            index=self.semantic_stack[-1],
            operation="JP",
            first_op=str(self.PC)
        )
        self.pop_last_n(1)

        # add back breaks
        self.semantic_stack.extend(breaks)

    def id(self, token):
        # push the address of current token
        # todo semantic: check if variable is declared in our scope
        # todo how should we handle scope?
        row = self.symbol_table.lookup(token, self.scope_stack[-1])
        if row[lexeme_key] != "output":  # added because of not implementing function calls
            address = row[address_key]
            self.semantic_stack.append(address)

    def push_eq(self, token):
        # in case of assignment, push = to stack
        # used for finding out if there is a nested assignment
        self.semantic_stack.append("=")

    def get_operand_type(self, operand):
        if str(operand).startswith("#"):
            return "int"
        elif str(operand).startswith("@"):
            operand = operand[1:]
        return self.heap_manager.get_type_by_address(int(operand))

    def print_pb(self):
        print("\n--------------Program Block---------------")
        for row in self.PB:
            print(row)

    def write_pb_to_file(self, file):
        for row in self.PB:
            file.write(str(row) + "\n")
