from App.Models.client import Client
from App.Tickets_sale_management.manage_ticket_creation import create_ticket


def manage_client(races, clients):
    client_in_db = False
    print('Welcome!, Please enter your information to buy a ticket:\n')
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
            ticket = create_ticket(client.id, races, clients)
            return client, ticket, client_in_db

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
    ticket = create_ticket(client.id, races, clients)
    return client, ticket, client_in_db
