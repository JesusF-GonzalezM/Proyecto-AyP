from App.Models.ticket import Ticket


class Client:
    def __init__(self, name, id, age, total_spent=0, tickets=None):
        self.name = name
        self.id = id
        self.age = int(age)
        self.total_spent = total_spent
        self.tickets = []
        if tickets is not None:
            for ticket in tickets:
                self.tickets.append(Ticket(**ticket))

    def __str__(self):
        return f'name: {self.name}, age: {self.age} tickets: {self.tickets}'

    def add_ticket(self, ticket):
        self.tickets.append(ticket)
