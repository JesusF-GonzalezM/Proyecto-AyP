class Refreshment:
    def __init__(self, name, price, total_sold):
        self.name = name
        self.price = float(price)
        self.total_sold = total_sold


class Food(Refreshment):
    def __init__(self, name, price, type, total_sold=0):
        super().__init__(name, price, total_sold)
        self.type = type


class Drink(Refreshment):
    def __init__(self, name, price, type, total_sold=0):
        super().__init__(name, price, total_sold)
        self.type = type
