from enum import Enum


# clase Enumerado que se encarga de darle al ticket una funcionalidad comoda para transformar de 1 a Vip y de 2 a General.
class TicketType(str, Enum):
    VIP = '1'
    GENERAL = '2'


# Mapa interno que le permite a la clase Ticket saber su valor.
ticket_price = {
    'VIP': 340,
    'GENERAL': 150,
}


# clase que se encarga de modelar la información el ticket en objetos de python.
class Ticket:
    def __init__(self, race_round, type, code=None, total_price=0, discount=False):
        self.race_round = race_round
        self.type = TicketType(type)
        self.code = code
        self.total_price = total_price
        self.discount = discount

    def calculate_price(self):
        self.total_price = ticket_price[self.type.name]
