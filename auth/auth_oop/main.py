import os.path
import getpass
from db import DB, Table
from auth import Auth
from user import User, Guest


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

def admin_space():
    while True:
        os.system('clear')
        print('[1] List Users')
        print('[2] Set admin role')
        print('[Q] Exit\n')
        option = input('>> ')

        if option.lower() == 'q':
            data.save()
            break

        if option == '1':
            print(users) # TODO paginate
            input()

        if option == '2':
            user_id = int(input('Select user id: '))
            users.update_by_id(user_id, 'is_admin', True)

while True:
    os.system('clear')
    if user.token and auth.is_active_token(user):
        print('[3] Browse')
        if user.is_admin:
            print('[4] Create Admin')
        print('[5] Logout')
    else:
        print('[1] Signup')
        print('[2] Login')
    print('[Q] Exit\n')
    option = input('>> ')

    if option.lower() == 'q':
        break

    if option == '1':
        username = input('User Name: ').strip()
        while True:
            password = getpass.getpass('Password: ')
            conf_pass = getpass.getpass('Confirm password: ')
            if password == conf_pass and password:
                break
        if not auth.signup(User(username, password)):
            input(f'{username!r} already exists!')

    elif  option == '2':
        username = input('User Name: ').strip()
        password = getpass.getpass('Password: ')
        user = auth.login(User(username, password))

    elif option == '3':
        input('Now you can browse the page....')

    elif option == '4':
        admin_space()

    elif option == '5':
        user = auth.logout(user)

    data.save()