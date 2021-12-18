class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def is_admin(self):
        return False

    def __str__(self):
        return f'@{self.username}'

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    @property
    def is_admin(self):
        return True

    def __str__(self):
        return f'@admin_{super().__str__()}'