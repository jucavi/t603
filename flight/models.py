class Flight:
    def __init__(self, origin, destination, departure_time, flight_time):
        self.destination = destination
        self.origin = origin
        self.departure_time = departure_time
        self.flight_time = flight_time

    @property
    def ETA(self):
        return self.departure_time + self.flight_time + (self.destination.utc - self.origin.utc)

    def dict_ticket(self):
        tracker = f'{self.origin.loc}{self.destination.loc}{self.flight_time.strftime("%Y%m%d%H%M")}'
        ticket = {
                'From': self.origin.name,
                'To:': self.destination.name,
                'At:': self.flight_time.strftime('%Y-%m-%d %H:%M'),
                'ETA': self.ETA.strftime('%Y-%m-%d %H:%M')
                }
        return tracker, ticket

    def __str__(self):
        return f'From: {self.origin.loc} To: {self.destination.loc} {self.ETA} hours'


class Airport:
    def __init__(self, loc, city, name, utc, fligts):
        self.loc = loc
        self.city = city
        self.name = name
        self.utc = utc
        self.flights = fligts

    def destinies(self):
        return (loc for loc in self.flights)

    def departures_to(self, loc):
        try:
            return self.flights[loc]['departures']
        except:
            return None

    def flight_time_to(self, loc):
        try:
            return self.flights[loc]['flight_time']
        except:
            return None

    def __str__(self):
        return f'{self.loc}-{self.name}'

    def __repr__(self):
        return f'{self.loc}-{self.name}'