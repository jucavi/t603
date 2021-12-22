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

    def get_user(self, user):
        return self._table.find_where('username', user.username)

    def cookie(self, user, set=True):
        pass

    def token_gen(self, user):
        self.get_secret()
        identifier = sha256(user.username.encode()).hexdigest()
        secret = environ['AuthCICE']
        rand = sha256(str(random.random()).encode()).hexdigest()
        return f'{identifier}.{secret}.{rand}'


    def signup(self, user):
        if self.get_user(user):
            return False
        self._table.add_row((user.username, user.password, False))
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
        pass
