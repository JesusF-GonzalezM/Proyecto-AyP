# clase que se encarga de modelar la información del location en objetos de python.
class Location:
    def __init__(self, lat, long, locality, country):
        self.lat = lat  # latitude
        self.long = long  # longitude
        self.locality = locality
        self.country\
            = country
