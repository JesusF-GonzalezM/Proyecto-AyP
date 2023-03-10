class Constructor:
    def __init__(self, constructor_id, name, nationality):
        self.id = constructor_id
        self.name = name
        self.nationality = nationality

    def __str__(self):
        return f' -----\n ---\n name: {self.name}\n ' \
               f'nationality: {self.nationality}\n ---\n -----\n'
