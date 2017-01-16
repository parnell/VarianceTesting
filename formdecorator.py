from functools import wraps

from logger import stacktrace

class FFException(Exception):
    def __init__(self, exception, *args, **kwargs):
        '''
        The original exception with the parameters used in the function call
        '''
        super().__init__("%s" %exception)
        self.exception = exception
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return str(self.exception)

    def __reduce__(self):
        '''
        To make our FFException work with pickle
        append our exception to the beginning of args
        '''
        ps = super().__reduce__()
        state = (ps[2]['exception'],) + ps[1]
        return (ps[0], state, ps[2])



def FailFree(func):
    '''
    Decorator to wrap a function and prevent it from throwing an Exception
    This allows for multiproccessing on the function which won't
    stop the entire threaded run for one bad function.

    return: original return of the function,
            or an Exception if one occurred
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            nargs = args
            if args:
                nargs = []
                for x in args:
                    if isinstance(x, dict):
                        nargs.append(x.__class__)
                    else:
                        nargs.append(x)
            stacktrace("\n%s in %s" %(e.__class__.__name__,str(func.__name__)), *nargs,**kwargs)
            return FFException(e, *args, **kwargs)
        except:
            stacktrace("Error of some sort")
    return wrapper
