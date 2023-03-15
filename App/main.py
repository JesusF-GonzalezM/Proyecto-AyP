import uuid

from App.Races_and_team_management.filter_races import get_constructor_by_country, get_driver_by_constructor, \
    get_races_by_circuit_country, get_races_by_month, show_circuit_country, show_constructor_id, show_countries
from App.Races_and_team_management.finish_race import set_drivers_and_constructors_score, randomize_list, \
    get_winning_constructor, reset_scores
from App.Restaurant_management.order_restaurant_products import get_product_by_name, get_products_by_type, \
    get_products_by_price_range
from App.Restaurant_sale_management.manage_purchases import manage_purchase
from App.Tickets_sale_management.manage_client_creation import manage_client
from App.parse_data.download_data import initialize_data, download_clients_from_file, upload_data_to_file


# Modulo 1 listo
# Modulo 2 listo
# Modulo 3 listo
# Modulo 4 listo
# Modulo 5 Gestion de venta de restaurantes, pendiente terminar, arreglar.
# Modulo 6 Falta 2, 5 y 7 y luego implementarlo en el main()
# noinspection PyUnboundLocalVariable


def main():
    # inicializo la información, si no existen los archivos, la bajo de la api, sino, la bajo de los archivos
    drivers, constructors, races = initialize_data()
    clients = download_clients_from_file()
    # si las matrices de los asientos no están inicializadas todavía, las inicializo y le agrego el codigo unico a cada asiento.
    for race in races:
        if not race.general_seats:
            race.define_general_seats_matrix()
            set_unique_code_to_seats(race.general_seats)
        if not race.vip_seats:
            race.define_vip_seats_matrix()
            set_unique_code_to_seats(race.vip_seats)

    # corro los modulos
    while True:
        print('Choose which module you want to use: ')
        module_to_choose = input('\t1. Races and team management\n\t2. Tickets sale management\n\t'
                                 '3.Races assistance management\n\t4.Restaurants management\n\t'
                                 '5.Restaurants sale management\n\t6.Statistics\n\t7.Exit\n\t'
                                 )
        match module_to_choose:
            case '1':
                # Races and team management Module
                print('Welcome to the Races and team management module!')
                races_and_team_management(constructors, drivers, races)
            case '2':
                # Tickets sale management Module
                print('Welcome to the Tickets sale management module!')
                tickets_sale_management(clients, races)
            case '3':
                # Races assistance management Module
                print('Welcome to the ticket validation module!')
                race_assistance_management(clients, races)
            case '4':
                # Restaurants management Module
                print('Welcome to the restaurant management module!, here you can see our food and drinks by filters!')
                restaurant_management_module(races)

            case '5':
                # Restaurants sale management Module
                restaurant_sales_management(clients, races)
            case '6':
                # Statistics Module
                pass
            case _:
                # Exit and Save
                save_data(clients, constructors, drivers, races)

                quit()


# Se encarga de manejar la asistencia de los clientes, y verificar que las entradas sean válidas
def race_assistance_management(clients, races):
    for index, race in enumerate(races):
        print(f'{index + 1}. {race.name}')
    while True:
        is_valid = False
        chosen_race_round = input('Choose the race you are trying to get into: ')
        for index, race in enumerate(races):
            if chosen_race_round == str(index + 1):
                is_valid = True
                current_race = race
                current_race_index = str(index + 1)
                break
        if is_valid:
            break
        print('That is not a valid race!')
    while True:
        is_valid = False
        client_id = input('Enter your id so we can verify your ticket: ')
        if client_id.isnumeric():
            for client in clients:
                if client.id == client_id:
                    is_valid = True
                    current_client = client
                    break
            if is_valid:
                break
            print('That is not a valid id!')
    # noinspection PyUnboundLocalVariable
    for ticket in current_client.tickets:
        # noinspection PyUnboundLocalVariable
        if ticket.race_round == current_race_index:
            if ticket.type == '1':
                # noinspection PyUnboundLocalVariable
                for row in current_race.vip_seats:
                    for seat in row:
                        if seat.code == ticket.code:
                            seat.assisted = True
                            current_race.attendance += 1
            print(f'Welcome to the race, enjoy!')
            break
        print('You dont have any ticket for this race!')


def restaurant_management_module(races):
    for race in races:
        print(f'{race.round}. {race.name}')
    while True:
        is_valid = False
        race_round = input('Which race restaurants do you want to see:\n')
        for race in races:
            if race_round == race.round:
                if race.restaurants:
                    race_at = race
                    is_valid = True
                    break
        if is_valid:
            break
        print(f'{race_round} is not a valid race choice or race does not have any restaurants!')
    # noinspection PyUnboundLocalVariable
    for index, restaurant in enumerate(race_at.restaurants):
        print(f'{index + 1}. {restaurant.name}')
    while True:
        is_valid = False
        restaurant_choice = input('Which restaurant do you want to see:\n')
        for index, restaurant in enumerate(race_at.restaurants):
            if str(index + 1) == restaurant_choice:
                if restaurant.items:
                    is_valid = True
                    restaurant_at = restaurant
                    break
        if is_valid:
            break
        print(f'{restaurant_choice} is not a valid restaurant choice or restaurant is empty')
    choice = input('1.Products by name\n2.Products by type\n3.Products by price_range\n')
    match choice:
        case '1':
            # noinspection PyUnboundLocalVariable
            for index, item in enumerate(restaurant_at.items):
                print(f'{index + 1}. {item.name}')
            while True:
                is_valid = False
                product_index = input('Enter the product you want to search by: ')
                for index, item in enumerate(restaurant_at.items):
                    if str(index + 1) == product_index:
                        is_valid = True
                        product_at = item
                        break
                if is_valid:
                    break
                print(f'{product_index} is not a valid product choice')
            # noinspection PyUnboundLocalVariable
            found_product = get_product_by_name(restaurant_at.items, product_at.name)
            if found_product:
                print(found_product)
            else:
                print(f'{product_index} is not a product in this restaurant')
        case '2':
            choice = input(f'Enter the product types you want to search by: \n\t1. drink:alcoholic\n\t'
                           f'2. drink:not-alcoholic\n\t3. food:restaurant\n\t4. food:fast\n')
            match choice:
                case '1':
                    # noinspection PyUnboundLocalVariable
                    filtered_products = get_products_by_type(restaurant_at.items, 'drink:alcoholic')
                    if filtered_products:
                        for product in filtered_products:
                            print(product)
                    else:
                        print('There are no alcoholic drinks in this restaurant')
                case '2':
                    # noinspection PyUnboundLocalVariable
                    filtered_products = get_products_by_type(restaurant_at.items, 'drink:not-alcoholic')
                    if filtered_products:
                        for product in filtered_products:
                            print(product)
                    else:
                        print('There are no non alcoholic drinks in this restaurant')
                case '3':
                    # noinspection PyUnboundLocalVariable
                    filtered_products = get_products_by_type(restaurant_at.items, 'food:restaurant')
                    if filtered_products:
                        for product in filtered_products:
                            print(product)
                    else:
                        print('There are not eat-in-restaurant foods in this restaurant')
                case '4':
                    # noinspection PyUnboundLocalVariable
                    filtered_products = get_products_by_type(restaurant_at.items, 'food:fast')
                    if filtered_products:
                        for product in filtered_products:
                            print(product)
                    else:
                        print('There are no fast foods in this restaurant')
                case _:
                    print('Invalid choice')

        case '3':
            min_price = float(input('Enter the minimum price you want to search by: '))
            max_price = float(input('Enter the maximum price you want to search by: '))
            # noinspection PyUnboundLocalVariable
            filtered_products = get_products_by_price_range(restaurant_at.items, min_price, max_price)
            if filtered_products:
                for product in filtered_products:
                    print(product)
            else:
                print(f'No products found by the price range {min_price} to {max_price}')


# Se encarga de generar un codigo unico para cada asiento
def set_unique_code_to_seats(seats):
    for row in seats:
        for seat in row:
            seat.code = uuid.uuid4().hex


# Se encarga de las compras en los restaurantes, y agregarle el costo a una variable en el cliente.
def restaurant_sales_management(clients, races):
    client, total_price, restaurant_at = manage_purchase(clients, races)
    if client != 'no restaurants':
        choice = input(f'1.Pay the products\n2.Cancel Payment\n')
        if choice == '1':
            print('Success! Thank you for your purchase!')
            client.total_spent += total_price
            # TODO: Remove from restaurant inventory


# Se encarga de la venta de tickets delegando responsabilidades en otras funciones
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


# Se encarga de subir la data a la base de datos
def save_data(clients, constructors, drivers, races):
    upload_data_to_file(drivers, 'drivers')
    upload_data_to_file(constructors, 'constructors')
    upload_data_to_file(races, 'races')
    upload_data_to_file(clients, 'clients')


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


# Ejecuta el programa principal
if __name__ == '__main__':
    main()
