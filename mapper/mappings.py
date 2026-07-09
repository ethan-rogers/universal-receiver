class Mapping:
    def __init__(self):
        self.mapping = []
        self.code = None
        self.keys = []

    def add_key(self, key):
        self.keys.append(key)

    def get_keys(self):
        key_str = "" 

        for i, k in enumerate(self.keys):
            key_str += k
            if i != len(self.keys) - 1:
                key_str += " + "

        return key_str


    def add_code(self, code):
        self.code = code

    def add_mapping(self):
        self.mapping.append([self.code, self.keys])
        self.code = None
        self.keys = []

    def map_to_arduino(self):
        print("Attempting Mapping")