import random
import uuid
from tabulate import tabulate
from math import gcd

from App.Races_and_team_management.filter_races import get_constructor_by_country, get_driver_by_constructor, \
    get_races_by_circuit_country, get_races_by_month, show_circuit_country, show_constructor_id, show_countries
from App.Races_and_team_management.finish_race import set_drivers_and_constructors_score, randomize_list, \
    get_winning_constructor, reset_scores
from App.Restaurant_management.order_restaurant_products import get_products_by_name, get_products_by_type, \
    get_products_by_price_range
from App.Restaurant_sale_management.manage_purchases import manage_purchase, print_receipt
from App.Statistics.statistics_calculation import average_spent_by_vip_client, \
    race_with_more_assistance_and_most_tickets_sold, calculate_top_sold_items_of_restaurant, calculate_top_clients
from App.Tickets_sale_management.manage_client_creation import manage_client
from App.parse_data.download_data import initialize_data, download_clients_from_file, upload_data_to_file

# Diagrama UML pendiente
# README.md pendiente
# Modulo 1 listo a
# Modulo 2 listo a
# Modulo 3 listo a
# Modulo 4 listo a
# Modulo 5 Gestion de venta de restaurantes, falta la parte del inventario.
# Modulo 6 Falta 2 y luego implementarlo en el main()
# noinspection PyUnboundLocalVariable


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


# Mostrar tabla con la asistencia a las carreras de mejor a peor, mostrando el nombre del carrera (nombre de los equipos), estadio en donde se juega, boletos vendidos, personas que asistieron y la relación asistencia/venta
def make_table(races):
    sorted_races = sort_races_by_attendance(races)
    data = {
        'Race_name': [],
        'Circuit': [],
        'Attendance': [],
        'Tickets_sold': [],
        'Attendance/Tickets_sold ratio': []
    }
    for race in sorted_races:

        if race.sold_tickets and race.attendance:
            common_divisor = gcd(race.attendance, race.sold_tickets)
            numerator = race.attendance // common_divisor
            denominator = race.sold_tickets // common_divisor
        data['Race_name'].append(race.name)
        data['Circuit'].append(race.circuit.name)
        data['Attendance'].append(race.attendance)
        data['Tickets_sold'].append(race.sold_tickets)
        # noinspection PyUnboundLocalVariable
        data['Attendance/Tickets_sold ratio'].append(f'{numerator}/{denominator}')

    print(tabulate(data, headers='keys', tablefmt='fancy_grid', showindex='always'))


# Ordena las carreras por asistencias.
def sort_races_by_attendance(races):
    sorted_races = sorted(races, key=lambda race: race.attendance, reverse=True)
    return sorted_races


# Se encarga de generar todas las estadísticas
def statistics_module(clients, races):
    highest_attendance, most_tickets_sold = race_with_more_assistance_and_most_tickets_sold(races)
    while True:
        choice = input("\t1. Average spending's of a VIP client\n\t2. Show table of races assistance\n\t"
                       "3.Race with highest attendance\n\t4. Race with most sold tickets\n\t"
                       "5. Top 3 products sold by a restaurant\n\t6. Top 3 clients with more tickets\n\t"
                       "7.Graphics of all the statistics\n\t8.Exit\n\t")
        match choice:
            case '1':
                average_spent = average_spent_by_vip_client(clients)
                print(f'Average spending of a VIP client:\n\t{average_spent}')
            case '2':
                make_table(races)
            case '3':
                print('---------------------------------------------')
                print(f'Highest attendance:\n\t{highest_attendance}')
                highest_attendance.pretty_print_attendance()
                print('---------------------------------------------')
            case '4':
                print('---------------------------------------------')
                print(f'Highest attendance:\n\t{most_tickets_sold}')
                highest_attendance.pretty_print_sold_tickets()
                print('---------------------------------------------')
            case '5':
                for race in races:
                    print(f'RACE: {race.name}')
                    print('---------------------------------------------')
                    for restaurant in race.restaurants:
                        print(f'\tRESTAURANT: {restaurant.name}')
                        print('---------------------------------------------')
                        top_items_sold = calculate_top_sold_items_of_restaurant(restaurant.items)
                        for index, item in enumerate(top_items_sold):
                            print(f'\tTOP {index + 1}:\n\tProduct: {item.name}\n\ttotal sales: {item.total_sold}\n')
                        print('---------------------------------------------')
            case '6':
                top_clients = calculate_top_clients(clients)
                for index, client in enumerate(top_clients):
                    print(f'\tTOP {index + 1}:\n\tName: {client.name}\n\ttotal tickets: {len(client.tickets)}\n')
                    print('---------------------------------------------')
            case '7':
                pass
                # Hacer gráficos con libraries.
            case '8':
                print('Goodbye!')
                break
            case _:
                print('Wrong input!')


# Se encarga de manejar la asistencia de los clientes, y verificar que las entradas sean válidas
def race_assistance_management(clients, races):
    while True:
        choice = input('\t1. Enter the race\n\t2. Leave\n')
        match choice:
            case '1':
                if not clients:
                    print('There are no clients in the database!')
                    return
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
                is_valid = False
                # noinspection PyUnboundLocalVariable
                for ticket in current_client.tickets:
                    # noinspection PyUnboundLocalVariable
                    if ticket.race_round == current_race_index:
                        if ticket.type.value == '1':
                            # noinspection PyUnboundLocalVariable
                            is_valid = check_if_ticket_code_is_valid(current_race, current_race.vip_seats, is_valid, ticket)
                        if ticket.type.value == '2':
                            # noinspection PyUnboundLocalVariable
                            is_valid = check_if_ticket_code_is_valid(current_race, current_race.general_seats, is_valid, ticket)
                    if is_valid:
                        break
                if not is_valid:
                    print('----------------------------------------')
                    print('You dont have any ticket for this race!')
                    print('----------------------------------------')
            case '2':
                print('Thank you for using the Races and team management module!')
                break
            case _:
                print('Wrong input!')


# revisa si el codigo del ticket es válido
def check_if_ticket_code_is_valid(current_race, seats, is_valid, ticket):
    for row in seats:
        for seat in row:
            if seat.code == ticket.code:
                if not seat.assisted:
                    seat.assisted = True
                    current_race.attendance += 1
                print('----------------------------')
                print(f'Welcome to the race, enjoy!')
                print('----------------------------')
                print(f'Your seat is the {seat.position} | row {seat.position[0]} | column {seat.position[1]} |')
                print('----------------------------')
                is_valid = True
                break
    return is_valid


# se encarga de permitir la búsqueda de items en los restaurantes mediante filtros
def restaurant_management_module(races):
    while True:
        choice = input('\t1. Search by filters\n\t2. Leave\n')
        match choice:
            case '1':
                chosen_filter = input(f'\t1. Search by name\n\t2. Search by type\n\t3. Search by price range\n\t')
                match chosen_filter:
                    case '1':
                        product_name = input('Enter the name of the product you want to search: ')
                        for race in races:
                            for restaurant in race.restaurants:
                                filtered_products = get_products_by_name(restaurant.items, product_name)
                                if filtered_products:
                                    print(f'RACE: {race.name}')
                                    print('--------------------------------')
                                    print(f'\tRESTAURANT: {restaurant.name}')
                                    print('--------------------------------')
                                for product in filtered_products:
                                    print(f'\t\tname: {product.name} | type: {product.type} | price: {product.price} |')
                    case '2':
                        chosen_type = input('\t1. drink:alcoholic\n\t2. drink:not-alcoholic\n\t'
                                            '3. food:restaurant\n\t4. food:fast\n')
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('--------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('--------------------------------')
                                match chosen_type:
                                    case '1':
                                        filtered_products = get_products_by_type(restaurant.items, 'drink:alcoholic')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'name: {product.name} | type: {product.type} | price: {product}')
                                        else:
                                            print('There are no products with that type at this restaurant!')
                                            print('--------------------------------------------------------')
                                    case '2':
                                        filtered_products = get_products_by_type(restaurant.items, 'drink:not-alcoholic')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'name: {product.name} | type: {product.type} | price: {product}')
                                        else:
                                            print(f'There are no products with that type at this restaurant!')
                                            print('--------------------------------------------------------')
                                    case '3':
                                        filtered_products = get_products_by_type(restaurant.items, 'food:restaurant')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'name: {product.name} | type: {product.type} | price: {product}')
                                        else:
                                            print(f'There are no products with that type at this restaurant!')
                                            print('--------------------------------------------------------')
                                    case '4':
                                        filtered_products = get_products_by_type(restaurant.items, 'food:fast')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'name: {product.name} | type: {product.type} | price: {product}')
                                        else:
                                            print(f'There are no products with that type at this restaurant!')
                                            print('--------------------------------------------------------')
                                    case _:
                                        print('Wrong input!')
                                        break
                    case '3':
                        while True:
                            min_price = input('Enter the minimum price you want to search by: ')
                            if min_price.isnumeric():
                                min_price = float(min_price)
                                if min_price > 0:
                                    break
                            print('That is not a valid minimum price, must be a number and greater than 0')

                        while True:
                            max_price = input('Enter the maximum price you want to search by: ')
                            if max_price.isnumeric():
                                max_price = float(max_price)
                                if max_price > min_price:
                                    break
                            print('That is not a valid maximum price, must be a number and grater than the minimum price')
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('--------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('--------------------------------')
                            # noinspection PyUnboundLocalVariable
                            filtered_products = get_products_by_price_range(restaurant.items, min_price, max_price)
                            if filtered_products:
                                for product in filtered_products:
                                    print(f'name: {product.name} | type: {product.type} | price: {product}')
                            else:
                                print('There are no products with that price range at this restaurant!')
                                print('---------------------------------------------------------------')

                    case _:
                        print('Wrong input!')
            case '2':
                print('Goodbye!')
                break
            case _:
                print('Wrong input!')


# Se encarga de generar un codigo unico para cada asiento
def set_unique_code_to_seats(seats):
    for row in seats:
        for seat in row:
            seat.code = uuid.uuid4().hex


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
                            client.total_spent += total_price
                            for item in restaurant_at.items:
                                for product in products:
                                    if product == item:
                                        item.total_sold += 1
                        case '2':
                            # TODO: Remove from restaurant inventory
                            #for item in restaurant_at.items:
                                #for product in products:
                                    #if product == item:
                                        #item.inventory += 1
                            print('Goodbye!')
                        case _:
                            print('Wrong input!')
            case '2':
                print('Goodbye!')
                break
            case _:
                print('Wrong input!')


# Se encarga de la venta de tickets delegando responsabilidades en otras funciones
def tickets_sale_management(clients, races):
    while True:
        choice = input(f'1.Buy ticket(s)\n2.Leave\n')
        match choice:
            case '1':

                seats, race_at, client, tickets, client_in_db = manage_client(races, clients)
                total_price = calculate_total_ticket_price_and_print(tickets)
                payment = input('\tDo you want to pay this ticket(s)? (y/n):\n\t')
                if payment == 'y':
                    for ticket in tickets:
                        client.add_ticket(ticket)
                    race_at.sold_tickets += len(tickets)
                    client.total_spent += total_price
                    for seat in seats:
                        seat.taken = True
                    if not client_in_db:
                        clients.append(client)
                    print('Success! Thank you for your purchase!')
                else:
                    for seat in seats:
                        seat.taken = False
                    print('Goodbye!')
            case '2':
                print('Goodbye!')
                break
            case _:
                print('Wrong input!')


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
                print('Goodbye!')
                break

            case _:
                print('Wrong input')


# se encarga de calcular el costo total del los tickets a comprar
def calculate_total_ticket_price_and_print(tickets):
    base_price = 0
    discount = 0
    for ticket in tickets:
        base_price += ticket.total_price
    if tickets[0].discount:
        discount = base_price * 0.5
    total_price = base_price - discount
    iva = total_price * 0.16
    total_price = total_price + iva
    print_receipt(base_price, total_price, iva, discount)
    return total_price


# Ejecuta el programa principal
if __name__ == '__main__':
    main()
