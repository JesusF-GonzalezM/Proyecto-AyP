import json
import os
import requests

from App.parse_data.initialize_data import initialize_clients, initialize_drivers, initialize_constructors, \
    initialize_races

URL_DRIVERS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/drivers.json'
URL_CONSTRUCTORS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/' \
                   'api-proyecto/main/constructors.json'
URL_RACES = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/races.json'


# Sube la data a los archivos
def upload_data_to_file(obj, filename):
    json_string = json.dumps(obj, default=lambda o: o.__dict__, indent=4)
    with open(f"Database/{filename}.json", "w") as json_file:
        json_file.write(json_string)


# descarga los clientes de los archivos
def download_clients_from_file():
    clients = []
    if check_txt_data('clients'):
        with open('Database/clients.json', 'r') as clients_file:
            json_clients = json.load(clients_file)
            clients = initialize_clients(json_clients)
    return clients


# descarga los drivers de la api
def download_drivers_from_api(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Exception occurred while code execution')
        print('There is no connection, program aborting...')
        raise SystemExit(e)
    data_array = response.json()
    return initialize_drivers(data_array)


# descarga los constructors de la api
def download_constructors_from_api(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Exception occurred while code execution')
        print('There is no connection, program aborting...')
        raise SystemExit(e)
    data_array = response.json()
    return initialize_constructors(data_array)


# descarga las carreras de la api
def download_races_from_api(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Exception occurred while code execution')
        print('There is no connection, program aborting...')
        raise SystemExit(e)
    data_array = response.json()
    return initialize_races(data_array)


# descarga la data de los archivos
def download_data_from_txt():
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


# descarga toda la data de las apis y la salva en archivos locales
def load_data_from_api_and_save():
    drivers = download_drivers_from_api(URL_DRIVERS)
    constructors = download_constructors_from_api(URL_CONSTRUCTORS)
    races = download_races_from_api(URL_RACES)

    upload_data_to_file(drivers, 'drivers')
    upload_data_to_file(constructors, 'constructors')
    upload_data_to_file(races, 'races')

    return drivers, constructors, races


# revisa si el archivo existe o no
def check_txt_data(file_path):
    return os.path.isfile(f'Database/{file_path}.json')


# inicializa la data de la api o de los archivos, dependiendo si los archivos existen
def initialize_data():
    if not check_txt_data('races'):
        drivers, constructors, races = load_data_from_api_and_save()
    else:
        drivers, constructors, races = download_data_from_txt()
    return drivers, constructors, races
