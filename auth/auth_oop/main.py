import os.path
import getpass
from db import DB, Table
from auth import Auth
from user import User, Guest
from functools import wraps


CWD = os.path.dirname(__file__)
db_name = 'app'
table_name = 'users'

data = DB(db_name, CWD)
data.setup()
if data.tables:
    users = data.find(table_name)
else:
    users = Table(table_name, ('username', 'password', 'is_admin', 'token'))
    data.append_table(users)

auth = Auth(users)
user = Guest()

def global_space():
    if isinstance(user, Guest):
        print('[1] Signup')
        print('[2] Login')
    else:
        print('[3] Browse')
        if user.is_admin:
            print('[4] Admin Area')
        print('[5] Logout')
    print('[Q] Exit\n')
    option =  input('>> ')
    return option

@auth.authenticate
def admin_space():
    if user.is_admin:
        while True:
            os.system('clear')
            print('[1] List Users')
            print('[2] Set admin role')
            print('[Q] Back to main\n')
            option = input('>> ')

            if option.lower() == 'q':
                data.save()
                break

            if option == '1':
                # TODO paginate
                print(users)
                input()

            if option == '2':
                try:
                    user_id = int(input('Select user id: '))
                    users.update_by_id(user_id, 'is_admin', True)
                    data.save()
                except:
                    pass

@auth.authenticate
def user_space():
    input('Browse the page!!!...')

def log_out(user):
    auth.logout(user)


while True:
    os.system('clear')
    user = auth.is_active_token()
    option = global_space()

    if option.lower() == 'q':
        break

    if option == '1':
        username = input('User Name: ').strip()
        while True:
            password = getpass.getpass('Password: ')
            conf_pass = getpass.getpass('Confirm password: ')
            if password == conf_pass and password:
                break
        if auth.signup(User(username, password)):
            input('Successfully singup')
        else:
            input(f'{username!r} already exists!')

    elif  option == '2':
        username = input('User Name: ').strip()
        password = getpass.getpass('Password: ')
        user = auth.login(User(username, password))

    elif option == '3':
        user_space()

    elif option == '4':
        admin_space()

    elif option == '5':
        log_out(user)

    data.save()