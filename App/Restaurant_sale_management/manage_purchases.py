def perfect_number(n):
    n = int(n)
    n_divisors = 0
    for i in range(1, n + 1):
        if n % i == 0:
            n_divisors += i
    if n_divisors == (2 * n):
        return True
    return False


def manage_purchase(clients, races):
    can_buy = False
    valid_id = False
    restaurants = {}
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
        race_round = input("Enter the round of the race you are at: ")
        if 1 <= int(race_round) <= 23:
            for race in races:
                if race_round == race.round:
                    race_at = race
                    break
            break
        print('Entered round is not valid, try again')
    # noinspection PyUnboundLocalVariable
    if len(race_at.restaurants) == 0:
        print('There are no restaurants in this race')
        return 'no restaurants', 'no restaurants'
    for restaurant in race_at.restaurants:
        if len(restaurant.items) > 0:
            can_buy = True
    if not can_buy:
        print('There are no items in this race restaurants')
        return 'no restaurants', 'no restaurants'

    # noinspection PyUnboundLocalVariable
    for index, restaurant in enumerate(race_at.restaurants):
        restaurants.update({index+1: restaurant})
    # noinspection PyUnboundLocalVariable
    total_price = purchase_products(current_client, restaurants)
    return current_client, total_price


def purchase_products(client, restaurants):
    no_items = False
    products_to_buy = []
    products = {}
    valid_restaurant = False
    while True:
        for number, restaurant in restaurants.items():
            print(f'{number}. {restaurant.name}')
        chosen_restaurant = int(input('Choose the restaurant you want the products of: '))
        for key in restaurants.keys():
            if key == int(chosen_restaurant):
                if len(restaurants[chosen_restaurant].items) > 0:
                    valid_restaurant = True
                    break
                print('This restaurant does not have any inventory currently')
                no_items = True
        if valid_restaurant:
            break
        if not no_items:
            print('Restaurant is not valid, try again')

    for index, product in enumerate(restaurants[chosen_restaurant].items):
        products.update({index+1: product})
        print(f'{index+1}. {product.name}\n\ttype: {product.type}\n\tprice: {product.price}')
    while True:
        chosen_product = input("Enter the product you want to buy: ")
        if chosen_product in products.keys():
            chosen_product = int(chosen_product)
            alcoholic = products[chosen_product].type.split(':')[1]
            print(f'Alcoholic: {alcoholic}')
            if alcoholic == 'alcoholic' and int(client.age) < 18:
                print('Sorry, you are too young to buy this alcoholic product')
                continue
            print(products[chosen_product].type)
            products_to_buy.append(products[chosen_product])
            print('Successfully added the item to the cart\n ---------')
            choice = input('Do you want to buy another product? (y/n): ')
            if choice == 'y':
                continue
            break
    total_price = calculate_total_price(client, products_to_buy)
    print_checkout(products_to_buy, total_price)
    return total_price


def calculate_total_price(client, products):
    total_price = 0
    for product in products:
        total_price += (float(product.price) * 1.16)
    if perfect_number(client.id):
        total_price *= 0.85
    return total_price


def print_checkout(products, total_price):
    for product in products:
        print(f"{product.name} - {product.price:.2f}")
    print(f"Total: {total_price:.2f}")
