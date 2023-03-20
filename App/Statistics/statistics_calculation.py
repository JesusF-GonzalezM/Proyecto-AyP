from math import gcd
from tabulate import tabulate
import matplotlib.pyplot as plt


# Se encarga de generar todas las estadísticas
def statistics_module(clients, races):
    sorted_races = sort_races_by_attendance(races)
    highest_attendance, most_tickets_sold = race_with_more_assistance_and_most_tickets_sold(races)
    table = make_table(sorted_races)
    top_clients = calculate_top_clients(clients)
    while True:
        choice = input("\t1.Average spending's of a VIP client in a race\n\t2.Show table of races assistance\n\t"
                       "3.Race with highest attendance\n\t4.Race with most sold tickets\n\t"
                       "5.Top 3 products sold by a restaurant\n\t6.Top 3 clients with more tickets\n\t"
                       "7.Exit\n\t")
        match choice:
            case '1':
                for index, race in enumerate(races):
                    print(f'{index + 1}. {race.name}')
                while True:
                    is_valid = False
                    chosen_race = input('Choose a race: ')
                    for index, race in enumerate(races):
                        if chosen_race == str(index + 1):
                            is_valid = True
                            race_at = race
                            break
                    if is_valid:
                        break
                    print('Invalid choice!')
                    print('---------------')
                # noinspection PyUnboundLocalVariable
                vip_clients = get_vip_clients(clients, race_at)
                average_spent = average_spent_by_vip_client(vip_clients)
                print('---------------------------------------------')
                print(f'Average spending of a VIP client:\n\t{average_spent}$')
                print('---------------------------------------------')
                make_graph_of_average_vip_spending(vip_clients, average_spent)
            case '2':
                print(table)
                make_graph_of_races_attendance(sorted_races)
            case '3':
                print('---------------------------------------------')
                print(f'Highest attendance:\n\t{highest_attendance}')
                highest_attendance.pretty_print_attendance()
                make_graph_of_races_attendance(sorted_races)
                print('---------------------------------------------')
            case '4':
                print('---------------------------------------------')
                print(f'Highest sold tickets:\n\t{most_tickets_sold}')
                highest_attendance.pretty_print_sold_tickets()
                sorted_races = sort_races_by_sold_tickets(sorted_races)
                make_graph_of_highest_sold_tickets_races(sorted_races)
                print('---------------------------------------------')
            case '5':
                choice = input("\t1.Top 3 products sold by a restaurant in all the races\n\t"
                               "2.Top 3 products sold by a restaurant in specific(with graphs)\n\t")
                match choice:
                    case '1':
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('---------------------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('\t---------------------------------------------')
                                top_items_sold = calculate_top_sold_items_of_restaurant(restaurant.items)
                                for index, item in enumerate(top_items_sold):
                                    print(f'\t\tTOP {index + 1}:\n\t\tProduct: {item.name}\n\t\ttotal sales: {item.total_sold}\n')
                                print('---------------------------------------------')
                    case '2':
                        for index, race in enumerate(races):
                            print(f'{index + 1}. RACE: {race.name}')
                        while True:
                            is_valid_race = False
                            race_chosen = input("\tChoose a race: ")
                            for index, race in enumerate(races):
                                if race_chosen == str(index + 1):
                                    is_valid_race = True
                                    race_chosen = race
                                    break
                            if is_valid_race:
                                break
                            print('Wrong race chosen, try again')
                            print('----------------------------')
                        for index, restaurant in enumerate(race_chosen.restaurants):
                            print(f'{index + 1}. RESTAURANT: {restaurant.name}')
                        while True:
                            is_valid_restaurant = False
                            chosen_restaurant = input("\tChoose a restaurant: ")
                            for index, restaurant in enumerate(race_chosen.restaurants):
                                if chosen_restaurant == str(index + 1):
                                    is_valid_restaurant = True
                                    chosen_restaurant = restaurant
                                    break
                            if is_valid_restaurant:
                                break
                            print('Wrong restaurant chosen, try again')
                            print('----------------------------------')
                        top_items_sold = calculate_top_sold_items_of_restaurant(chosen_restaurant.items)
                        for index, item in enumerate(top_items_sold):
                            print(f'\t\tTOP {index + 1}:\n\t\tProduct: {item.name}\n\t\ttotal sales: {item.total_sold}\n')
                        print('---------------------------------------------')
                        make_graph_of_top_sold_items_in_restaurant(top_items_sold)
                    case _:
                        print('Wrong input!')
                        print('------------')
            case '6':
                for index, client in enumerate(top_clients):
                    print(f'\tTOP {index + 1}:\n\tName: {client.name}\n\ttotal tickets: {len(client.tickets)}\n')
                    print('---------------------------------------------')
                make_graph_of_top_clients_with_most_tickets(top_clients)
            case '7':
                print('Goodbye!')
                print('----------')
                break
            case _:
                print('Wrong input!')
                print('------------')


# retorna la carrera con mayor asistencia, y también la carrera con mayor cantidad de tickets vendidos
def race_with_more_assistance_and_most_tickets_sold(races):
    highest_attendance_race = races[0]
    most_tickets_sold_race = races[0]
    for race in races:
        if race.attendance > highest_attendance_race.attendance:
            highest_attendance_race = race
        if race.sold_tickets > most_tickets_sold_race.sold_tickets:
            most_tickets_sold_race = race
    return highest_attendance_race, most_tickets_sold_race


# retorna la lista con los 3 clientes con mayor cantidad de tickets comprados
# si hay menos de 3 clientes retorna una lista con la cantidad de clientes
def calculate_top_clients(clients):
    sorted_clients = sorted(clients, key=lambda obj: len(obj.tickets), reverse=True)
    if len(sorted_clients) > 3:
        return sorted_clients[:3]
    else:
        return sorted_clients


# retorna el promedio de gasto de un cliente vip
def average_spent_by_vip_client(vip_clients):
    vip_clients_spent = 0
    if len(vip_clients) == 0:
        return 0
    for client in vip_clients:
        vip_clients_spent += client.total_spent
    return vip_clients_spent / len(vip_clients)


# retorna una lista únicamente con los clientes vip
def get_vip_clients(clients, race):
    vip_clients = []
    for client in clients:
        for ticket in client.tickets:
            if ticket.type == '1' and ticket.race_round == race.round:
                vip_clients.append(client)
                break
    return vip_clients


# retorna la lista con los 3 productos más comprados de un restaurant
# si hay menos de 3 productos retorna una lista con la cantidad de productos
def calculate_top_sold_items_of_restaurant(items):
    sorted_items = sorted(items, key=lambda obj: obj.total_sold, reverse=True)
    if len(sorted_items) > 3:
        return sorted_items[:3]
    else:
        return sorted_items


# Mostrar tabla con la asistencia a las carreras de mejor a peor y con una cantidad de información extra por carrera
def make_table(sorted_races):
    data = {
        'Race_name': [],
        'Circuit': [],
        'Attendance': [],
        'Tickets_sold': [],
        'Attendance/Tickets_sold ratio': []
    }
    for race in sorted_races:
        numerator = race.attendance
        denominator = race.sold_tickets
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
    return tabulate(data, headers='keys', tablefmt='fancy_grid', numalign='center', stralign='center')


# Ordena las carreras por asistencias.
def sort_races_by_attendance(races):
    sorted_races = sorted(races, key=lambda race: race.attendance, reverse=True)
    return sorted_races


# Ordena las carreras por tickets vendidos.
def sort_races_by_sold_tickets(races):
    sorted_races = sorted(races, key=lambda race: race.sold_tickets, reverse=True)
    return sorted_races


# Realiza un gráfico de barras con los gastos de un cliente vip
def make_graph_of_average_vip_spending(vip_clients, average_spent):
    vip_clients = sorted(vip_clients, key=lambda cl: cl.total_spent, reverse=True)
    positions = range(len(vip_clients))
    label = []
    for i in range(len(vip_clients)):
        label.append(f'Client {i + 1}')
    heights = []
    for client in vip_clients:
        heights.append(client.total_spent)
    plt.axhline(y=average_spent, color='red', linewidth=3, label='Avg')
    plt.bar(positions, heights, color=['red', 'black'], width=0.3, tick_label=label)
    plt.xlabel('Vip clients')
    plt.ylabel('Total spent')
    plt.title("Average vip client spending's")
    plt.show()


# Realiza un gráfico de barras con las asistencias de las carreras de mejor a peor
def make_graph_of_races_attendance(sorted_races):
    positions = range(len(sorted_races))
    label = []
    heights = []
    highest_value = 0
    for race in sorted_races:
        label.append(race.round)
        heights.append(race.sold_tickets)
        if race.sold_tickets > highest_value:
            highest_value = race.sold_tickets
    plt.axhline(y=highest_value, color='grey', linewidth=3, label='Avg')
    plt.bar(positions, heights, color=['blue', 'red'], tick_label=label)
    plt.xlabel('Races')
    plt.ylabel('Attendance')
    plt.title("All Races by attendance")
    plt.show()


# Realiza un gráfico de barras con la cantidad de tickets vendidos de las carreras
def make_graph_of_highest_sold_tickets_races(sorted_races):
    positions = range(len(sorted_races))
    label = []
    heights = []
    highest_value = 0
    for race in sorted_races:
        label.append(race.round)
        heights.append(race.attendance)
        if race.attendance > highest_value:
            highest_value = race.attendance
    plt.axhline(y=highest_value, color='grey', linewidth=3, label='Avg')
    plt.bar(positions, heights, color=['blue', 'red'], tick_label=label)
    plt.xlabel('Races')
    plt.ylabel('Sold tickets')
    plt.title("Races by sold tickets")
    plt.show()


# Realiza un gráfico de barras de los 3 clientes con mayor cantidad de tickets comprados
def make_graph_of_top_sold_items_in_restaurant(items):
    positions = range(len(items))
    label = []
    heights = []
    for index, item in enumerate(items):
        label.append(f'{index + 1}')
        heights.append(item.total_sold)
    plt.bar(positions, heights, color=['blue', 'red'], tick_label=label)
    plt.xlabel('Products')
    plt.ylabel('Sold amount')
    plt.title("Top 3 products sold in a restaurant")
    plt.show()


# Realiza un gráfico de barras de los 3 productos más vendidos de un restaurante
def make_graph_of_top_clients_with_most_tickets(top_clients):
    positions = range(len(top_clients))
    label = []
    heights = []
    for index, client in enumerate(top_clients):
        label.append(f'Client {index + 1}')
        heights.append(len(client.tickets))
    plt.bar(positions, heights, color=['blue', 'red'], tick_label=label)
    plt.xlabel('Clients')
    plt.ylabel('Tickets bought')
    plt.title("Clients by tickets bought")
    plt.show()
