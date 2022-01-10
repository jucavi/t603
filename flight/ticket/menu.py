from helpers import clear, clear_await, f2delta, set_tomorrow
from models import Flight, make_menu, numeric_menu_with_return
import manager


COUNTRIES = {
    "ARG": "Argentina",
    "PER": "Peru",
    "SPA": "Spain",
    "BRA": "Brazil"
}

def from_to_menu(locs, airports):
    index = numeric_menu_with_return((COUNTRIES[loc] for loc in locs))
    return airports[locs[index]], locs[index]

def list_tickets_menu(update=True):
    tickets = manager.ticket_list()
    tickets_ids = tuple(tickets.keys())
    index = numeric_menu_with_return(tickets.keys(), prompt='Seleccione el ticket: ')
    try:
        return tickets_ids[index], index
    except:
        return None, None

@clear_await
def buy_menu():
    airports = manager.airports_list()
    if airports:
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
    ticket_id, index = list_tickets_menu()
    if index != None:
        manager.remove_ticket(ticket_id)
        buy_menu.__wrapped__()
    else:
        print('Not tickets found!')


@clear_await
def remove_menu():
    ticket_id, index = list_tickets_menu(update=False)
    if index != None:
        manager.remove_ticket(ticket_id)
    else:
        print('Not tickets found!')

@clear_await
def view_menu():
    ticket_id, index = list_tickets_menu()
    if index != None:
        tickets = manager.ticket_list()
        for key, value in tickets[ticket_id].items():
            print(f'{key:9}: {value}')
    else:
        print('Not tickets found!')


main_menu_gen = (
    (1, 2, 3, 4, 'Q'),
    ('Buy a ticket', 'Modify ticket', 'Remove ticket', 'View ticket', 'Quit'),
    (buy_menu, modify_menu, remove_menu, view_menu, exit)
)

main_menu = make_menu(*main_menu_gen)
def loop():
    while True:
        clear()
        print('Flight Ticket Seller\n')
        print(main_menu)
        main_menu.execute_option('>>')
