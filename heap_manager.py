class HeapManager():

    def __init__(self, size):
        self.first_free = 500

    def get_temp(self, type, size):
        return 0