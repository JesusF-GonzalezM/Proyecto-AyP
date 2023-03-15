from App.Models.ticket import Ticket


def choose_race_and_ticket_type(races):
    valid_races = []
    for race in races:
        vip_full = check_if_seats_available(race.vip_seats)
        general_full = check_if_seats_available(race.general_seats)
        if not (vip_full and general_full):
            valid_races.append(str(race.round))
            print(race)

    while True:
        race_round = input('Enter the round of the race you want to buy a ticket for: ')
        if race_round in valid_races:
            for race in races:
                if race_round == str(race.round):
                    race_at = race
                    vip_full = check_if_seats_available(race_at.vip_seats)
                    general_full = check_if_seats_available(race_at.general_seats)
                    break
            break
        print('Race does not exist or is out of tickets, please try again.')

    while True:
        full = False
        print('\tEnter your desired ticket type:')
        print('\t1. VIP')
        ticket_type = input('\t2. GENERAL\n\t')
        if ticket_type == '1' or ticket_type == '2':
            if ticket_type == '1' and vip_full:
                full = True
                print('We are out of VIP seats, please try again.')
            elif ticket_type == '2' and general_full:
                full = True
                print('We are out of GENERAL seats, please try again.')
            else:
                break
        if not full:
            print('Ticket type is not valid, please try again.')
    return race_at, race_round, ticket_type


def validate_seat(seats):
    valid = False
    taken = False
    print('Expected Input: Number in the seat')
    while True:
        chosen_seat = input('Enter the seat you want to buy a ticket for: ')
        for row in seats:
            for seat in row:
                if chosen_seat == seat.position:
                    if not seat.taken:
                        current_seat = seat
                        valid = True
                        break
                    taken = True
                    print('Seat already taken')
        if valid:
            break
        if not taken:
            print('Seat does not exist, please try again.')
    return current_seat


def choose_seat(race, ticket_type):
    while True:
        if ticket_type == '1':
            race.print_vip_seats()
            current_seat = validate_seat(race.vip_seats)
        else:
            race.print_general_seats()
            current_seat = validate_seat(race.general_seats)
        return current_seat


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


def create_ticket(race_at, race_round, ticket_type, client_id):

    seat = choose_seat(race_at, ticket_type)
    ticket = Ticket(race_round=race_round, type=ticket_type, code=seat.code)

    if number_is_ondulado(client_id):
        ticket.discount = True
    ticket.calculate_price()
    ticket.print_detailed_price()
    return ticket, seat


def check_if_seats_available(seats):
    taken = True
    for row in seats:
        for seat in row:
            if not seat.taken:
                taken = False
                break
    return taken