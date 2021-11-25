import json
from os import path, sep

filename = 'woeids.json'
dirpath = path.dirname(__file__)
path = path.join(dirpath, filename)

def get_data():
    try:
        with open(path, encoding='utf-8') as file:
            data = json.load(file)
    except Exception:
        print(f'Error: Unable to Read {filename}')
        data = {}
    
    return data


def write_data(data):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            print(f'Writing to {file}...', end=' ')
            json.dump(data, file, indent=4)
            print('Done!')
    except Exception:
        print(f'Error: Unable to Write {filename}')