

# Se encarga de manejar la asistencia de los clientes, y verificar que las entradas sean válidas
def race_assistance_management(clients, races):
    while True:
        choice = input('\t1. Enter the race\n\t2. Leave\n')
        match choice:
            case '1':
                if not clients:
                    print('There are no clients in the database!')
                    print('-------------------------------------')
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
                    print('-------------------------')
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
                        print('-----------------------')
                is_valid = False
                # noinspection PyUnboundLocalVariable
                for ticket in current_client.tickets:
                    # noinspection PyUnboundLocalVariable
                    if ticket.race_round == current_race_index:
                        if ticket.type.value == '1':
                            # noinspection PyUnboundLocalVariable
                            is_valid = check_if_ticket_code_is_valid(current_client, current_race, current_race.vip_seats, ticket)
                        if ticket.type.value == '2':
                            # noinspection PyUnboundLocalVariable
                            is_valid = check_if_ticket_code_is_valid(current_client, current_race, current_race.general_seats, ticket)
                    if is_valid:
                        break
                if not is_valid:
                    print('----------------------------------------')
                    print('You dont have any ticket for this race!')
                    print('----------------------------------------')
            case '2':
                print('Thank you for using the Races and team management module!')
                print('---------------------------------------------------------')
                break
            case _:
                print('Wrong input!')
                print('------------')


# revisa si el codigo del ticket es válido
def check_if_ticket_code_is_valid(current_client, current_race, seats, ticket):
    is_valid = False
    for row in seats:
        for seat in row:
            if seat.code == ticket.code:
                if not seat.assisted:
                    seat.assisted = True
                    current_race.attendance += 1
                print('----------------------------')
                print(f'Welcome to the race {current_client.name.title()}, enjoy!')
                print('----------------------------')
                print(f'Your seat is the {seat.position} | row {seat.position[0]} | column {seat.position[1]} |')
                print('----------------------------')
                is_valid = True
                break
    return is_valid
