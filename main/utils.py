def logger(func):
    def inner(*args, **kwargs):
        print(func.__name__ + "(%s, %s)" % (args, kwargs))
        return func(*args, **kwargs)
    return inner
