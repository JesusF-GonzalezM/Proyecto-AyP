import random
from App.Models.client import Client
from App.parse_data.download_data import initialize_data, load_clients_from_file, upload_data_to_file
from App.search_filters.filter_races import get_constructor_by_country, get_driver_by_constructor, \
    get_races_by_circuit_country, get_races_by_month


def generate_unique_ticket_code(clients):
    while True:
        unique_code = random.randint(100000, 999999)
        unique = True
        for client in clients:
            if unique_code == client.ticket_type.code:
                unique = False
                break
        if unique:
            break
    return unique_code


def end_race():
    pass

# Gestión de venta de entradas


def get_client_data(races):
    print('Welcome!, Please enter your information to buy a ticket:\n')
    while True:
        name = input('\tEnter your name: ')
        if name.isalpha():
            name = name.lower()
            break
        print('Name is not valid, please try again.')

    while True:
        id = input('\tEnter your ID: ')
        if id.isnumeric():
            break
        print('ID is not valid, please try again.')

    while True:
        age = input('\tEnter your age: ')
        if age.isnumeric():
            break
        print('Age is not valid, please try again.')

    for race in races:
        print(race)
    valid = False
    while True:
        race_name = input('Enter the name of the race you want to buy a ticket for: ').title()
        for race in races:
            if race.name == race_name:
                valid = True
                break
        if valid:
            break
        print('Race does not exist, please try again.')

    while True:
        print('\tEnter your desired ticket type:')
        print('\t1. VIP')
        ticket_type = input('\t2. GENERAL\n\t')
        if ticket_type == '1' or ticket_type == '2':
            break
        print('Ticket type is not valid, please try again.')

    new_client = Client(name=name, id=id, age=age, race_name=race_name, ticket_type=ticket_type)
    new_client.ticket_type.calculate_price()
    new_client.ticket_type.print_detailed_price()
    return new_client


def set_unique_code_to_ticket(clients):
    if clients:
        unique_ticket_code = generate_unique_ticket_code(clients)
    else:
        unique_ticket_code = random.randint(100000, 999999)
    return unique_ticket_code


def main():
    drivers, constructors, races = initialize_data()
    clients = load_clients_from_file()

    while True:
        print('Choose which module you want to use: ')
        module_to_choose = input('\t1. Races and team management\n\t2. Tickets sale management\n\t'
                                 '3.Races assistance management\n\t4.Restaurants management\n\t'
                                 '5.Restaurants sale management\n\t6.Statistics\n\t7.Exit\n\t'
                                 )
        if module_to_choose == '1':
            choice = input(f'1.Search by filters\n\t2.Manage race\n')
            match choice:
                case '1':
                    type_of_filter = input('Enter the type of filter you want to use:\n\t1.Constructors by country\n\t'
                                           '2.Drivers by constructor\n\t3.Races by circuit\n\t4.Races by month\n')
                    match type_of_filter:
                        case '1':
                            country = input('Enter the country you want to search by: ')
                            filtered_constructors = get_constructor_by_country(constructors, country)
                            for constructor in filtered_constructors:
                                print(constructor)
                        case '2':
                            constructor_id = input('Enter the id of the constructor you want to search by: ')
                            filtered_drivers = get_driver_by_constructor(drivers, constructor_id)
                            for driver in filtered_drivers:
                                print(driver)
                        case '3':
                            circuit_country = input('Enter the country of the circuit you want to search by: ')
                            filtered_races_by_circuit_country = get_races_by_circuit_country(races, circuit_country)
                            for race in filtered_races_by_circuit_country:
                                print(race)
                        case '4':
                            race_month = input('Enter the month of the year you want to search by: ')
                            filtered_races_by_month = get_races_by_month(races, race_month)
                            for race in filtered_races_by_month:
                                print(race)

            if choice == '2':
                pass

        elif module_to_choose == '2':
            client = get_client_data(races)
            client.ticket_type.code = set_unique_code_to_ticket(clients)
            payment = input('\tDo you want to pay this ticket? (y/n):\n\t')
            if payment == 'y':
                print('Success! Thank you for your purchase!')
                clients.append(client)
            else:
                print('Goodbye!')

        elif module_to_choose == '3':
            pass

        elif module_to_choose == '4':
            print('Welcome to the restaurant management system!, here you can see our food and drinks by filters!')
            choice = input('1.Products by name\n\t2.Products by type\n\t3.Products by price_range\n')
            match choice:
                case '1':
                    name = input('Enter the name of the product you want to search by: ')
                case '2':
                    pass
                case '3':
                    pass

        elif module_to_choose == '5':
            pass

        elif module_to_choose == '6':
            pass

        else:
            # TODO: fix clients Upload to database
            for client in clients:
                print(type(client))
            upload_data_to_file(drivers, 'drivers')
            upload_data_to_file(constructors, 'constructors')
            upload_data_to_file(races, 'races')
            upload_data_to_file(clients, 'clients')

            quit()


if __name__ == '__main__':
    main()
