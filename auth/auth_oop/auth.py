from log import logger
from user import Guest, User, Admin
from hashlib import sha256
import random
from os import environ
import secret

class Auth:
    def __init__(self, table):
        self._table = table

    def get_secret(self):
        secret.setup()

    def is_active_token(self, user):
        self.get_secret()
        auth_user = self.get_user(user)
        if auth_user:
            if auth_user['token']:
                return auth_user['token'].split('.')[1] == environ['AuthCICE']
        return False

    def get_user(self, user):
        return self._table.find_where('username', user.username)

    def cookie(self, user, set=True):
        if not isinstance(user, Guest) and set: # if login return None delete this
            token = self.token_gen(user)
            user.token = token
        else:
            token = None
        user_id = self._table.get_id_by('username', user.username)
        self._table.update_by_id(user_id, 'token', token)

    def token_gen(self, user):
        self.get_secret()
        identifier = sha256(user.username.encode()).hexdigest()
        secret = environ['AuthCICE']
        rand = sha256(str(random.random()).encode()).hexdigest()
        return f'{identifier}.{secret}.{rand}'


    def signup(self, user):
        if self.get_user(user):
            return False
        self._table.add_row((user.username, user.password, False, None))
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
            self.cookie(user)
        return user

    @logger
    def logout(self, user):
        user.token = None
        self.cookie(user, set=False)
        return user
