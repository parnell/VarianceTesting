import logging
import sys
import os

logdir = '/home1/01208/parnell/logs'
DL = 1

if not os.path.exists(logdir):
    os.mkdir(logdir)

log = logging.getLogger("mainLogger")
log.setLevel(logging.INFO)

dlog = logging.getLogger("logLogger")
dlog.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
log.addHandler(sh)

sh = logging.StreamHandler(open(logdir+'/err.log','w'))
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
dlog.addHandler(sh)

sh = logging.StreamHandler(open(logdir+'/allerr.log','a'))
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
dlog.addHandler(sh)


def __fmt(*args):
    if issubclass(type(args), list) \
            or issubclass(type(args), tuple):
        return " ".join([str(x) for x in args])
    else:
        return args

def printl(*args):
    if DL > 0:
        log.info(__fmt(*args))
    dlog.info(__fmt(*args))

def printd(*args):
    if DL > 1:
        log.info(__fmt(*args))
    dlog.info(__fmt(*args))

def printe(*args):
    dlog.error(__fmt(*args))

def stacktrace():
    stacktracem("")

def stacktracem(msg, *args):
    dlog.exception(msg, *args)
