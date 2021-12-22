from posixpath import commonpath
from log import logger
from user import Guest, User, Admin
from hashlib import sha256
import random
from os import environ, path
import json
import secret
from functools import wraps

class Auth:
    __path = path.dirname(__file__)

    def __init__(self, table):
        self._table = table

    def get_secret(self):
        '''Generate new secret based on time'''
        secret.setup()

    def set_token(self, user, token):
        auth_user_id = self._table.get_id_by('username', user.username)
        self._table.update_by_id(auth_user_id, 'token', token)

    def is_active_token(self):
        self.get_secret()
        username, token = self.cookies.get('token', {'user': None,  'token': None}).values()
        if token:
            token_shunk = token.split('.')[1]
            secret = environ['AuthCICE']
            if secret == token_shunk:
                user = User(username, '')
                auth_user_id = self._table.get_id_by('username', username)
                user.password = self._table.find_by_id(auth_user_id)['password']
                return self.login(user)
        return Guest()

    def get_user(self, user):
        return self._table.find_where('username', user.username)

    def authenticate(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username, token = self.cookies['token'].values()
            user = self._table.find_where('username', username)
            if token and user:
                if token == user['token'] and self.is_active_token():
                    return func(*args, **kwargs)
                else:
                    return False
        return wrapper

    @property
    def cookies(self):
        try:
            with open(path.join(self.__path, 'cookies.json')) as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def set_cookie(self, user, auth=True):
        cookies = self.cookies
        token = self.token_gen(user) if auth else None
        cookie = {
            'token': {
                'user': user.username,
                'token': token
            }
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
        self.set_cookie(user, auth=False)
        return user

