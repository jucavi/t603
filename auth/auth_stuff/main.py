import os.path
import getpass
import hashlib
import db
import json
from deco import logger
from time import sleep
from user import User
from auth import Auth


CWD = os.path.dirname(__file__)
db_name = 'app_db.json'

@logger
def signup():
    username = input('User Name: ').strip()
    while True:
        password = getpass.getpass('Password: ')
        conf_pass = getpass.getpass('Confirm password: ')
        if password == conf_pass and password:
            break

    password = hashlib.sha256(password.encode()).hexdigest()

    if username:
        users.append({'username': username, 'password': password})
        print(f'User @{username} successfully created.')
        sleep(1)
        return User(username, password)

@logger
def login():
    username = input('User name: ')
    password = getpass.getpass('Password: ')
    password = hashlib.sha256(password.encode()).hexdigest()
    user = find_user(username)

    if user:
        user_password = user['password']
        if user_password == password:
            print(f'User @{username} logged in')
            sleep(1)
            return User(username, password)

def find_user(name):
    user = list(filter(lambda user: user['username'] == name, users))
    if user:
        return user[0]

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

def create_db(name, *tables):
    data = db.DB(name, CWD)
    for table in tables:
        data.write_table(table)
    return data


users = db.Table('user', ('name', 'pwd'))
data = create_db('app_db', users)
guest = User('guest', 'guest_pass')

while True:
    os.system('clear')
    print('[1] Signup')
    print('[2] Login')
    print('[Q] Exit\n')
    option = input('>> ')

    if option.lower() == 'q':
        data.write_table(users)
        break

    if option == '1':
        username = input('User Name: ').strip()
        while True:
            password = getpass.getpass('Password: ')
            conf_pass = getpass.getpass('Confirm password: ')
            if password == conf_pass and password:
                break

        auth = Auth(users)
        user = auth.signup(User(username, password))

    elif  option == '2':
        user = login()

#     if not user:
#         user = user_gest

#     print('Accessing....')
#     sleep(6)