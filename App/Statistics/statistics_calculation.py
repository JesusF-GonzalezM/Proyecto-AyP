from math import gcd
from tabulate import tabulate


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
                print('---------------------------------------------')
                print(f'Average spending of a VIP client:\n\t{average_spent}$')
                print('---------------------------------------------')
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
                        print('\t---------------------------------------------')
                        top_items_sold = calculate_top_sold_items_of_restaurant(restaurant.items)
                        for index, item in enumerate(top_items_sold):
                            print(f'\t\tTOP {index + 1}:\n\t\tProduct: {item.name}\n\t\ttotal sales: {item.total_sold}\n')
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
def average_spent_by_vip_client(clients):
    total_spent = 0
    total_vip_clients = 0
    for client in clients:
        for ticket in client.tickets:
            if ticket.type == '1':
                total_vip_clients += 1
                total_spent += client.total_spent
                break
    if total_vip_clients > 0:
        return total_spent / total_vip_clients
    else:
        return 0


# retorna la lista con los 3 productos más comprados de un restaurant
# si hay menos de 3 productos retorna una lista con la cantidad de productos
def calculate_top_sold_items_of_restaurant(items):
    sorted_items = sorted(items, key=lambda obj: obj.total_sold, reverse=True)
    if len(sorted_items) > 3:
        return sorted_items[:3]
    else:
        return sorted_items


# Mostrar tabla con la asistencia a las carreras de mejor a peor y con una cantidad de información extra por carrera
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

    print(tabulate(data, headers='keys', tablefmt='fancy_grid', showindex='always', numalign='center', stralign='center'))


# Ordena las carreras por asistencias.
def sort_races_by_attendance(races):
    sorted_races = sorted(races, key=lambda race: race.attendance, reverse=True)
    return sorted_races
