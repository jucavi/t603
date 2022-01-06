from helpers import clear, clear_await, f2delta
from models import Flight, make_menu, numeric_menu_with_return
import parser
from datetime import datetime


COUNTRIES = {
    "ARG": "Argentina",
    "PER": "Peru",
    "SPA": "Spain",
    "BRA": "Brazil"
}

@clear_await
def buy_menu():
    airports = parser.airports_list()

    print('From:')
    origins_locs = tuple(loc for loc in airports)
    index = numeric_menu_with_return((COUNTRIES[loc] for loc in origins_locs))
    origin = airports[origins_locs[index]]
    print(origin)

    print('To:')
    destinies_locs = tuple(origin.destinies())
    index = numeric_menu_with_return((COUNTRIES[loc] for loc in destinies_locs))
    destiny = airports[destinies_locs[index]]
    print(destiny)

    print('At:')
    departures = origin.flights[destinies_locs[index]]['departures']
    departure_time = origin.flights[destinies_locs[index]]['flight_time']
    index = numeric_menu_with_return(departures)
    departure = departures[index]
    print(departure)

    print(Flight(origin,
                 destiny,
                 f2delta(departure_time),
                 datetime.strptime(departure, '%H:%M') #for tomorrow
                )
         )





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
