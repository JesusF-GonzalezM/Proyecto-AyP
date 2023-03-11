from App.Models.location import Location


class Circuit:
    def __init__(self, circuitId, name, **kwargs):
        self.circuitId = circuitId
        self.name = name
        if 'location' in kwargs:
            self.location = Location(**kwargs.get('location'))
        else:
            self.location = Location(**kwargs.get('Location'))
