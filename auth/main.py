users = {'user': []}

def signup():
    pass

def login():
    pass

while True:
    print('[1] Signup')
    print('[2] Login')
    print('[Q] Exit')
    option = input('> ')

    if option.lower() == 'q':
        break

    if option == '1':
        signup()
    elif  option == '2':
        pass