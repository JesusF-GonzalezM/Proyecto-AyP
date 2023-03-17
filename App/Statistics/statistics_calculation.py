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


# Imprime una tabla con las carreras ordenadas de mayor a menor por asistencia, y con una cantidad de información extra por carrera
def print_table_of_races_assistance(races):
    pass


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


