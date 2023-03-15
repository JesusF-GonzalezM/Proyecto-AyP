def get_constructor_by_country(constructors, country):
    return filter(lambda constructor: constructor.nationality == country.title(), constructors)


def get_driver_by_constructor(drivers, constructor_id):
    return filter(lambda driver: driver.team == constructor_id.lower(), drivers)


def get_races_by_circuit_country(races, circuit_country):
    return filter(lambda race: race.circuit.location.country == circuit_country, races)


def get_races_by_month(races, month):
    if len(month) == 1:
        month = '0' + month
    filtered_races = []
    for race in races:
        race_month = race.date.split('-')[1]
        if race_month == month:
            filtered_races.append(race)
    return filtered_races


def show_countries(constructors):
    countries = set()
    for constructor in constructors:
        countries.add(constructor.nationality)
    for country in countries:
        print(country)


def show_constructor_id(constructors):
    for constructor in constructors:
        print(constructor.id)


def show_circuit_country(races):
    for race in races:
        print(race.circuit.location.country)
