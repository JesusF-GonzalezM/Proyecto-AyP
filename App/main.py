import uuid

from App.Races_and_team_management.filter_races import get_constructor_by_country, get_driver_by_constructor, \
    get_races_by_circuit_country, get_races_by_month, show_circuit_country, show_constructor_id, show_countries
from App.Races_and_team_management.finish_race import set_drivers_and_constructors_score, randomize_list, \
    get_winning_constructor, reset_scores
from App.Restaurant_sale_management.manage_purchases import manage_purchase
from App.Tickets_sale_management.manage_client_creation import manage_client
from App.parse_data.download_data import initialize_data, download_clients_from_file, upload_data_to_file

# Modulo 1 listo
# Modulo 2 listo
# Modulo 3 Gestion de Asistencia de Carreras pendiente
# Modulo 4 Gestion de Restaurantes filtros listos, lo demás pendiente.
# Modulo 5 Gestion de venta de restaurantes, pendiente terminar
# Modulo 6 Estadísticas pendientes


def main():
    drivers, constructors, races = initialize_data()
    clients = download_clients_from_file()
    for race in races:
        if not race.general_seats:
            race.define_general_seats_matrix()
            set_unique_code_to_seats(race.general_seats)
        if not race.vip_seats:
            race.define_vip_seats_matrix()
            set_unique_code_to_seats(race.vip_seats)

    while True:
        print('Choose which module you want to use: ')
        module_to_choose = input('\t1. Races and team management\n\t2. Tickets sale management\n\t'
                                 '3.Races assistance management\n\t4.Restaurants management\n\t'
                                 '5.Restaurants sale management\n\t6.Statistics\n\t7.Exit\n\t'
                                 )
        match module_to_choose:
            # Races and team management Module
            case '1':
                races_and_team_management(constructors, drivers, races)
            # Tickets sale management Module
            case '2':
                tickets_sale_management(clients, races)
            # Races assistance management Module
            case '3':
                print('Welcome to the ticket validation system!')
            # Restaurants management Module
            case '4':
                print('Welcome to the restaurant management system!, here you can see our food and drinks by filters!')
                choice = input('1.Products by name\n\t2.Products by type\n\t3.Products by price_range\n')
                match choice:
                    case '1':
                        restaurant = input('Enter the name of the restaurant you want to search the products by: ')
                        name = input('Enter the name of the product you want to search by: ')
                        print(name, restaurant)
                    case '2':
                        pass
                    case '3':
                        pass
            # Restaurants sale management Module
            case '5':
                restaurant_sales_management(clients, races)
            # Statistics Module
            case '6':
                pass
            # Exit and Save
            case _:
                save_data(clients, constructors, drivers, races)

                quit()


def set_unique_code_to_seats(seats):
    for row in seats:
        for seat in row:
            seat.code = uuid.uuid4().hex


def restaurant_sales_management(clients, races):
    client, total_price = manage_purchase(clients, races)
    if client != 'no restaurants':
        choice = input(f'1.Pay the products\n2.Cancel Payment\n')
        if choice == '1':
            print('Success! Thank you for your purchase!')
            client.total_spent += total_price
            # TODO: Remove from restaurant inventory


def tickets_sale_management(clients, races):
    while True:
        choice = input(f'1.Buy ticket\n2.Leave\n')
        match choice:
            case '1':

                seat, race_at, client, ticket, client_in_db = manage_client(races, clients)
                payment = input('\tDo you want to pay this ticket? (y/n):\n\t')
                if payment == 'y':
                    client.add_ticket(ticket)
                    client.total_spent += ticket.total_price
                    race_at.sold_tickets += 1
                    seat.taken = True
                    if not client_in_db:
                        clients.append(client)
                    print('Success! Thank you for your purchase!')
                else:
                    print('Goodbye!')
            case _:
                break


def save_data(clients, constructors, drivers, races):
    upload_data_to_file(drivers, 'drivers')
    upload_data_to_file(constructors, 'constructors')
    upload_data_to_file(races, 'races')
    upload_data_to_file(clients, 'clients')


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
                        show_countries(constructors)
                        country = input('Enter the country you want to search by: ')
                        filtered_constructors = get_constructor_by_country(constructors, country)
                        for constructor in filtered_constructors:
                            print(constructor)
                    case '2':
                        show_constructor_id(constructors)
                        constructor_id = input('Enter the id of the constructor you want to search by: ')
                        filtered_drivers = get_driver_by_constructor(drivers, constructor_id)
                        for driver in filtered_drivers:
                            print(driver)
                    case '3':
                        show_circuit_country(races)
                        circuit_country = input('Enter the country of the circuit you want to search by: ')
                        filtered_races_by_circuit_country = \
                            get_races_by_circuit_country(races, circuit_country)
                        for race in filtered_races_by_circuit_country:
                            print(race)
                    case '4':
                        while True:
                            race_month = input('Enter the month(in numbers) of the year you want to search by: ')
                            if race_month.isnumeric() and 0 < int(race_month) < 13:
                                filtered_races_by_month = get_races_by_month(races, race_month)
                                for race in filtered_races_by_month:
                                    print(race)
                                    break
                            print('Invalid month')
                    case _:
                        break

            case '2':
                randomize_list(drivers)

                set_drivers_and_constructors_score(drivers, constructors)
                print(f'Congratulations to the driver {drivers[0].firstName} {drivers[0].lastName}, '
                      f'for winning in the first place!, scoring {drivers[0].score} points')

                winning_constructor = get_winning_constructor(constructors)
                print(f'Congratulations to the constructor {winning_constructor.name}, for '
                      f'winning in the first place!, scoring {winning_constructor.score} points')

                reset_scores(drivers, constructors)
            case '3':
                break


if __name__ == '__main__':
    main()
