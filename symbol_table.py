from heap_manager import HeapManager


class SymbolTable:

    def __init__(self, heap_manager) -> None:
        # row properties are id, lexeme, proc/func/var/param (kind), No. Arg/Cell (attributes), type, scope, address
        self.address_to_row = {}
        self.table = []
        self.current_scope = 0
        self.heap_manager = heap_manager
        self.scope_stack = [0]
        self.insert("output")
        self.modify_last_row("func", "void")
        self.table[-1]['attributes'] = 1
        self.table.append({'id': 1, 'lexeme': 'somethingwild', 'kind': "var", 'attributes': '-', 'type': "int",
                           'scope': 0, 'address': self.heap_manager.get_temp("int", 1)})

    def insert(self, lexeme):
        self.table.append({'id': len(self.table), 'lexeme': lexeme})

    def modify_last_row(self, kind, type):
        # after declaration of a variable by scanner, code generator needs
        # to complete the declaration by modifying the last row of symbol table
        self.table[-1]['kind'] = kind
        self.table[-1]['type'] = type
        self.table[-1]['address'] = self.heap_manager.get_temp(type, 1)
        self.table[-1]['scope'] = self.current_scope
        self.table[-1]['attributes'] = '-'
        self.address_to_row[self.table[-1]['address']] = len(self.table) - 1

    def modify_attributes_last_row(self, num_attributes, arr_func: bool = True):
        # used for array declaration and function declaration
        # if arr_func == True then it is an array
        # else it is a function
        # note: for now it is only used for array declaration
        num_attributes = int(num_attributes[1:])
        self.table[-1]['attributes'] = num_attributes
        if arr_func:
            self.heap_manager.get_temp(self.table[-1]['type'], num_attributes - 1, True)

    def modify_attributes_row(self, row_id, num_attributes, arr_func: bool = True):
        # used for modifying function No. of args after counting them
        # if arr_func == True then it is an array
        # else it is a function
        self.table[row_id]['attributes'] = num_attributes

    def modify_kind_last_row(self, kind):
        self.table[-1]['kind'] = kind

    def add_scope(self):
        self.current_scope += 1
        self.scope_stack.append(len(self.table))

    def end_scope(self):
        # remove all rows of symbol table that are in the current scope 
        # and update the current scope
        # remember function is first added and then the scope is added
        # also param type of the function that the scope is created for,
        # must not be removed
        remove_from = len(self.table)
        for i in range(self.scope_stack[-1], len(self.table)):
            if self.table[i]['kind'] != "param":
                remove_from = i
                break

        for i in range(remove_from, len(self.table)):
            # this function free_temp is not implemented yet
            self.heap_manager.free_temp(self.table[i]['type'],
                                        self.table[i]['attributes'],
                                        self.table[i]['address'])

        self.table = self.table[:remove_from]

        self.current_scope -= 1
        # self.scope_stack.pop()

    def declare_array(self, num_of_cells):
        self.table[-1]['attributes'] = num_of_cells

    def lookup(self, name, start_ind=0, end_ind=-1, in_declare=False) -> dict:
        # search in symbol table
        # search for it between the start_ind and end_ind of symbol table
        # if end_ind == -1 then it means to search till the end of symbol table

        if end_ind == -1:
            end_ind = len(self.table)
            if in_declare:
                end_ind -= 1

        row_answer = None
        for i in range(start_ind, end_ind):
            if "address" in self.table[i] and self.table[i]['lexeme'] == name and (self.table[i]['kind'] != "param" or
                                                                                   self.table[i]['id'] >= self.scope_stack[-1]):
                row_answer = self.table[i]

        return row_answer

    def remove_last_row(self):
        self.table.pop()

    def get_row_id_by_address(self, address) -> int:
        return self.address_to_row[address]

    def get_row_by_id(self, id) -> dict:
        return self.table[id]

    def get_id_last_row(self):
        return len(self.table) - 1

    def get_row_by_address(self, address) -> dict:
        return self.get_row_by_id(self.get_row_id_by_address(address))

    def get_last_row(self):
        return self.get_row_by_id(-1)
