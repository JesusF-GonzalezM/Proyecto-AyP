from App.Restaurant_management.order_restaurant_products import get_products_by_price_range, get_products_by_type, \
    get_products_by_name, search_product_generally


# se encarga de permitir la búsqueda de items en los restaurantes mediante filtros
def restaurant_management_module(races):
    while True:
        choice = input('\t1. Search by filters\n\t2. Leave\n')
        match choice:
            case '1':
                chosen_filter = input(f'\t1. Search by name\n\t2. Search by type\n\t3. Search by price range\n\t')
                match chosen_filter:
                    case '1':
                        while True:
                            choice = input(f'\t1. Search by name generally\n\t2. Search by name in a specific restaurant\n\t')
                            match choice:
                                case '1':
                                    restaurant = search_product_generally(races)
                                    break
                                case '2':
                                    for race in races:
                                        print(f'{race.round}. {race.name}')
                                    while True:
                                        is_valid = False
                                        race_round = input('Which race restaurants do you want to see:\n')
                                        for race in races:
                                            if race_round == race.round:
                                                if race.restaurants:
                                                    race_at = race
                                                    is_valid = True
                                                    break
                                        if is_valid:
                                            break
                                        print(f'{race_round} is not a valid race choice or race does not have any restaurants!')
                                        print('-------------------------------------------------------------------------------')
                                    # noinspection PyUnboundLocalVariable
                                    for index, restaurant in enumerate(race_at.restaurants):
                                        print(f'{index + 1}. {restaurant.name}')
                                    while True:
                                        is_valid = False
                                        restaurant_choice = input('Which restaurant do you want to see:\n')
                                        for index, restaurant in enumerate(race_at.restaurants):
                                            if str(index + 1) == restaurant_choice:
                                                if restaurant.items:
                                                    is_valid = True
                                                    restaurant_at = restaurant
                                                    break
                                        if is_valid:
                                            break
                                        print(f'{restaurant_choice} is not a valid restaurant choice or restaurant is empty')
                                        print('----------------------------------------------------------------------------')
                                    # noinspection PyUnboundLocalVariable
                                    for index, item in enumerate(restaurant_at.items):
                                        print(f'{index + 1}. {item.name}')
                                    while True:
                                        is_valid = False
                                        product_index = input('Enter the product you want to search by: ')
                                        for index, item in enumerate(restaurant_at.items):
                                            if str(index + 1) == product_index:
                                                is_valid = True
                                                product_at = item
                                                break
                                        if is_valid:
                                            break
                                        print(f'{product_index} is not a valid product choice')
                                        print('----------------------------------------------')
                                    # noinspection PyUnboundLocalVariable
                                    found_products = get_products_by_name(restaurant_at.items, product_at.name)
                                    if found_products:
                                        for product in found_products:
                                            print(product)
                                    else:
                                        print(f'{product_index} is not a product in this restaurant')
                                        print('----------------------------------------------------')
                                    break
                                case _:
                                    print('Wrong input!')
                                    print('------------')
                    case '2':
                        chosen_type = input('\t1. drink:alcoholic\n\t2. drink:not-alcoholic\n\t'
                                            '3. food:restaurant\n\t4. food:fast\n')
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('--------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('\t--------------------------------')
                                match chosen_type:
                                    case '1':
                                        filtered_products = get_products_by_type(restaurant.items, 'drink:alcoholic')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print('\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case '2':
                                        filtered_products = get_products_by_type(restaurant.items, 'drink:not-alcoholic')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print(f'\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case '3':
                                        filtered_products = get_products_by_type(restaurant.items, 'food:restaurant')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print(f'\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case '4':
                                        filtered_products = get_products_by_type(restaurant.items, 'food:fast')
                                        if filtered_products:
                                            for product in filtered_products:
                                                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                                        else:
                                            print('\t\t--------------------------------------------------------')
                                            print(f'\t\tThere are no products with that type at this restaurant!')
                                            print('\t\t--------------------------------------------------------')
                                    case _:
                                        print('Wrong input!')
                                        print('------------')
                                        break
                    case '3':
                        while True:
                            min_price = input('Enter the minimum price you want to search by: ')
                            if min_price.isnumeric():
                                min_price = float(min_price)
                                if min_price >= 0:
                                    break
                            print('That is not a valid minimum price, must be a number and greater than 0')
                            print('----------------------------------------------------------------------')

                        while True:
                            max_price = input('Enter the maximum price you want to search by: ')
                            if max_price.isnumeric():
                                max_price = float(max_price)
                                if max_price > min_price:
                                    break
                            print('That is not a valid maximum price, must be a number and grater than the minimum price')
                            print('-------------------------------------------------------------------------------------')
                        for race in races:
                            print(f'RACE: {race.name}')
                            print('--------------------------------')
                            for restaurant in race.restaurants:
                                print(f'\tRESTAURANT: {restaurant.name}')
                                print('\t--------------------------------')
                            # noinspection PyUnboundLocalVariable
                            filtered_products = get_products_by_price_range(restaurant.items, min_price, max_price)
                            if filtered_products:
                                for product in filtered_products:
                                    print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                                          f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
                            else:
                                print('\t\t---------------------------------------------------------------')
                                print('\t\tThere are no products with that price range at this restaurant!')
                                print('\t\t---------------------------------------------------------------')

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
