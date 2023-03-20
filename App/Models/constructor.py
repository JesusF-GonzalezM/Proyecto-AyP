# clase que se encarga de modelar la información del constructor en objetos de python.
class Constructor:
    def __init__(self, id, name, nationality, score=0):
        self.id = id  # Name of the team used in code to compare equality with drivers.team.
        self.name = name  # Same name as team_id but formatted for prints.
        self.nationality = nationality
        self.score = int(score)

    def __str__(self):
        return f' --------------\n name: {self.name}\n ' \
               f'nationality: {self.nationality}\n'

    # sets the score to the constructors after the race finished.
    def set_score(self, drivers):
        for driver in drivers:
            if driver.team == self.id:
                self.score += driver.score
    