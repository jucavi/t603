from datetime import datetime, timedelta

class Flight:
    def __init__(self, origin, destiny, departure, flight_time):
        self.destiny = destiny
        self.origin = origin
        self.departure = departure
        self.flight_time = flight_time

    @property
    def ETA(self):
        return self.departure + self.flight_time + (self.destiny.utc - self.origin.utc)

    @property
    def arrival(self):
        return f''



class Airport:
    def __init__(self, country, city, name, utc, fligts):
        self.city = city
        self.country = country
        self.name = name
        self.utc = timedelta(hours=utc)
        self.flights = fligts

    # def str2dtime(self, time):
    #     return datetime.strptime(time, '%H:%M')

    # def f2delta(self, hours):
    #     return timedelta(hours=float(hours))

    def airport_dict(self):
        return {
            'city': self.city,
            'country': self.country
        }


