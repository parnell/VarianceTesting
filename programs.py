import subprocess
import configuration as cfg
import os
def run(cmd, printcmd=False):
    if printcmd:
        print(" ".join(cmd))
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
        

