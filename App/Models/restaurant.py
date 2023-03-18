from App.Models.refreshment import Drink, Food


# clase que se encarga de modelar la información del restaurant en objetos de python.
class Restaurant:
    def __init__(self, name, items):
        self.name = name
        # drinks and food
        self.items = []
        for item in items:
            if item['type'].startswith('d'):
                self.items.append(Drink(**item))
            else:
                self.items.append(Food(**item))
