class HeapManager():

    def __init__(self):
        self.first_free = 500

    def get_temp(self, type_name, size=1):
        # return address of the first free cell
        temp_address = self.first_free
        # update first_free
        self.first_free += size * self.get_length_by_type(type_name)
        return temp_address

    def get_length_by_type(self, type_name):
        if type_name == "int":
            return 4
        elif type_name == "void":
            return 1
