from App.Models.ticket import Ticket


def number_is_ondulado(num):  # this shit does not work
    num = str(num)
    if int(num) < 100:
        return True
    a = num[0]
    b = num[1]
    for index in range(2, len(num), 2):
        if len(num) == index or len(num) == index + 1:
            break
        if num[index] != a or num[index + 1] != b:
            return False
    return True


class Client:
    def __init__(self, name, id, age, race_name, ticket):
        self.name = name
        self.id = id
        self.age = age
        self.race_name = race_name
        if isinstance(ticket, str):
            self.ticket = Ticket(ticket)
        else:
            self.ticket = Ticket(**ticket)

        if number_is_ondulado(self.id):
            self.ticket.discount = True

    def __str__(self):
        return f'name: {self.name}, age: {self.age}, race_name: {self.race_name}'
