from heap_manager import HeapManager
# TODO there are two heap managers in the project, one in symbol_table.py and one in code_generator.py

class SymbolTable():

    def __init__(self) -> None:
        # row properties are lexeme, proc/func/var/param (kind), No. Arg/Cell (attributes), type, scope, address
        self.address_to_row = {}
        self.table = []
        self.current_scope = 0
        self.heap_manager = HeapManager()

    def insert(self, lexeme):
        self.table.append({'lexeme': lexeme})

    def modify_last_row(self, kind, type):
        # after declaration of a variable by scanner, code generator needs
        # to complete the declaration by modifying the last row of symbol table
        self.table[-1]['kind'] = kind
        self.table[-1]['type'] = type
        self.table[-1]['address'] = self.heap_manager.get_temp(type, 1)
        self.table[-1]['scope'] = self.current_scope
        self.table[-1]['attributes'] = 0
        self.address_to_row[self.table[-1]['address']] = len(self.table) - 1


    def modify_attributes_last_row(self, num_attributes, arr_func: bool = True):
        # used for array declaration and function declaration
        # if arr_func == True then it is an array
        # else it is a function
        self.table[-1]['attributes'] = num_attributes
        if arr_func:
            self.heap_manager.get_temp(self.table[-1]['type'], num_attributes - 1)

    
    def modify_parameter(self):
        self.table[-1]['kind'] = "param"


    def add_scope(self):
        self.current_scope += 1

    def declare_array(self, num_of_cells):
        self.table[-1]['attributes'] = num_of_cells

    def end_scope(self):
        # remove all rows with scope = current_scope
        while self.table[-1]['scope'] == self.current_scope:
            self.table.pop()
        
        self.current_scope -= 1



    def lookup(self, name, start_ind, end_ind = -1) -> dict:
        # search in symbol table
        # search for it between the start_ind and end_ind of symbol table
        # if end_ind == -1 then it means to search till the end of symbol table
        if end_ind == -1:
            end = len(self.table)
        
        for i in range(start_ind, end):
            if self.table[i]['lexeme'] == name:
                return self.table[i]

    def get_row_id_by_address(self, address) -> int:
        return self.address_to_row[address]

    def get_row_by_id(self, id) -> dict:
        return self.table[id]

    def get_row_by_address(self, address) -> dict:
        return self.get_row_by_id(self.get_row_id_by_address(address))