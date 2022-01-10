import json
from os import path

filename = 'woeids.json'
dirpath = path.dirname(__file__)
path = path.join(dirpath, filename)

def get_data():
    try:
        with open(path) as file:
            return json.load(file)
    except Exception:
        print(f'Error: Unable to Read {filename}')
        return {}


def write_data(data, message=False):
    try:
        with open(path, 'w') as file:
            if message:
                print(f'Writing to {file}...', end=' ')
            json.dump(data, file, indent=4, ensure_ascii=False)
            if message:
                print('Done!')
    except Exception:
        print(f'Error: Unable to Write {filename}')