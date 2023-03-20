from App.Models.ticket import Ticket


# clase que se encarga de modelar la información del cliente en objetos de python.
class Client:
    def __init__(self, name, id, age, total_spent=0, tickets=None):
        self.name = name
        self.id = id
        self.age = int(age)
        self.total_spent = int(total_spent)
        self.tickets = []
        if tickets is not None:
            for ticket in tickets:
                self.tickets.append(Ticket(**ticket))

    def __str__(self):
        return f'Name: {self.name} | Age: {self.age} | amount_of_tickets: {len(self.tickets)}'

    def add_ticket(self, ticket):
        self.tickets.append(ticket)
