# retorna el producto con el nombre indicado.
def get_product_by_name(products, product_name):
    for product in products:
        if product.name == product_name:
            return product


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
