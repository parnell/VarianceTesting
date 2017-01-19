import time
import random
from functools import wraps
from logger import printl

class CountdownTimer():
    def __init__(self, seconds, sigma=None, minimum=None):
        self.seconds = seconds
        if sigma is not None:
            self.seconds = random.gauss(seconds, sigma)
            if minimum is not None:
                self.seconds = max(self.seconds, minimum)

        self.starttime = time.time()

    def ellapsed(self):
        return time.time() - self.starttime > self.seconds

    def reset(self, seconds=None):
        if seconds is not None:
            self.seconds = seconds
        self.starttime = time.time()
    def __str__(self):
        return '[CountdownTimer remaining=%d]' %(self.seconds - (time.time() - self.starttime))

class Timer():
    mult = None
    def __init__(self):
        self.time = 0
        self.start() ## init time
        self.starttime = self.time
        self.mult = None

    def reset(self):
        self.start()
        self.starttime = self.time

    def millis(self):
        return int(round(time.time() * 1000))

    def start(self):
        self.time = self.millis()

    def ellapsed(self):
        curtime = self.millis()
        dif = curtime - self.time
        self.time = curtime
        return dif

    def greater(self, milli):
        dif = self.millis() - self.time
        return dif > milli

    def totalellapsed(self):
        return self.millis() - self.starttime

    def waitseconds(self, seconds):
        self.wait(seconds*1000)

    def wait(self, milliseconds):
        curtime = self.millis()
        timedif = curtime - self.time
        if timedif < milliseconds:
            time.sleep( (milliseconds-timedif)*0.001)
        self.time = curtime

    def rawwait(self, milli):
        time.sleep(milli/1000)

    @staticmethod
    def setMult(mult):
        Timer.mult = mult

    @staticmethod
    def sleep(seconds):
        if Timer.mult: seconds *= Timer.mult
        time.sleep(seconds)

    @staticmethod
    def sleepm(millis):
        if Timer.mult: millis *= Timer.mult
        time.sleep(millis)

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        if len(args) > 0 and 'Data' == args[0].__class__.__name__:
            printl('func<%r %s %s> took: %2.4f sec' %(
                func.__name__,
                args[0].cfg.S,
                args[0].cfg.D,
                te-ts))
        else:
            printl('func<%r> took: %2.4f sec' %(func.__name__, te-ts))
        return result

    return wrapper
