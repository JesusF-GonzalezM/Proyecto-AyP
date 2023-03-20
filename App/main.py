import random
import uuid

from App.Races_and_team_management.filter_races import get_constructor_by_country, get_driver_by_constructor, \
    get_races_by_circuit_country, get_races_by_month, show_circuit_country, show_constructor_id, show_countries
from App.Races_and_team_management.finish_race import set_drivers_and_constructors_score, randomize_list, \
    get_winning_constructor, reset_scores
from App.Races_assistance_module.manage_race_assistance import race_assistance_management
from App.Restaurant_management.order_restaurant_products import get_products_by_type, \
    get_products_by_price_range, search_product_generally, get_products_by_name
from App.Restaurant_sale_management.manage_purchases import manage_purchase
from App.Statistics.statistics_calculation import statistics_module
from App.Tickets_sale_management.manage_client_creation import manage_client
from App.Tickets_sale_management.manage_ticket_creation import calculate_total_ticket_price_and_print
from App.parse_data.download_data import initialize_data, download_clients_from_file, upload_data_to_file


# La función principal donde se ejecutan todas las demás funciones
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
    if clients:
        for client in clients:
            client.tickets.sort(key=lambda x: x.type)

    # Borrar esto al terminar, esto es para poblar las clases de información y testear, to lazy to do unittests :D
    for client in clients:
        client.total_spent = random.randint(0, 1000000)
    for race in races:
        race.attendance = random.randint(0, 1000000)
        race.sold_tickets = random.randint(0, 1000000)

    # corro los modulos
    while True:
        print('Choose which module you want to use: ')
        module_to_choose = input('\t1.Races and team management\n\t2.Tickets sale management\n\t'
                                 '3.Races assistance management\n\t4.Restaurants management\n\t'
                                 '5.Restaurants sale management\n\t6.Statistics\n\t7.Exit\n\t'
                                 )
        match module_to_choose:
            case '1':
                # Races and team management Module
                print('Welcome to the Races and team management module!')
                print('------------------------------------------------')
                races_and_team_management(constructors, drivers, races)
            case '2':
                # Tickets sale management Module
                print('Welcome to the Tickets sale management module!')
                print('-----------------------------------------------')
                tickets_sale_management(clients, races)
            case '3':
                # Races assistance management Module
                print('Welcome to the ticket validation module!')
                print('----------------------------------------')
                race_assistance_management(clients, races)
            case '4':
                # Restaurants management Module
                print('Welcome to the restaurant management module!, here you can see our food and drinks by filters!')
                print('-----------------------------------------------------------------------------------------------')
                restaurant_management_module(races)

            case '5':
                # Restaurants sale management Module
                print('Welcome to the restaurant sale management module!')
                restaurant_sales_management(clients, races)
            case '6':
                print('Welcome to the statistics module!')
                print('---------------------------------')
                statistics_module(clients, races)
            case '7':
                print('Goodbye!')
                # Exit and Save
                save_data(clients, constructors, drivers, races)
                quit()
            case _:
                print('Wrong input!')


# Se encarga de generar un codigo unico para cada asiento
def set_unique_code_to_seats(seats):
    for row in seats:
        for seat in row:
            seat.code = uuid.uuid4().hex


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
                randomize_list(drivers)

                set_drivers_and_constructors_score(drivers, constructors)
                print('---------------------------------------------------------------------------')
                print(f'Congratulations to the driver {drivers[0].firstName} {drivers[0].lastName}, '
                      f'for winning in the first place!, scoring {drivers[0].score} points')
                print('---------------------------------------------------------------------------')
                winning_constructor = get_winning_constructor(constructors)
                print('---------------------------------------------------------------------------')
                print(f'Congratulations to the constructor {winning_constructor.name}, for '
                      f'winning in the first place!, scoring {winning_constructor.score} points')
                print('---------------------------------------------------------------------------')

                reset_scores(drivers, constructors)
            case '3':
                print('Goodbye!')
                print('--------')
                break
            case _:
                print('Wrong input')
                print('-----------')


# Se encarga de la venta de tickets delegando responsabilidades en otras funciones
def tickets_sale_management(clients, races):
    while True:
        choice = input(f'1.Buy ticket(s)\n2.Leave\n')
        match choice:
            case '1':

                seats, race_at, client, tickets, client_in_db = manage_client(races, clients)
                total_price = calculate_total_ticket_price_and_print(tickets)
                while True:
                    payment = input('\tDo you want to pay this ticket(s)? (y/n):\n\t')
                    match payment:
                        case 'y':
                            for ticket in tickets:
                                client.add_ticket(ticket)
                            race_at.sold_tickets += len(tickets)
                            client.total_spent += total_price
                            for seat in seats:
                                seat.taken = True
                            if not client_in_db:
                                clients.append(client)
                            print('-------------------------------------')
                            print('Success! Thank you for your purchase!')
                            print('-------------------------------------')
                            break
                        case 'n':
                            for seat in seats:
                                seat.taken = False
                            print('Goodbye!')
                            print('--------')
                            break
                        case _:
                            print('Wrong input!')
                            print('------------')
            case '2':
                print('Goodbye!')
                print('--------')
                break
            case _:
                print('Wrong input!')
                print('------------')


# se encarga de permitir la búsqueda de items en los restaurantes mediante filtros
def restaurant_management_module(races):
    while True:
        choice = input('\t1. Search by filters\n\t2. Leave\n')
        match choice:
            case '1':
                chosen_filter = input(f'\t1. Search by name\n\t2. Search by type\n\t3. Search by price range\n\t')
                match chosen_filter:
                    case '1':
                        while True:
                            choice = input(f'\t1. Search by name generally\n\t2. Search by name in a specific restaurant\n\t')
                            match choice:
                                case '1':
                                    restaurant = search_product_generally(races)
                                    break
                                case '2':
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
                                        print('-------------------------------------------------------------------------------')
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
                                        print('----------------------------------------------------------------------------')
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
                                        print('----------------------------------------------')
                                    # noinspection PyUnboundLocalVariable
                                    found_products = get_products_by_name(restaurant_at.items, product_at.name)
                                    if found_products:
                                        for product in found_products:
                                            print(product)
                                    else:
                                        print(f'{product_index} is not a product in this restaurant')
                                        print('----------------------------------------------------')
                                    break
                                case _:
                                    print('Wrong input!')
                                    print('------------')
                    case '2':
                        chosen_type = input('\t1. drink:alcoholic\n\t2. drink:not-alcoholic\n\t'
                                            '3. food:restaurant\n\t4. food:fast\n')
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('--------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('\t--------------------------------')
                                match chosen_type:
                                    case '1':
                                        filtered_products = get_products_by_type(restaurant.items, 'drink:alcoholic')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print('\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case '2':
                                        filtered_products = get_products_by_type(restaurant.items, 'drink:not-alcoholic')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print(f'\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case '3':
                                        filtered_products = get_products_by_type(restaurant.items, 'food:restaurant')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print(f'\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case '4':
                                        filtered_products = get_products_by_type(restaurant.items, 'food:fast')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print(f'\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case _:
                                        print('Wrong input!')
                                        print('------------')
                                        break
                    case '3':
                        while True:
                            min_price = input('Enter the minimum price you want to search by: ')
                            if min_price.isnumeric():
                                min_price = float(min_price)
                                if min_price >= 0:
                                    break
                            print('That is not a valid minimum price, must be a number and greater than 0')
                            print('----------------------------------------------------------------------')

                        while True:
                            max_price = input('Enter the maximum price you want to search by: ')
                            if max_price.isnumeric():
                                max_price = float(max_price)
                                if max_price > min_price:
                                    break
                            print('That is not a valid maximum price, must be a number and grater than the minimum price')
                            print('-------------------------------------------------------------------------------------')
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('--------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('\t--------------------------------')
                            # noinspection PyUnboundLocalVariable
                            filtered_products = get_products_by_price_range(restaurant.items, min_price, max_price)
                            if filtered_products:
                                for product in filtered_products:
                                    print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                          f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                            else:
                                print('\t\t---------------------------------------------------------------')
                                print('\t\tThere are no products with that price range at this restaurant!')
                                print('\t\t---------------------------------------------------------------')

                    case _:
                        print('Wrong input!')
                        print('------------')
            case '2':
                print('Goodbye!')
                print('--------')
                break
            case _:
                print('Wrong input!')
                print('------------')


# Se encarga de las compras en los restaurantes, y agregarle el costo a una variable en el cliente.
def restaurant_sales_management(clients, races):
    while True:
        choice = input('\t1. Buy products\n\t2. Leave\n')
        match choice:
            case '1':
                client, total_price, restaurant_at, products = manage_purchase(clients, races)
                if not client:
                    break
                if client != 'no restaurants':
                    choice = input(f'1.Pay the products\n2.Cancel Payment\n')
                    match choice:
                        case '1':
                            print('Success! Thank you for your purchase!')
                            print('-------------------------------------')
                            client.total_spent += total_price
                            for item in restaurant_at.items:
                                for product in products:
                                    if product == item:
                                        item.total_sold += 1
                        case '2':
                            for product in products:
                                product.stock += 1
                            print('Goodbye!')
                            print('--------')
                        case _:
                            print('Wrong input!')
                            print('------------')
            case '2':
                print('Goodbye!')
                print('--------')
                break
            case _:
                print('Wrong input!')
                print('------------')


# Se encarga de subir la data a la base de datos
def save_data(clients, constructors, drivers, races):
    upload_data_to_file(drivers, 'drivers')
    upload_data_to_file(constructors, 'constructors')
    upload_data_to_file(races, 'races')
    upload_data_to_file(clients, 'clients')


# Ejecuta el programa principal
if __name__ == '__main__':
    main()
