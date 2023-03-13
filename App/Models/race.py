from App.Models.circuit import Circuit
from App.Models.restaurant import Restaurant


class Race:
    def __init__(self, round, name, circuit, date, restaurants):
        self.round = round
        self.name = name
        self.circuit = Circuit(**circuit)
        self.date = date
        self.restaurants = []
        for restaurant in restaurants:
            self.restaurants.append(Restaurant(**restaurant))

    def __str__(self):
        return f'RACE NUMBER: {self.round}\n\trace name: {self.name}\n\tcircuit name: {self.circuit.name}\n' \
               f'\trace date: {self.date}\n\trace country: {self.circuit.location.country}\n' \
               f'\trace state: {self.circuit.location.locality}'
