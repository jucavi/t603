from log import logger
from user import Guest, User, Admin
from hashlib import sha256
import random
from os import environ, path
import json
import secret

class Auth:
    __path = path.dirname(__file__)

    def __init__(self, table):
        self._table = table

    def get_secret(self):
        secret.setup()

    def set_token(self, user, token):
        auth_user_id = self._table.get_id_by('username', user.username)
        self._table.update_by_id(auth_user_id, 'token', token)

    def is_active_token(self, user):
        self.get_secret()

    def get_user(self, user):
        return self._table.find_where('username', user.username)

    @property
    def cookies(self):
        try:
            with open(path.join(self.__path, 'cookies.json')) as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def set_cookie(self, user):
        cookies = self.cookies
        token = self.token_gen(user)
        cookie = {
            user.username: { 'token': token }
        }
        cookies.update(cookie)
        with open(path.join(self.__path, 'cookies.json'), 'w') as file:
                json.dump(cookies, file, indent=4, ensure_ascii=False)
        self.set_token(user, token)

    def token_gen(self, user):
        self.get_secret()
        identifier = sha256(user.username.encode()).hexdigest()
        secret = environ['AuthCICE']
        rand = sha256(str(random.random()).encode()).hexdigest()
        return f'{identifier}.{secret}.{rand}'


    def signup(self, user):
        if self.get_user(user):
            return False
        self._table.add_row((user.username, user.password, user.is_admin, None))
        return True

    @logger
    def login(self, user):
        db_user = self.get_user(user)
        if not db_user:
            return Guest()
        elif user.password == db_user['password']:
            if db_user['is_admin']:
                user = Admin(db_user['username'], db_user['password'])
            else:
                user = User(db_user['username'], db_user['password'])
            self.set_cookie(user)
        return user

    @logger
    def logout(self, user):
        self.set_token(user, None)
        return user

