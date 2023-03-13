# Buscar productos por nombre, tipo, o rango de precio.


def get_product_by_name(products, product_name):
    for product in products:
        if product.name == product_name:
            return product


def get_products_by_type(products, product_type):
    filtered_products = []
    for product in products:
        if product.type == product_type:
            filtered_products.append(product)
    return filtered_products


def get_products_by_price_range(products, min_price, max_price):
    filtered_products = []
    for product in products:
        if min_price <= product.price <= max_price:
            filtered_products.append(product)
    filtered_products = sorted(filtered_products, key=lambda item: item.price)
    return filtered_products
