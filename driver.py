class Driver:
    def __init__(self, driver_id, permanent_number, code, team, first_name, last_name, birth_date, nationality):
        self.id = driver_id
        self.permanent_number = permanent_number
        self.code = code
        self.team = team
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.nationality = nationality

    def __str__(self):
        return f' -----\n ---\n name: {self.first_name} {self.last_name}\n ' \
               f'birth_date: {self.birth_date}\n nationality: {self.nationality}\n ---\n -----\n'
