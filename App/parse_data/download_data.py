import json
import os
import requests

from App.Models.client import Client
from App.Models.constructor import Constructor
from App.Models.driver import Driver
from App.Models.race import Race

URL_DRIVERS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/drivers.json'
URL_CONSTRUCTORS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/' \
                   'api-proyecto/main/constructors.json'
URL_RACES = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/races.json'


def upload_data_to_file(obj, filename):
    json_string = json.dumps(obj, default=lambda o: o.__dict__, indent=4)
    with open(f"Database/{filename}.json", "w") as json_file:
        json_file.write(json_string)


def load_clients_from_file():
    clients = []
    if check_txt_data('clients'):
        with open('Database/clients.json', 'r') as clients_file:
            json_clients = json.load(clients_file)
            clients = initialize_clients(json_clients)
    return clients


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


def initialize_drivers_from_api(url):
    response = requests.get(url)
    data_array = response.json()
    return initialize_drivers(data_array)


def initialize_constructors_from_api(url):
    response = requests.get(url)
    data_array = response.json()
    return initialize_constructors(data_array)


def initialize_races_from_api(url):
    response = requests.get(url)
    data_array = response.json()
    return initialize_races(data_array)


def check_txt_data(file_path):
    return os.path.isfile(f'Database/{file_path}.json')


def load_data_from_txt():
    with open('Database/drivers.json', 'r') as drivers_file:
        json_drivers = json.load(drivers_file)
        drivers = initialize_drivers(json_drivers)

    with open('Database/constructors.json', 'r') as constructors_file:
        json_constructors = json.load(constructors_file)
        constructors = initialize_constructors(json_constructors)

    with open('Database/races.json', 'r') as races_file:
        json_race = json.load(races_file)
        races = initialize_races(json_race)

    return drivers, constructors, races


def load_data_from_api_and_save():
    drivers = initialize_drivers_from_api(URL_DRIVERS)
    constructors = initialize_constructors_from_api(URL_CONSTRUCTORS)
    races = initialize_races_from_api(URL_RACES)

    upload_data_to_file(drivers, 'drivers')
    upload_data_to_file(constructors, 'constructors')
    upload_data_to_file(races, 'races')

    return drivers, constructors, races


def initialize_data():
    if not check_txt_data('drivers'):
        drivers, constructors, races = load_data_from_api_and_save()
    else:
        drivers, constructors, races = load_data_from_txt()
    return drivers, constructors, races
