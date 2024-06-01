class stack():
    def __init__(self, bit_string: str) -> None:
        self.stack = list(bit_string)

    def pop(self):
        return_value = self.stack[0]
        self.stack = self.stack[1:]
        return return_value
    
    def push(self, value: str):
        value = list(value)
        self.stack = value +  self.stack






