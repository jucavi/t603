import requests
import os
import json

path = os.path.join(os.path.dirname(__file__), 'flags.json')
url = 'https://restcountries.com/v3.1/name'

def load_flags():
    try:
        with open(path) as file:
            flags = json.load(file)
    except:
        flags = {}
        
    return flags
    

def get_country(name):
    country = requests.get(f'{url}/{name}')
    if country.ok:
        country = country.json()[0]
        return {
            'name': country['name']['common'],
            'population': country['population'],
            'area': country['area'],
            'capital': country['capital'][0],
            'languages': list(country['languages'].values()),
            'flag': country['flags']['png']
        }
    else:
        print(f'Country {name} not found')
        return {}


def add_flag(country, flags):
    flags[country['name']] = country['flag']
    
    
def write_flags(flags):
    with open(path, 'w') as file:
        json.dump(flags, file, indent=4, sort_keys=True)


def print_country(country):
    for key, value in country:
        print(f'{key}: {value}')


def main_screen():
    print(f'[1] Country')
    print(f'[2] Flag download')
    print(f'[Q] Quit')


country = get_country('sadfasdf')
if country:
    flags = load_flags()
    add_flag(country, flags)
    write_flags(flags)
    print(country)
# while True:
#     main_screen()
#     user = input(': ')
    
#     if user.lower() == 'q':
#         break
    
#     if user == '1':
#         search = input('Country: ')
#         country = get_country(search)
#         print(country)
#         print(type(country['flag']))