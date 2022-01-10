from functools import wraps

def dec(func):
    @wraps(func)
    def wrapp(*args, **kwargs):
        print('Decorated!')
        return func(args, kwargs)
    return wrapp


@dec
def sin_wrapps():
    pass

print(sin_wrapps.__dict__)

