import random
from App.Models.ticket import Ticket


def number_is_ondulado(num):  # this shit does not work
    num = str(num)
    if int(num) < 100:
        return True
    a = num[0]
    b = num[1]
    for index in range(2, len(num), 2):
        if len(num) == index or len(num) == index + 1:
            break
        if num[index] != a or num[index + 1] != b:
            return False
    return True


def generate_unique_ticket_code(clients):
    while True:
        unique_code = random.randint(100000, 999999)
        unique = True
        for client in clients:
            for ticket in client.tickets:
                if unique_code == ticket.code:
                    unique = False
                    break
        if unique:
            break
    return unique_code


def create_ticket(client_id, races, clients):
    for race in races:
        print(race)
    valid = False
    while True:
        race_round = input('Enter the round of the race you want to buy a ticket for: ')
        for race in races:
            if race.round == race_round:
                valid = True
                race.sold_tickets += 1
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

    ticket = Ticket(race_round=race_round, type=ticket_type)
    ticket.code = set_unique_code_to_ticket(clients)
    if number_is_ondulado(client_id):
        ticket.discount = True
    ticket.calculate_price()
    ticket.print_detailed_price()
    return ticket


def set_unique_code_to_ticket(clients):
    if clients:
        unique_ticket_code = generate_unique_ticket_code(clients)
    else:
        unique_ticket_code = random.randint(100000, 999999)
    return unique_ticket_code
