import os
import json
import getpass
import base64
from time import sleep
from deco import logger

CWD = os.path.dirname(__file__)
db_name = 'app_db.json'

@logger
def signup():
    username = input('User Name: ')
    while True:
        password = getpass.getpass('Password: ').encode()
        password = base64.b64encode(password).decode()
        conf_pass = getpass.getpass('Confirm password: ').encode()
        conf_pass = base64.b64encode(conf_pass).decode()
        if password == conf_pass:
            break
    user = {
        'username': username,
        'password': password
    }
    users.append(user)
    print(f'User {username} successfully created.')
    sleep(1)
    return user

def find_user(name):
    return list(filter(lambda user: user['username'] == name, users))[0]

@logger
def login():
    name = input('User name: ')
    password = getpass.getpass('Password: ')
    user = find_user(name)

    if user:
        user_password = base64.b64decode((user['password'].encode())).decode()
        if user_password == password:
            print(f'User {name} log in')
            sleep(1)
            return user

def load_db(name, path='.'):
    try:
        with open(os.path.join(path, name)) as f:
            data = json.load(f)
        return data
    except:
        print(f'Unable to read {name!r}')
        return {'data': {}}

def write_db(data, name, path='.'):
    with open(os.path.join(path, name), 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


data = load_db('app_db.json', path=CWD)
users = data['data'].setdefault('users', [])

while True:
    os.system('clear')
    print('[1] Signup')
    print('[2] Login')
    print('[Q] Exit')
    option = input('> ')

    if option.lower() == 'q':
        write_db(data, db_name, path=CWD)
        break

    if option == '1':
        signup()
    elif  option == '2':
        login()