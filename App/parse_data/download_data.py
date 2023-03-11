import requests
from App.Models.constructor import Constructor
from App.Models.driver import Driver
from App.Models.race import Race


def initialize_drivers(data_array):
    drivers = []
    for data in data_array:
        driver = Driver(**data)
        drivers.append(driver)
    return drivers


def initialize_drivers_from_api(url):
    response = requests.get(url)
    data_array = response.json()
    return initialize_drivers(data_array)


def initialize_drivers_from_txt(file_path):
    # read from the file
    return initialize_drivers(file_path)


def initialize_constructors(data_array):
    constructors = []
    for data in data_array:
        constructor = Constructor(**data)
        constructors.append(constructor)
    return constructors


def initialize_constructors_from_api(url):
    response = requests.get(url)
    data_array = response.json()
    return initialize_constructors(data_array)


def initialize_constructors_from_txt(file_path):
    return


def initialize_races(data_array):
    races = []
    for data in data_array:
        race = Race(**data)
        races.append(race)
    return races


def initialize_races_from_api(url):
    response = requests.get(url)
    data_array = response.json()
    return initialize_races(data_array)
