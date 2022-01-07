from helpers import ticket

class IdentifierError(Exception):
    pass

class Option:
    def __init__(self, identifier, message, func):
        self.__set_func(func)
        self.message = message
        self.id = str(identifier).upper()

    def __set_func(self, func):
        if not hasattr(func, '__call__'):
            self.func = lambda: f'{self.message}, not implmented yet!'
        else:
            self.func = func

    def __str__(self):
        return f'[{self.id}] {self.message}'

class NumOption(Option):
    def __init__(self, identifier, message, func=None):
        self.__is_valid(identifier)
        super().__init__(identifier, message, func)

    def __is_valid(self, identifier):
        if not (isinstance(identifier, int) or identifier.isdigit()):
            raise IdentifierError('Id must be numeric value')

class AlphaOption(Option):
    def __init__(self, identifier, message, func=None):
        self.__is_valid(identifier)
        super().__init__(identifier, message, func)

    def __is_valid(self, identifier):
        if not (isinstance(identifier, str) and identifier.isalpha() and len(identifier) == 1):
            raise IdentifierError('Id must be a character value')

class OptionMenu():
    def __init__(self, options=None):
        self.options = dict()
        if options:
            self.__set_options(options)

    def __set_options(self, options):
        for option in options:
            self.add_option(option)

    def add_option(self, option):
        if isinstance(option, Option):
            self.options[option.id.lower()] = option

    def __str__(self):
        return "\n".join(f'{option}' for option in self.options.values())


    def execute(self, identifier):
        identifier = str(identifier).lower()
        if identifier in self.options:
            self.options[identifier].func()

    def get_identifier(self, message):
        identifier = input(f'\n{message} ').strip().lower()
        while True:
            if identifier in self.options:
                print()
                return identifier
            identifier = input(f'Invalid option try again: ')

    def execute_option(self, message):
        identifier = self.get_identifier(message)
        self.execute(identifier)

@ticket('tickets.json')
class Flight:
    def __init__(self, origin, destiny, departure_time, flight_time):
        self.destiny = destiny
        self.origin = origin
        self.departure_time = departure_time
        self.flight_time = flight_time

    @property
    def ETA(self):
        return self.departure_time + self.flight_time + (self.destiny.utc - self.origin.utc)

    def dict_ticket(self):
        tracker = f'{self.origin.loc}{self.destiny.loc}{self.flight_time.strftime("%Y%m%d%H%M")}'
        ticket = {
                'From': self.origin.name,
                'To:': self.destiny.name,
                'At:': self.flight_time.strftime('%Y-%m-%d %H:%M'),
                'ETA': self.ETA.strftime('%Y-%m-%d %H:%M')
                }
        return tracker, ticket

    def __str__(self):
        return f'From: {self.origin.loc} To: {self.destiny.loc} {self.ETA} hours'


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

def make_menu(identifiers, messages, funcs):
    menu = OptionMenu()
    for identifier, message, func in zip(identifiers, messages, funcs):
        try:
            menu.add_option(NumOption(identifier, message, func))
        except IdentifierError:
            try:
                menu.add_option(AlphaOption(identifier, message, func))
            except IdentifierError:
                pass
    return menu

def make_numeric_menu(items):
    menu = OptionMenu()
    for i, item in enumerate(items, start=1):
        menu.add_option(NumOption(i, item))
    return menu

def numeric_menu_with_return(items, prompt='>>', cap=False):
    if items:
        menu = make_numeric_menu(items)
        print(menu)
        str_index = menu.get_identifier(prompt)
        return int(str_index) - 1
    return None


if __name__ == '__main__':
    # print(numeric_menu_with_return(list('agua')))
    pass