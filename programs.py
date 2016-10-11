import subprocess
import configuration as cfg
import os
import sys

def run(cmd, printcmd=False):
    cmd = [str(x) for x in cmd]
    if printcmd:
        print(" ".join(cmd), file=sys.stderr)
    processcomplete = subprocess.run(cmd)
    processcomplete.check_returncode()

def vec2bin(vec, bin, printcmd=False):
    cmd = [cfg.vec2bin, vec, bin]
    try:
        run(cmd, printcmd)
    except Exception as e:
        os.remove(bin)
        raise e

def vec2hdf5(vec, hdf5, printcmd=False):
    cmd = [cfg.vec2hdf5, vec, hdf5, "data"]
    try:
        run(cmd, printcmd)
    except Exception as e:
        os.remove(hdf5)
        raise e
        
def genGauss(nclus, dim, var, conffile, printcmd=False):
    cmd = [cfg.gaussora, nclus, dim, var, conffile]
    try:
        run(cmd, printcmd)
    except Exception as e:
        os.remove(conffile)
        raise e
    