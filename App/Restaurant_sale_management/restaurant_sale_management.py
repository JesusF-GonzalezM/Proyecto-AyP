from App.Restaurant_sale_management.manage_purchases import manage_purchase


# Se encarga de las compras en los restaurantes, y agregarle el costo a una variable en el cliente.
def restaurant_sales_management(clients, races):
    if clients:
        while True:
            choice = input('\t1. Buy products\n\t2. Leave\n')
            match choice:
                case '1':
                    client, total_price, restaurant_at, products = manage_purchase(clients, races)
                    if not client:
                        break
                    if client != 'no restaurants':
                        choice = input(f'1.Pay the products\n2.Cancel Payment\n')
                        match choice:
                            case '1':
                                print('Success! Thank you for your purchase!')
                                print('-------------------------------------')
                                client.total_spent += total_price
                                for item in restaurant_at.items:
                                    for product in products:
                                        if product == item:
                                            item.total_sold += 1
                            case '2':
                                for product in products:
                                    product.stock += 1
                                print('Goodbye!')
                                print('--------')
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
    else:
        print('--------------------------------------')
        print('There are no clients in the database!!')
        print('--------------------------------------')
