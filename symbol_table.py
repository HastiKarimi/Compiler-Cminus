class SymbolTable():

    def __init__(self) -> None:
        # row properties are lexeme, proc/func/var/param (kind), No. Arg/Cell (attributes), type, scope, address
        self.adress_to_row = {}
        self.table = []
        self.current_scope = 0

    def insert(self):
        # self.table.append(row)
        # self.adress_to_row[row.adress] = row
        pass

    def modify_last_row(self, kind, type):
        # after declaration of a variable by scanner, code generator needs
        # to complete the declaration by modifying the last row of symbol table
        self.table[-1]['kind'] = kind
        self.table[-1]['type'] = type
        self.table[-1]['scope'] = self.current_scope
        self.table[-1]['attributes'] = 0
        #TODO add address
        pass

    def modify_attributes_last_row(self, num_attributes):
        # used for array declaration and function declaration
        self.table[-1]['attributes'] = num_attributes

    def add_scope(self):
        self.current_scope += 1

    def declare_array(self, num_of_cells):
        self.table[-1]['attributes'] = num_of_cells

    def end_scope(self):
        # remove all rows with scope = current_scope
        pass



    def lookup(self, name, start_ind, end_ind = -1) -> dict:
        # search in symbol table
        # search for it between the start_ind and end_ind of symbol table
        # if end_ind == -1 then it means to search till the end of symbol table
        pass

    def get_row_id_by_address(self, address) -> int:
        # return self.adress_to_row[address]
        pass

    def get_row_by_id(self, id) -> dict:
        return self.table[id]