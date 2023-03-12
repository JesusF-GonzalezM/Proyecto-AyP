import random
from enum import Enum


class TicketType(Enum):
    VIP = '1'
    GENERAL = '2'


ticket_price = {
    'VIP': 340,
    'GENERAL': 150,
}


class Ticket:
    def __init__(self, type):
        self.type = TicketType(type)
        self.code = None
        self.total_price = 0
        self.discount = False

    def calculate_price(self):
        initial_price = ticket_price[self.type.name]
        ticket_price_iva = initial_price * 0.16
        total_ticket_price = initial_price + ticket_price_iva
        if self.discount:
            total_ticket_price *= 0.5
        self.total_price = total_ticket_price

    def print_detailed_price(self):
        base_price = ticket_price[self.type.name]
        iva_price = base_price * 0.16
        print(f'Subtotal: {base_price}\nIVA: {iva_price}')
        if self.discount:
            print(f'You qualify for a discount!')
        else:
            print(f'You dont qualify for a discount')
        print(f'Total: {self.total_price}')

