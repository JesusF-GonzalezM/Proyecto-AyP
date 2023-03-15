from App.Models.client import Client
from App.Models.constructor import Constructor
from App.Models.driver import Driver
from App.Models.race import Race


def initialize_drivers(data_array):
    drivers = []
    for data in data_array:
        driver = Driver(**data)
        drivers.append(driver)
    return drivers


def initialize_races(data_array):
    races = []
    for data in data_array:
        race = Race(**data)
        races.append(race)
    return races


def initialize_constructors(data_array):
    constructors = []
    for data in data_array:
        constructor = Constructor(**data)
        constructors.append(constructor)
    return constructors


def initialize_clients(data_array):
    clients = []
    for data in data_array:
        client = Client(**data)
        clients.append(client)
    return clients
