from functools import wraps
from datetime import datetime
import os.path

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        pathfile = os.path.join(os.path.dirname(__file__), 'call.log')
        with open(pathfile, 'a+') as file:
            try:
                file.write(f'{datetime.now()}| {func.__name__.capitalize()} {result.username!r} as {type(result).__name__}\n')
            except Exception:
                file.write(f'{datetime.now()}| Function {func.__name__}\n')
        return result
    return wrapper