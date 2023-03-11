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
