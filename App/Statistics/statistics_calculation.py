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
                       "7.Leave\n\t")
        match choice:
            case '1':
                average_in_races = {}
                for race in races:
                    vip_clients = get_vip_clients(clients, race)
                    average_spent_per_race = average_spent_by_vip_client(vip_clients)
                    print('----------------------------------------------------------')
                    print(f'Race: {race.name}\naverage spent by VIP clients: {average_spent_per_race}$')
                    print('----------------------------------------------------------')
                    average_in_races.update({race.round: average_spent_per_race})
                average_spent = sum(average_in_races.values())/23
                print('---------------------------------------------')
                print(f'Average spending of a VIP client in all races:\n\t{average_spent}$')
                print('---------------------------------------------')
                see_graph = input('Do you want to to see the graph? (y/n)\n\t')
                if see_graph == 'y':
                    make_graph_of_average_vip_spending(average_in_races)
            case '2':
                print(table)
                print('-------------------------------------')
                see_graph = input('Do you want to to see the graph? (y/n)\n\t')
                if see_graph == 'y':
                    make_graph_of_races_attendance(sorted_races)
            case '3':
                if highest_attendance:
                    print('---------------------------------------------')
                    print(f'Highest attendance:\n\t{highest_attendance}')
                    print('---------------------------------------------')
                    highest_attendance.pretty_print_attendance()
                    see_graph = input('Do you want to to see the graph? (y/n)\n\t')
                    if see_graph == 'y':
                        make_graph_of_races_attendance(sorted_races)
                else:
                    print('---------------------------------')
                    print('No one have attended to any race.')
                    print('---------------------------------')
            case '4':
                if most_tickets_sold:
                    print('---------------------------------------------')
                    print(f'Highest sold tickets:\n\t{most_tickets_sold}')
                    highest_attendance.pretty_print_sold_tickets()
                    sorted_races = sort_races_by_sold_tickets(sorted_races)
                    print('---------------------------------------------')
                    see_graph = input('Do you want to to see the graph? (y/n)\n\t')
                    if see_graph == 'y':
                        make_graph_of_highest_sold_tickets_races(sorted_races)
                else:
                    print('--------------------------')
                    print('No tickets have been sold.')
                    print('--------------------------')
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
                                if not top_items_sold:
                                    print('No items have been sold at this restaurant!')
                                    print('-------------------------------------------')
                                else:
                                    for index, item in enumerate(top_items_sold):
                                        if item.total_sold != 0:
                                            print(f'\t\tTOP {index + 1}:\n\t\tProduct: {item.name}\n\t\ttotal sales: {item.total_sold}\n')
                                            print('---------------------------------------------')
                    case '2':
                        no_restaurants = False
                        for index, race in enumerate(races):
                            if race.restaurants:
                                print(f'{index + 1}. RACE: {race.name}')
                        while True:
                            is_valid_race = False
                            race_chosen = input("\tChoose a race: ")
                            for index, race in enumerate(races):
                                if race_chosen == str(index + 1):
                                    race_chosen = race
                                    if race_chosen.restaurants:
                                        is_valid_race = True
                                        break
                                    else:
                                        no_restaurants = True
                            if is_valid_race:
                                break
                            if not no_restaurants:
                                print('Wrong race chosen, try again')
                                print('----------------------------')
                            else:
                                print('Race have no restaurants!')
                                print('-------------------------')
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
                        if not top_items_sold:
                            print('There are no items sold at this restaurant!')
                            print('-------------------------------------------')
                        else:
                            for index, item in enumerate(top_items_sold):
                                print(f'\t\tTOP {index + 1}:\n\t\tProduct: {item.name}\n\t\ttotal sales: {item.total_sold}\n')
                            print('---------------------------------------------')
                            see_graph = input('Do you want to to see the graph? (y/n)\n\t')
                            if see_graph == 'y':
                                make_graph_of_top_sold_items_in_restaurant(top_items_sold)
                    case _:
                        print('Wrong input!')
                        print('------------')
            case '6':
                if not top_clients:
                    print('There are no clients with tickets')
                    print('---------------------------------')
                else:
                    for index, client in enumerate(top_clients):
                        print(f'\tTOP {index + 1}:\n\tName: {client.name}\n\ttotal tickets: {len(client.tickets)}\n')
                        print('---------------------------------------------')
                    see_graph = input('Do you want to to see the graph? (y/n)\n\t')
                    if see_graph == 'y':
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
    if clients:
        if len(sorted_clients[0].tickets) == 0:
            return False
        if len(sorted_clients[2].tickets) > 0:
            return sorted_clients[:3]
        elif len(sorted_clients[1].tickets) > 0:
            return sorted_clients[:2]
        elif len(sorted_clients[0].tickets) > 0:
            return sorted_clients[: 1]
    else:
        return False


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
    if sorted_items:
        if sorted_items[0].total_sold == 0:
            return False
        if sorted_items[2].total_sold > 0:
            return sorted_items[:3]
        elif sorted_items[1].total_sold > 0:
            return sorted_items[:2]
        elif sorted_items[0].total_sold > 0:
            return sorted_items[: 1]
    else:
        return False


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
        its_zero = False
        numerator = race.attendance
        denominator = race.sold_tickets
        if race.sold_tickets and race.attendance:
            common_divisor = gcd(race.attendance, race.sold_tickets)
            numerator = race.attendance // common_divisor
            denominator = race.sold_tickets // common_divisor
        else:
            its_zero = True
        data['Race_name'].append(race.name)
        data['Circuit'].append(race.circuit.name)
        data['Attendance'].append(race.attendance)
        data['Tickets_sold'].append(race.sold_tickets)
        # noinspection PyUnboundLocalVariable
        if its_zero:
            data['Attendance/Tickets_sold ratio'].append(f'0')
        else:
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
def make_graph_of_average_vip_spending(average_spent_in_races):
    sum_of_averages = 0
    positions = average_spent_in_races.keys()
    label = []
    for i in average_spent_in_races:
        label.append(i)
    heights = []
    for average_in_race in average_spent_in_races.values():
        sum_of_averages += average_in_race
        heights.append(average_in_race)
    plt.axhline(y=sum_of_averages/23, color='gold', linewidth=3, label='Avg')
    plt.bar(positions, heights, color=['blue'], tick_label=label)
    plt.xlabel('Races')
    plt.ylabel('Avg spent in race')
    plt.title("Average vip client spending's")
    plt.legend(['Average Spent in all races', 'Avg spent per Race'], bbox_to_anchor=(1.1, 1.15), loc='upper right', borderaxespad=0)
    plt.show()


# Realiza un gráfico de barras con las asistencias de las carreras de mejor a peor
def make_graph_of_races_attendance(sorted_races):
    races_sorted_by_attendance = sorted(sorted_races, key=lambda x: x.attendance, reverse=True)
    positions = range(len(races_sorted_by_attendance))
    label = []
    heights = []
    highest_value = 0
    for race in races_sorted_by_attendance:
        label.append(race.round)
        heights.append(race.attendance)
        if race.attendance > highest_value:
            highest_value = race.attendance
    plt.axhline(y=highest_value, color='gold', linewidth=3, label='Avg')
    plt.bar(positions, heights, color=['blue'], tick_label=label)
    plt.xlabel('Races')
    plt.ylabel('Attendance')
    plt.title("All Races by attendance")
    plt.legend(['Highest Attendance', 'Attendances'], bbox_to_anchor=(1.1, 1.15), loc='upper right', borderaxespad=0)
    plt.show()


# Realiza un gráfico de barras con la cantidad de tickets vendidos de las carreras
def make_graph_of_highest_sold_tickets_races(sorted_races):
    positions = range(len(sorted_races))
    label = []
    heights = []
    highest_value = 0
    for race in sorted_races:
        label.append(race.round)
        heights.append(race.sold_tickets)
        if race.sold_tickets > highest_value:
            highest_value = race.sold_tickets
    plt.axhline(y=highest_value, color='gold', linewidth=3, label='Avg')
    plt.bar(positions, heights, color=['blue'], tick_label=label)
    plt.xlabel('Races')
    plt.ylabel('Sold tickets')
    plt.title("Races by sold tickets")
    plt.legend(['Highest sold ticket race', 'Race sold tickets'], bbox_to_anchor=(1.12, 1.15), loc='upper right', borderaxespad=0)
    plt.show()


# Realiza un gráfico de barras de los 3 clientes con mayor cantidad de tickets comprados
def make_graph_of_top_sold_items_in_restaurant(items):
    positions = range(len(items))
    label = []
    heights = []
    for index, item in enumerate(items):
        label.append(f'{index + 1}')
        heights.append(item.total_sold)
    plt.bar(positions, heights, color=['blue'], tick_label=label)
    plt.xlabel('Products')
    plt.ylabel('Sold amount')
    plt.title("Top 3 products sold in a restaurant")
    plt.legend(['sold amount'], bbox_to_anchor=(1.1, 1.15), loc='upper right', borderaxespad=0)
    plt.show()


# Realiza un gráfico de barras de los 3 productos más vendidos de un restaurante
def make_graph_of_top_clients_with_most_tickets(top_clients):
    positions = range(len(top_clients))
    label = []
    heights = []
    for index, client in enumerate(top_clients):
        label.append(f'Client {index + 1}')
        heights.append(len(client.tickets))
    plt.bar(positions, heights, color=['blue'], tick_label=label)
    plt.xlabel('Clients')
    plt.ylabel('Tickets bought')
    plt.title("Clients by tickets bought")
    plt.legend(['Tickets bought'], bbox_to_anchor=(1.1, 1.15), loc='upper right', borderaxespad=0)
    plt.show()
