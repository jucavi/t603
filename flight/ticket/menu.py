from helpers import clear
from models import make_menu

identifiers = (
    1,
    2,
    3,
    'q'
)
messages = (
    'buy a ticket',
    'modify ticket',
    'remove ticket',
    'quit'
)
funcs = (
    'pass',
    'pass',
    'pass',
    exit
)

menu = menu = make_menu(identifiers, messages, funcs)

def loop():
    while True:
        clear()
        print('Flight Ticket Seller\n')
        menu.print()
        menu.execute_option('>>')
