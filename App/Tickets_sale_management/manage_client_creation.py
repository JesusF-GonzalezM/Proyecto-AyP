from App.Models.client import Client
from App.Tickets_sale_management.manage_ticket_creation import create_ticket, choose_race_and_ticket_type


def manage_client(races, clients):
    client_in_db = False
    print('Welcome!, Please enter your information to buy a ticket:\n')
    race_at, race_round, ticket_type = choose_race_and_ticket_type(races)

    while True:
        id = input('\tEnter your ID: ')
        if id.isnumeric():
            break
        print('ID is not valid, please try again.')

    for client in clients:
        if client.id == id:
            client_in_db = True
            print(f'Welcome back, {client.name.title()}')
            print('-------------------')
            ticket, seat = create_ticket(race_at, race_round, ticket_type, client.id)
            return seat, race_at, client, ticket, client_in_db

    while True:
        name = input('\tEnter your name: ')
        if name.isalpha():
            name = name.lower()
            break
        print('Name is not valid, please try again.')

    while True:
        age = input('\tEnter your age: ')
        if age.isnumeric():
            break
        print('Age is not valid, please try again.')

    client = Client(name=name, id=id, age=age)
    ticket, seat = create_ticket(race_at, race_round, ticket_type, client.id)
    return seat, race_at, client, ticket, client_in_db
