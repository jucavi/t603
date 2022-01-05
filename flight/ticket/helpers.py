import os
import platform
import json

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def fullpath(filename, path=''):
    path = path or os.path.dirname(__file__)
    return os.path.join(path, filename)

def load_json_data(filename, path=''):
    try:
        with open(fullpath(filename, path)) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Unable to find {filename} in ./{path}')
    except json.decoder.JSONDecodeError:
        print(f'Invalid data or corrupt file!')

def write_json_data(data, filename, path='', overwrite=False):
    filepath = fullpath(filename, path)

    if os.path.exists(fullpath):
        if not overwrite:
            print(f'{filename} already exists!')
            overwrite = input('Confirm overwriting (Y/n): ').lower() == 'y'

    if overwrite:
        with open(filepath, 'w+') as f:
            json.dump(data, f)
