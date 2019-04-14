import threading
import time
from unidecode import unidecode


def sanitise_artist(artist):
    return unidecode(artist).lower().replace(' ', '').replace('.', '').replace(',', '').replace('&', 'and').replace("'", '').replace('"', '').replace('/', '').replace('-', '')


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def timeit(function):
    def timed(*args, **kw):
        start_time = time.time()
        result = function(*args, **kw)
        end_time = time.time()
        print('%r %r %r  %2.2f ms' %
              (function.__name__, args, kw, (end_time - start_time) * 1000))
        return result
    return timed
