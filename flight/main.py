from datetime import utcnow
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
    print('[1] Modificar Vuelo')
    print('[1] Cancelar Vuelo')
    print('[Q] Salir')

def load_data():
    with open(DB) as file:
        return json.load(file)

def translate(loc):
    return LEG.get(loc, None)

user = ''
while user.lower() != 'q':
    menu()
    option = input(': ')


