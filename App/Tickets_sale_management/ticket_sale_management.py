from App.Tickets_sale_management.manage_client_creation import manage_client
from App.Tickets_sale_management.manage_ticket_creation import calculate_total_ticket_price_and_print


# Se encarga de la venta de tickets delegando responsabilidades en otras funciones
def tickets_sale_management(clients, races):
    while True:
        choice = input(f'1.Buy ticket(s)\n2.Leave\n')
        match choice:
            case '1':

                seats, race_at, client, tickets, client_in_db = manage_client(races, clients)
                total_price = calculate_total_ticket_price_and_print(tickets)
                while True:
                    payment = input('\tDo you want to pay this ticket(s)? (y/n):\n\t')
                    match payment:
                        case 'y':
                            for ticket in tickets:
                                client.add_ticket(ticket)
                            race_at.sold_tickets += len(tickets)
                            client.total_spent += total_price
                            for seat in seats:
                                seat.taken = True
                            if not client_in_db:
                                clients.append(client)
                            print('-------------------------------------')
                            print('Success! Thank you for your purchase!')
                            print('-------------------------------------')
                            break
                        case 'n':
                            for seat in seats:
                                seat.taken = False
                            print('Goodbye!')
                            print('--------')
                            break
                        case _:
                            print('Wrong input!')
                            print('------------')
            case '2':
                print('Goodbye!')
                print('--------')
                break
            case _:
                print('Wrong input!')
                print('------------')
