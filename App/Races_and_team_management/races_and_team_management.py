from App.Races_and_team_management.filter_races import show_countries, get_constructor_by_country, show_constructor_id, \
    get_driver_by_constructor, show_circuit_country, get_races_by_circuit_country, get_races_by_month
from App.Races_and_team_management.finish_race import set_drivers_and_constructors_score, get_winning_constructor, \
    randomize_list


# Se encarga de que se pueda buscar por filtros cierta información, y se pueda finalizar una carrera.
def races_and_team_management(constructors, drivers, races):
    while True:
        choice = input(f'1.Search by filters\n2.Finish race\n3.Leave\n')
        match choice:
            case '1':
                type_of_filter = input('Enter the type of filter you want to use:'
                                       '\n\t1.Constructors by country'
                                       '\n\t2.Drivers by constructor'
                                       '\n\t3.Races by circuit'
                                       '\n\t4.Races by month'
                                       '\n\t5.Leave\n')
                match type_of_filter:
                    case '1':
                        countries = show_countries(constructors)
                        while True:
                            chosen_country = input('Choose the country you want to search by: ')
                            if chosen_country.isnumeric():
                                if 0 < int(chosen_country) <= len(countries):
                                    chosen_country = countries[int(chosen_country) - 1]
                                    filtered_constructors = get_constructor_by_country(constructors, chosen_country)
                                    for constructor in filtered_constructors:
                                        print(constructor)
                                    break
                            print('Invalid country choice')
                            print('----------------------')
                    case '2':
                        show_constructor_id(constructors)
                        while True:
                            constructor_id = input('Choose the constructor you want to search drivers by: ')
                            if constructor_id.isnumeric():
                                if 0 < int(constructor_id) <= len(constructors):
                                    constructor_id = constructors[int(constructor_id) - 1].id
                                    filtered_drivers = get_driver_by_constructor(drivers, constructor_id)
                                    for driver in filtered_drivers:
                                        print(driver)
                                    break
                            print('Invalid constructor choice')
                            print('--------------------------')
                    case '3':
                        show_circuit_country(races)
                        while True:
                            circuit_country = input('Choose the country of the circuit you want to search by: ')
                            if circuit_country.isnumeric():
                                if 0 < int(circuit_country) <= len(races):
                                    circuit_country = races[int(circuit_country) - 1].circuit.location.country
                                    filtered_races_by_circuit_country = \
                                        get_races_by_circuit_country(races, circuit_country)
                                    if filtered_races_by_circuit_country:
                                        for race in filtered_races_by_circuit_country:
                                            print(race)
                                        break
                            print('Invalid country choice')
                            print('----------------------')
                    case '4':
                        while True:
                            race_month = input('Enter the month(in numbers) of the year you want to search by: ')
                            if race_month.isnumeric() and 0 < int(race_month) < 13:
                                filtered_races_by_month = get_races_by_month(races, race_month)
                                if filtered_races_by_month:
                                    for race in filtered_races_by_month:
                                        print(race)
                                else:
                                    print(f'There are no races in this month')
                                    print('---------------------------------')
                                break
                            print('Invalid month')
                            print('-------------')
                    case _:
                        break

            case '2':
                races_available = False
                for race in races:
                    if not race.finished:
                        races_available = True
                        break
                if not races_available:
                    print('----------------------------')
                    print('There are no races available')
                    print('----------------------------')
                    break
                finished = False
                for race in races:
                    if not race.finished:
                        print(race)
                while True:
                    chosen_race = input('Select a race round to finish: ')
                    if chosen_race.isnumeric():
                        if 0 < int(chosen_race) <= 23:
                            for race in races:
                                if chosen_race == race.round:
                                    chosen_race = race
                                    break
                            if not chosen_race.finished:
                                break
                            else:
                                finished = True
                    if not finished:
                        print('Invalid input')
                        print('-------------')
                    else:
                        print('That race finished already!')
                        print('---------------------------')
                print('CHOSEN RACE:')
                print('--------------------------------')
                print(chosen_race)
                drivers_podium = drivers.copy()
                randomize_list(drivers_podium)
                constructors_podium = constructors.copy()
                set_drivers_and_constructors_score(drivers_podium, constructors_podium)
                print('---------------------------------------------------------------------------')
                print(f'Congratulations to the driver {drivers_podium[0].firstName} {drivers_podium[0].lastName}, '
                      f'for winning in the first place!, scoring {drivers_podium[0].score} points')
                print('---------------------------------------------------------------------------')
                print('All Drivers score:')
                for driver in drivers_podium:
                    print(f'{driver.firstName} {driver.lastName}: {driver.score} points')
                winning_constructor = get_winning_constructor(constructors_podium)
                print('---------------------------------------------------------------------------')
                print(f'Congratulations to the constructor {winning_constructor.name}, for '
                      f'winning in the first place!, scoring {winning_constructor.score} points')
                print('---------------------------------------------------------------------------')
                chosen_race.drivers_podium = drivers_podium[:10]
                chosen_race.winning_constructor = winning_constructor
                chosen_race.finished = True
            case '3':
                print('Goodbye!')
                print('--------')
                break
            case _:
                print('Wrong input')
                print('-----------')
