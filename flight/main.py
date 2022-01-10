from datetime import datetime, timedelta
import json
import os

DB = os.path.join(os.path.dirname(__file__), 'airports.json')
LEG = {
    "ARG": "Argentina",
    "PER": "Peru",
    "SPA": "Spain",
    "BRA": "Brazil"
}

def menu():
    print('[1] Comprar Vuelo')
    print('[2] Modificar Vuelo')
    print('[3] Cancelar Vuelo')
    print('[Q] Salir')

def load_data():
    with open(DB) as file:
        return json.load(file)

def translate(loc):
    return LEG.get(loc, None)

def validate_input(msg, num_options, str_op=('q',)):
    option = input(f'{msg}: ')
    while True:
        if option.lower() in str_op:
            return option
        try:
            if (int(option) - 1) in range(num_options):
                return option
            else:
                raise IndexError
        except KeyboardInterrupt:
            exit(0)
        except Exception:
            option = input('Enter valid option: ')

def option_list_menu(enum_items, **kwargs):
    for i, item in enumerate(enum_items, start=1):
        print(f'[{i}] {item.title()}')

    if  kwargs:
        for k, value in kwargs.items():
            print(f'[{k.upper()}] {value.title()}')

def option_origins():
    origins = map(lambda orig: translate(orig), locs)
    option_list_menu(origins)
    option =  int(validate_input('From', len(locs)))
    return locs[option - 1], data[locs[option - 1]]

def list_destinies(origin):
    destinies = [destiny for destiny in origin['dest'].keys()]
    option_list_menu(map(lambda dest: translate(dest), destinies))
    option = int(validate_input('To', len(destinies)))
    return destinies[option - 1], origin['dest'][destinies[option - 1]]

def list_departures(destiny_flights):
    departures = [time for time in destiny_flights['departures']]
    option_list_menu(departures)
    option = int(validate_input('Departure', len(departures)))
    return departures[option - 1]

def str2time(time):
    return datetime.strptime(time, '%H:%M').time()

def flight_departure(departure):
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    return datetime.combine(tomorrow, departure)



data = load_data()
user = ''
locs = list(data.keys())
while user.lower() != 'q':
    menu()
    user = validate_input('', 3)

    if user == '1':
        loc, origin = option_origins()
        print(origin)
        loc, destiny_flights = list_destinies(origin)
        print(destiny_flights)
        flight_time = destiny_flights['flight_time']
        departure = list_departures(destiny_flights)
        departure = str2time(departure)
        print(flight_departure(departure))


