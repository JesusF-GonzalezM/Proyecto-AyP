class Seat:
    def __init__(self, position, code=None, taken=False):
        self.position = position
        self.code = code
        self.taken = taken

    def __repr__(self):
        if not self.taken:
            return f'|{self.position}|'
        return f'|XX|'

    def show_all(self):
        print(f'position: {self.position}\ncode: {self.code}\ntaken: {self.taken}')
