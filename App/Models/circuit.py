from App.Models.location import Location


# clase que se encarga de modelar la información del circuito en objetos de python.
class Circuit:
    def __init__(self, circuitId, name, **kwargs):
        self.circuitId = circuitId
        self.name = name
        if 'location' in kwargs:
            self.location = Location(**kwargs.get('location'))
        else:
            self.location = Location(**kwargs.get('Location'))
