# pwd = 'topSecret'

# user_pwd = input('pwd: ')

# print('Success' if pwd == user_pwd else 'Fail!')

class Human:
    counter = 0
    
    def __init__(self, w):
        Human.counter += 1
        self.wathever = w

    def funct(cls):
        cls.wathever = 0

a = Human(3)
a.funct()
print(a.wathever)