# clase que se encarga de modelar la información del producto en objetos de python.
class Refreshment:
    def __init__(self, name, price, total_sold, stock):
        self.name = name
        self.price = float(price)
        self.total_sold = total_sold
        self.stock = stock

    def __str__(self):
        return f'name: {self.name}\n\tprice: {self.price}'


class Food(Refreshment):
    def __init__(self, name, price, type, total_sold=0, stock=10):
        super().__init__(name, price, total_sold, stock)
        self.type = type

    def __str__(self):
        return super().__str__() + f'\n\ttype: {self.type}'


class Drink(Refreshment):
    def __init__(self, name, price, type, total_sold=0, stock=10):
        super().__init__(name, price, total_sold, stock)
        self.type = type

    def __str__(self):
        return super().__str__() + f'\n\ttype: {self.type}'
