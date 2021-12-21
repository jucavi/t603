import hashlib

class GlobalUser:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.token = None

    @property
    def is_admin(self):
        return False

    def __str__(self):
        return f'@{self.username}'

class Guest(GlobalUser):
    def __init__(self):
        super().__init__('guest', '')

    @property
    def is_auth(self):
        return False

    def __str__(self):
        return f'{super().__str__()}'

class User(GlobalUser):
    def __init__(self, username, password):
        super().__init__(username, password)

    
    def __str__(self):
        return f'{super().__str__()}'

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    @property
    def is_admin(self):
        return True

    def __str__(self):
        return f'@admin/{self.username}'