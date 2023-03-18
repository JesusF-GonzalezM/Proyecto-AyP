# Maneja la compra de un item por un usuario
from App.Models.refreshment import Drink


# Maneja la validación de que la carrera no tenga restaurantes, o que si los tenga, pero ellos no contengan productos.
# También maneja la validación de que el usuario tenga un ticket VIP para esta carrera.
def manage_purchase(clients, races):
    can_buy = False
    valid_id = False
    ticket_vip = False
    non_alcoholic_items = False
    while True:
        id = input("Enter your ID: ")
        for client in clients:
            if client.id == id:
                current_client = client
                valid_id = True
                break
        if valid_id:
            break
        print('Entered ID is not in this race, try again')
    while True:
        for race in races:
            print(race)
        # validación de que la carrera sea un número válido en cuanto a los índices de las carreras
        race_round = input("Enter the round of the race you are at: ")
        if 1 <= int(race_round) <= 23:
            for race in races:
                if race_round == race.round:
                    race_at = race
                    break
            break
        print('Entered round is not valid, try again')
    # noinspection PyUnboundLocalVariable
    for ticket in current_client.tickets:
        # noinspection PyUnboundLocalVariable
        if ticket.race_round == race_at.round and ticket.type == '1':
            ticket_vip = True
    if ticket_vip:
        if len(race_at.restaurants) == 0:
            print('There are no restaurants in this race\n')
            return 'no restaurants', 'no restaurants', 'no restaurants', 'no restaurants'
        if int(current_client.age) < 18:
            for restaurant in race_at.restaurants:
                for item in restaurant.items:
                    if item.type != 'drink:alcoholic':
                        non_alcoholic_items = True
                        break
            if not non_alcoholic_items:
                print('There are not non alcoholic items in this restaurant\n')
                return 'no restaurants', 'no restaurants', 'no restaurants', 'no restaurants'
        for restaurant in race_at.restaurants:
            if len(restaurant.items) > 0:
                can_buy = True
        if not can_buy:
            print('There are no items in this race restaurants\n')
            return 'no restaurants', 'no restaurants', 'no restaurants', 'no restaurants'

        # noinspection PyUnboundLocalVariable
        for index, restaurant in enumerate(race_at.restaurants):
            print(f'{index + 1}. {restaurant.name}')
        # noinspection PyUnboundLocalVariable
        total_price, restaurant_at, products = purchase_products(current_client, race_at.restaurants)
    else:
        print('-----------------------------------------')
        print('You dont have a VIP ticket in this race\n')
        print('-----------------------------------------')
        return None, None, None, None
    return current_client, total_price, restaurant_at, products


# Maneja la compra de productos por un usuario y la mayoria de las validaciones
def purchase_products(client, restaurants):
    products_to_buy = []
    valid_restaurant = False
    while True:
        for index, restaurant in enumerate(restaurants):
            print(f'{index+1}. {restaurant.name}')
        while True:
            chosen_restaurant = input('Choose the restaurant you want the products of: ')
            if chosen_restaurant.isnumeric():
                if 0 < int(chosen_restaurant) <= len(restaurants):
                    break
            print('Chosen restaurant is not valid, try again')
        for index, restaurant in enumerate(restaurants):
            if index == (int(chosen_restaurant) - 1):
                if len(restaurant.items) > 0:
                    valid_restaurant = True
                    restaurant_at = restaurant
                    break
                print('This restaurant does not have any inventory currently\n')
        if valid_restaurant:
            break
    # noinspection PyUnboundLocalVariable
    for index, product in enumerate(restaurant_at.items):
        print(f'\t{index+1}. {product.name}\n\t\ttype: {product.type}\n\t\tprice: {product.price}\n\t\tstock: {product.stock}\n')
    while True:
        while True:
            chosen_product = input("Choose the product you want to buy: ")
            if chosen_product.isnumeric():
                if 0 < int(chosen_product) <= len(restaurant_at.items):
                    break
            print('Chosen product is not valid, try again')
        chosen_product = restaurant_at.items[int(chosen_product) - 1]
        if isinstance(chosen_product, Drink):
            alcoholic = chosen_product.type.split(':')[1]
            print(f'Alcoholic: {alcoholic}')
            if alcoholic == 'alcoholic' and int(client.age) < 18:
                print('Sorry, you are too young to buy this alcoholic product')
                continue
            print(chosen_product.type)
        total_price = 0
        if chosen_product.stock > 0:
            chosen_product.stock -= 1
            products_to_buy.append(chosen_product)
            total_price = calculate_total_products_price_and_print(products_to_buy, client.id)
        else:
            print('We do not have more of that product in our inventory!')
        choice = input('Do you want to buy another product?\n\t1. Yes\n\t2. No\n')
        match choice:
            case '1':
                continue
            case '2':
                break
            case _:
                print('Wrong Input!')
                print('------------')
    # noinspection PyUnboundLocalVariable
    return total_price, restaurant_at, products_to_buy


# calcula el precio total de los productos
def calculate_total_products_price_and_print(products, client_id):
    base_price = 0
    discount = 0
    for product in products:
        base_price += product.price
    if perfect_number(client_id):
        discount = base_price * 0.5
    total_price = base_price - discount
    iva = total_price * 0.16
    total_price = total_price + iva
    print_receipt(base_price, total_price, iva, discount)
    return total_price


# se encarga de imprimir una factura de manera amigable
def print_receipt(base_price, total_price, iva, discount):
    print('------------Ticket(s) receipt------------')
    print(f'Base price: {base_price}$')
    print(f'Discount: {discount}$')
    print(f'IVA: {iva}$')
    print(f'TOTAL PRICE: {total_price}$')
    print(f'--------------------------------------')


# se encarga de validar si un número es perfecto
def perfect_number(n):
    n = int(n)
    n_divisors = 0
    for i in range(1, n + 1):
        if n % i == 0:
            n_divisors += i
    if n_divisors == (2 * n):
        return True
    return False
