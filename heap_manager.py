class HeapManager():

    def __init__(self):
        self.first_free = 500

    def get_temp(self, type, size):
        # return address of the first free cell
        temp_address = self.first_free
        # update first_free
        if type == "int":
            self.first_free += size * 4
        elif type == "void":
            self.first_free += size

        return temp_address