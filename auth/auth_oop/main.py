import os.path
import getpass
from db import DB, Table
from auth import Auth
from user import User


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
auth_users = []

while True:
    os.system('clear')
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
        auth_users.append(user)
        print(user)
        try:
            print(user.token)
        except:
            pass
        print(user.session)
        input()

    data.save()