from tabulate import tabulate

from App.Models.circuit import Circuit
from App.Models.restaurant import Restaurant
from App.Models.seat import Seat


# clase que se encarga de modelar la información de la carrera en objetos de python.
class Race:
    def __init__(self, round, name, circuit, date, restaurants, map, attendance=0, sold_tickets=0, vip_seats=None, general_seats=None):
        self.round = round
        self.name = name
        self.circuit = Circuit(**circuit)
        self.date = date
        self.attendance = int(attendance)
        self.sold_tickets = int(sold_tickets)
        self.restaurants = []
        for restaurant in restaurants:
            self.restaurants.append(Restaurant(**restaurant))
        self.map = map
        self.vip_seats = []
        if vip_seats is not None:
            for row in vip_seats:
                new_row = []
                for seat in row:
                    new_row.append(Seat(**seat))
                self.vip_seats.append(new_row)

        self.general_seats = []
        if general_seats is not None:
            for row in general_seats:
                new_row = []
                for seat in row:
                    new_row.append(Seat(**seat))
                self.general_seats.append(new_row)

    def __str__(self):
        return f'RACE ROUND: {self.round}\n\trace name: {self.name}\n\tcircuit name: {self.circuit.name}\n' \
               f'\trace date: {self.date}\n\trace country: {self.circuit.location.country}\n'

    def define_general_seats_matrix(self):
        self.general_seats = [[Seat(position=str(j)+str(i)) for i in range(self.map['general'][1])] for j in range(self.map['general'][0])]

    def define_vip_seats_matrix(self):
        self.vip_seats = [[Seat(position=str(j)+str(i)) for i in range(self.map['vip'][1])] for j in range(self.map['vip'][0])]

    def print_general_seats(self):
        for row in self.general_seats:
            print('_____' * len(row))
            print_row = str(row).replace(',', '').replace('[', '').replace(']', '')
            print(print_row)

    def print_vip_seats(self):
        for row in self.vip_seats:
            print('_____' * len(row))
            print_row = str(row).replace(',', '').replace('[', '').replace(']', '')
            print(print_row)

    def print_general_seats_tabulate(self):
        print(tabulate(self.general_seats, tablefmt='grid', numalign='center', stralign='center'))

    def print_vip_seats_tabulate(self):
        print(tabulate(self.vip_seats, tablefmt='grid', numalign='center', stralign='center'))

    def pretty_print_attendance(self):
        print(f'\tATTENDANCE: {self.attendance}\n')

    def pretty_print_sold_tickets(self):
        print(f'\tSOLD TICKETS: {self.sold_tickets}\n')
