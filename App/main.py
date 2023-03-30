import uuid

from App.Races_and_team_management.races_and_team_management import races_and_team_management
from App.Races_assistance_module.manage_race_assistance import race_assistance_management
from App.Restaurant_management.restaurant_management_module import restaurant_management_module
from App.Restaurant_sale_management.restaurant_sale_management import restaurant_sales_management
from App.Statistics.statistics_calculation import statistics_module
from App.Tickets_sale_management.ticket_sale_management import tickets_sale_management
from App.parse_data.download_data import initialize_data, download_clients_from_file, upload_data_to_file


# Se encarga de subir la data a la base de datos
def save_data(clients, constructors, drivers, races):
    upload_data_to_file(drivers, 'drivers')
    upload_data_to_file(constructors, 'constructors')
    upload_data_to_file(races, 'races')
    upload_data_to_file(clients, 'clients')


# Se encarga de generar un codigo unico para cada asiento
def set_unique_code_to_seats(seats):
    for row in seats:
        for seat in row:
            seat.code = uuid.uuid4().hex


# si las matrices de los asientos no están inicializadas todavía, las inicializo y le agrego el codigo unico a cada asiento.
def initialize_seats_and_set_unique_code(clients, races):
    for race in races:
        if not race.general_seats:
            race.define_general_seats_matrix()
            set_unique_code_to_seats(race.general_seats)
        if not race.vip_seats:
            race.define_vip_seats_matrix()
            set_unique_code_to_seats(race.vip_seats)
    if clients:
        for client in clients:
            client.tickets.sort(key=lambda x: x.type)


# La función principal donde se ejecutan todas las demás funciones
def main():
    # inicializo la información, si no existen los archivos, la bajo de la api, sino, la bajo de los archivos
    drivers, constructors, races = initialize_data()
    clients = download_clients_from_file()
    # si las matrices de los asientos no están inicializadas todavía, las inicializo y le agrego el codigo unico a cada asiento.
    initialize_seats_and_set_unique_code(clients, races)

    # corro los modulos
    while True:
        print('Choose which module you want to use: ')
        module_to_choose = input('\t1.Races and team management\n\t2.Tickets sale management\n\t'
                                 '3.Races assistance management\n\t4.Restaurants management\n\t'
                                 '5.Restaurants sale management\n\t6.Statistics\n\t7.Exit\n\t'
                                 )
        match module_to_choose:
            case '1':
                # Races and team management Module
                print('Welcome to the Races and team management module!')
                print('------------------------------------------------')
                races_and_team_management(constructors, drivers, races)
            case '2':
                # Tickets sale management Module
                print('Welcome to the Tickets sale management module!')
                print('-----------------------------------------------')
                tickets_sale_management(clients, races)
            case '3':
                # Races assistance management Module
                print('Welcome to the ticket validation module!')
                print('----------------------------------------')
                race_assistance_management(clients, races)
            case '4':
                # Restaurants management Module
                print('Welcome to the restaurant management module!, here you can see our food and drinks by filters!')
                print('-----------------------------------------------------------------------------------------------')
                restaurant_management_module(races)

            case '5':
                # Restaurants sale management Module
                print('Welcome to the restaurant sale management module!')
                restaurant_sales_management(clients, races)
            case '6':
                print('Welcome to the statistics module!')
                print('---------------------------------')
                statistics_module(clients, races)
            case '7':
                print('Goodbye!')
                # Exit and Save
                save_data(clients, constructors, drivers, races)
                quit()
            case _:
                print('Wrong input!')
                print('------------')


# Ejecuta el programa principal
if __name__ == '__main__':
    main()
