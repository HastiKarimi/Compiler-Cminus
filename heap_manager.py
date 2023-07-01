class HeapManager:

    def __init__(self):
        self.first_free = 500
        self.variables = {}

    def get_temp(self, type_name, size=1):
        # return address of the first free cell
        temp_address = self.first_free
        for i in range(size):
            temp = TempVariable(type_name, self.first_free)
            self.variables[self.first_free] = temp
            self.first_free += self.get_length_by_type(type_name)

        return temp_address

    @staticmethod
    def get_length_by_type(type_name):
        return 4
        if type_name == "int":
            return 4
        elif type_name == "void":
            return 1

    def get_type_by_address(self, address):
        return self.variables[address].type_name


class TempVariable:
    def __init__(self, type_name, address):
        self.type_name = type_name
        self.address = address
