from deco import logger
from user import Guest, User, Admin
from hashlib import sha256
import random

class Auth:
    # os.environ ##
    __super_secret = 'l3tM3g0'

    def __init__(self, table):
        self._table = table

    def get_user(self, user):
        return self._table.find_where('username', user.username)


    def token_gen(self, user):
        identifier = sha256(user.username.encode()).hexdigest()
        secret = sha256(self.__super_secret.encode()).hexdigest()
        rand = sha256(str(random.random()).encode()).hexdigest()
        return f'{identifier}.{secret}.{rand}'


    def signup(self, user):
        if self.get_user(user):
            return False
        self._table.add_row((user.username, user.password, False, ''))
        return True

    @logger
    def login(self, user):
        db_user = self.get_user(user)
        if not db_user:
            user = Guest()
        elif user.password == db_user['password']:
            if db_user['is_admin']:
                user = Admin(db_user['username'], db_user['password'])
            else:
                user = User(db_user['username'], db_user['password'])

        token = self.token_gen(user)
        user.session = token

        if not isinstance(user, Guest):
            user.token = token
            user_id = self._table.get_id_by('username', user.username)
            self._table.update_by_id(user_id, 'token', token)

        return user
