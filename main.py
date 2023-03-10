from initialize_data import parse_drivers, parse_constructors

URL_DRIVERS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/drivers.json'
URL_CONSTRUCTORS = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/' \
                   'api-proyecto/main/constructors.json'
URL_RACES = 'https://raw.githubusercontent.com/Algorimtos-y-Programacion-2223-2/api-proyecto/main/races.json'


def main():
    drivers = parse_drivers(URL_DRIVERS)
    for driver in drivers:
        print(driver)

    constructors = parse_constructors(URL_CONSTRUCTORS)
    for constructor in constructors:
        print(constructor)


if __name__ == '__main__':
    main()
