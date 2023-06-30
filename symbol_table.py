class SymbolTable():

    def __init__(self) -> None:
        self.adress_to_row = {}
        self.table = []

    def insert(self, row):
        # self.table.append(row)
        # self.adress_to_row[row.adress] = row
        pass

    def lookup(self, name, start_ind, end_ind = -1):
        # search in symbol table
        # search for it between the start_ind and end_ind of symbol table
        # if end_ind == -1 then it means to search till the end of symbol table
        pass

    def get_row_by_address(self, address):
        # return self.adress_to_row[address]
        pass