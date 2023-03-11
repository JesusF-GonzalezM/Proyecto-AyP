class Driver:
    def __init__(self, id, permanentNumber, code, team, firstName, lastName, dateOfBirth, nationality):
        self.id = id
        self.permanentNumber = permanentNumber
        self.code = code
        self.team = team
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.nationality = nationality

    def __str__(self):
        return f' -----\n ---\n name: {self.firstName} {self.lastName}\n ' \
               f'birth_date: {self.dateOfBirth}\n nationality: {self.nationality}\n ---\n -----\n'
