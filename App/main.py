import json
import os

from App.parse_data.download_data import initialize_drivers_from_api, \
    initialize_constructors_from_api, initialize_races_from_api, initialize_drivers, initialize_constructors, \
    initialize_races
from App.parse_data.write_to_file import write_to_file

URL_DRIVERS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/drivers.json'
URL_CONSTRUCTORS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/' \
                   'api-proyecto/main/constructors.json'
URL_RACES = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/races.json'


def check_txt_data():
    return os.path.isfile('Database/drivers.json')


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


def main():
    if not check_txt_data():
        drivers, constructors, races = load_data_from_api_and_save()
    else:
        drivers, constructors, races = load_data_from_txt()


if __name__ == '__main__':
    main()
