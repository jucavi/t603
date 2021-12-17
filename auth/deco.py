from functools import wraps
import datetime
import os

def upper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def em(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f'{func(*args, **kwargs)}!!!'
    return wrapper

def deco_with_args(arg1):
    def decorator(func):
        print(f'Passed {arg1=}')
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrap = '*' * arg1
            return f'{wrap}\n{func(*args, **kwargs)}\n{wrap}'
        return wrapper
    return decorator

def logger(func):
    pass

@deco_with_args(28)
@upper
@em
def greeting(name):
    return f'Hola {name}'

###########################################

def logger(func):
    def wrapper(*args, **kwargs):
        pathfile = os.path.join(os.path.dirname(__file__), 'call.log')
        with open(pathfile, 'a+') as file:
            file.write(f'{datetime.datetime.now()}| {func.__name__}\n')
        return func(*args, **kwargs)
    return wrapper

@logger
def greeting(name):
    return f'Hello {name}'

@logger
def regards(name):
    return f'Hi! {name}'

f_list = [regards, greeting, regards, regards] * 6
name = 'Paul'

for f in f_list:
    f(name)
