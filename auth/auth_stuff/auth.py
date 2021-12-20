from deco import logger
from user import Guest, User, Admin
class Auth:
    def __init__(self, table):
        self._table = table

    def get_user(self, user):
        return self._table.find_where('username', user.username)

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
        if user.password == db_user['password']:
            if db_user['is_admin']:
                return Admin(db_user['username'], db_user['password'])
            return User(db_user['username'], db_user['password'])

