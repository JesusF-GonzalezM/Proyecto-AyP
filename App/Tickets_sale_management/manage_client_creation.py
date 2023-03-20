from App.Models.client import Client
from App.Tickets_sale_management.manage_ticket_creation import create_ticket, choose_race_and_ticket_type


# se encarga de la creación de un cliente y su ticket, delegando a otras funciones.
def manage_client(races, clients):
    client_in_db = False
    print('Welcome!, Please enter your information to buy a ticket:\n')
    race_at, race_round, ticket_type = choose_race_and_ticket_type(races)

    while True:
        id = input('\tEnter your ID: ')
        if id.isnumeric():
            break
        print('ID is not valid, please try again.')
        print('----------------------------------')
    # verificamos si el cliente ya existe en la base de datos
    for client in clients:
        if client.id == id:
            client_in_db = True
            print(f'Welcome back, {client.name.title()}')
            print('--------------------------')
            # creación de un ticket
            tickets, seats = create_ticket(race_at, race_round, ticket_type, client.id)
            return seats, race_at, client, tickets, client_in_db

    while True:
        name = input('\tEnter your name: ')
        if name.isalpha():
            name = name.lower()
            break
        print('Name is not valid, please try again.')
        print('------------------------------------')

    while True:
        age = input('\tEnter your age: ')
        if age.isnumeric():
            break
        print('Age is not valid, please try again.')
        print('-----------------------------------')

    client = Client(name=name, id=id, age=age)
    # creación de un ticket
    tickets, seats = create_ticket(race_at, race_round, ticket_type, client.id)
    return seats, race_at, client, tickets, client_in_db
