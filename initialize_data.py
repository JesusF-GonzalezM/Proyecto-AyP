import json
import requests
from driver import Driver
from constructor import Constructor


def initialize_data_from_api(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data


def parse_drivers(url):
    drivers = []
    dict_drivers = initialize_data_from_api(url)
    for dict_driver in dict_drivers:
        driver = Driver(driver_id=dict_driver['id'],
                        permanent_number=dict_driver['permanentNumber'],
                        code=dict_driver['code'],
                        team=dict_driver['team'],
                        first_name=dict_driver['firstName'],
                        last_name=dict_driver['lastName'],
                        birth_date=dict_driver['dateOfBirth'],
                        nationality=dict_driver['nationality']
                        )
        drivers.append(driver)
    return drivers


def parse_constructors(url):
    constructors = []
    dict_constructors = initialize_data_from_api(url)
    for dict_constructors in dict_constructors:
        constructor = Constructor(
                        constructor_id=dict_constructors['id'],
                        name=dict_constructors['name'],
                        nationality=dict_constructors['nationality']
                        )
        constructors.append(constructor)
    return constructors
