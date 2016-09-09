import subprocess
import configuration as cfg

def run(cmd, printcmd=False):
    if printcmd:
        print(" ".join(cmd))
    processcomplete = subprocess.run(cmd)
    processcomplete.check_returncode()

def vec2bin(vec, bin):
    cmd = [cfg.vec2bin, vec, bin]
    run(cmd)
