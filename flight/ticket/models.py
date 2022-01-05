class IdentifierError(Exception):
    pass

class Option:
    def __init__(self, identifier, message, func):
        self.__set_func(func)
        self.message = message.capitalize()
        self.id = str(identifier).upper()

    def __set_func(self, func):
        if not hasattr(func, '__call__'):
            self.func = lambda: f'{self.message}, not implmented yet!'
        else:
            self.func = func

    def __str__(self):
        return f'[{self.id}] {self.message}'

class NumOption(Option):
    def __init__(self, identifier, message, func):
        self.__is_valid(identifier)
        super().__init__(identifier, message, func)

    def __is_valid(self, identifier):
        if not (isinstance(identifier, int) or identifier.isdigit()):
            raise IdentifierError('Id must be numeric value')

class AlphaOption(Option):
    def __init__(self, identifier, message, func):
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

    def print(self):
        for option in self.options.values():
            print(option)

    def execute(self, identifier):
        identifier = str(identifier).lower()
        if identifier in self.options:
            self.options[identifier].func()

    def get_identifier(self, message):
        identifier = input(f'{message} ').strip().lower()
        while True:
            if identifier in self.options:
                return identifier
            identifier = input(f'Invalid option try again: ')

    def execute_option(self, message):
        identifier = self.get_identifier(message)
        self.execute(identifier)

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
