class Refreshment:
    def __init__(self, name, price):
        self.name = name
        self.price = float(price) * 1.16


class Food(Refreshment):
    def __init__(self, name, price, type):
        super().__init__(name, price)
        self.type = type


class Drink(Refreshment):
    def __init__(self, name, price, type):
        super().__init__(name, price)
        self.type = type
