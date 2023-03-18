# retorna el producto con el nombre indicado.
def get_products_by_name(products, product_name):
    filtered_products = []
    for product in products:
        if product.name == product_name:
            filtered_products.append(product)
    return filtered_products


# retorna todos los productos con el tipo indicado.
def get_products_by_type(products, product_type):
    filtered_products = []
    for product in products:
        if product.type == product_type:
            filtered_products.append(product)
    return filtered_products


# retorna todos los productos con el rango de precio indicado.
def get_products_by_price_range(products, min_price, max_price):
    filtered_products = []
    for product in products:
        if min_price <= product.price <= max_price:
            filtered_products.append(product)
    filtered_products = sorted(filtered_products, key=lambda item: item.price)
    return filtered_products


def search_product_generally(races):
    product_name = input('Enter the name of the product you want to search: ')
    for race in races:
        for restaurant in race.restaurants:
            filtered_products = get_products_by_name(restaurant.items, product_name)
            if filtered_products:
                print(f'RACE: {race.name}')
                print('--------------------------------')
                print(f'\tRESTAURANT: {restaurant.name}')
                print('\t--------------------------------')
            else:
                print('\t\t--------------------------------------------------------')
                print('\t\tThere are no products with that type at this restaurant!')
                print('\t\t--------------------------------------------------------')

            for product in filtered_products:
                print(f'\t\tname: {product.name}\n\t\ttype: {product.type}'
                      f'\n\t\tprice: {product.price}\n\t\t--------------------------------')
    # noinspection PyUnboundLocalVariable
    return restaurant
