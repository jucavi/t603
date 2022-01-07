from helpers import clear, clear_await, f2delta, set_tomorrow
from models import Flight, make_menu, numeric_menu_with_return
import parser


COUNTRIES = {
    "ARG": "Argentina",
    "PER": "Peru",
    "SPA": "Spain",
    "BRA": "Brazil"
}

def from_to_menu(locs, airports):
    index = numeric_menu_with_return((COUNTRIES[loc] for loc in locs))
    return airports[locs[index]], locs[index]

@clear_await
def buy_menu():
    airports = parser.airports_list()

    print('From:')
    origins_locs = tuple(loc for loc in airports)
    origin, _ = from_to_menu(origins_locs, airports)

    print('To:')
    destinies_locs = tuple(origin.destinies())
    destiny, loc = from_to_menu(destinies_locs, airports)
    flight_time = origin.flight_time_to(loc)

    print('At:')
    departures = origin.flights[loc]['departures']
    index = numeric_menu_with_return(departures)
    departure = departures[index]

    _, tracker = Flight(origin, destiny, f2delta(flight_time), set_tomorrow(departure))
    print(f'Keep! Tracking code: {tracker}')

@clear_await
def modify_menu():
    print('Modify!')

@clear_await
def remove_menu():
    print('Remove!')

main_menu_gen = (
    (1, 2, 3, 'q'),
    ('buy a ticket', 'modify ticket', 'remove ticket', 'quit'),
    (buy_menu, modify_menu, remove_menu, exit)
)

main_menu = make_menu(*main_menu_gen)
def loop():
    while True:
        clear()
        print('Flight Ticket Seller\n')
        print(main_menu)
        main_menu.execute_option('>>')
