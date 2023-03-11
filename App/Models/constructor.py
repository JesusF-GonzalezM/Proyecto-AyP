class Constructor:
    def __init__(self, id, name, nationality):
        self.id = id  # Name of the team used in code to compare equality with drivers.team.
        self.name = name  # Same name as team_id but formatted for prints.
        self.nationality = nationality

    def __str__(self):
        return f' -----\n ---\n name: {self.name}\n ' \
               f'nationality: {self.nationality}\n ---\n -----\n'
