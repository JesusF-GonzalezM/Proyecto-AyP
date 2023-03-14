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
        year, race_month, day = race.date.split('-')
        if race_month == month:
            filtered_races.append(race)
    return filtered_races
