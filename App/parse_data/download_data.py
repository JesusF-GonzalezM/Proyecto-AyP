import json
import os
import requests
from App.Models.constructor import Constructor
from App.Models.driver import Driver
from App.Models.race import Race
from App.parse_data.write_to_file import write_to_file

URL_DRIVERS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/drivers.json'
URL_CONSTRUCTORS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/' \
                   'api-proyecto/main/constructors.json'
URL_RACES = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/races.json'


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


def check_txt_data():
    return os.path.isfile(f'Database/drivers.json')


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

    write_to_file(drivers, 'drivers')
    write_to_file(constructors, 'constructors')
    write_to_file(races, 'races')

    return drivers, constructors, races


def upload_data_to_db():
    pass
