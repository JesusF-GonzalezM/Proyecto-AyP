# filtra los constructors por pais
def get_constructor_by_country(constructors, country):
    return filter(lambda constructor: constructor.nationality == country.title(), constructors)


# filtra los drivers por constructor
def get_driver_by_constructor(drivers, constructor_id):
    return filter(lambda driver: driver.team == constructor_id.lower(), drivers)


# filtra las carreras por pais del circuito
def get_races_by_circuit_country(races, circuit_country):
    return filter(lambda race: race.circuit.location.country == circuit_country, races)


# filtra las carreras por mes
def get_races_by_month(races, month):
    if len(month) == 1:
        month = '0' + month
    filtered_races = []
    for race in races:
        race_month = race.date.split('-')[1]
        if race_month == month:
            filtered_races.append(race)
    return filtered_races


# Imprime los paises
def show_countries(constructors):
    countries = set()
    for constructor in constructors:
        countries.add(constructor.nationality)
    for country in countries:
        print(country)


# imprime los ID de los constructors
def show_constructor_id(constructors):
    for constructor in constructors:
        print(constructor.id)


# imprime los paises de cada circuito
def show_circuit_country(races):
    for race in races:
        print(race.circuit.location.country)
