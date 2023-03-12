class Refreshment:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Food(Refreshment):
    def __init__(self, name, price, type):
        super().__init__(name, price)
        self.type = type


class Drink(Refreshment):
    def __init__(self, name, price, type):
        super().__init__(name, price)
        self.type = type
