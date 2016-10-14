import subprocess
import configuration as cfg
import os
import sys
import datahelper as dh

def run(cmd, stdout=sys.stdout, printcmd=False):
    cmd = [str(x) for x in cmd]
    if printcmd:
        print(" ".join(cmd)," > ",stdout.name, file=sys.stderr)
    processcomplete = subprocess.run(cmd, stdout=stdout)
    processcomplete.check_returncode()


def vec2bin(vec, bin, overwrite=True, printcmd=False):
    cmd = [cfg.vec2bin, vec, bin]
    runordel(cmd, bin, overwrite=overwrite, printcmd=printcmd)

def vec2vect(vec, bin, overwrite=True,printcmd=False):
    pass

def vec2hdf5(vec, hdf5, overwrite=True, printcmd=False):
    cmd = [cfg.vec2hdf5, vec, hdf5, "data"]
    runordel(cmd, hdf5, overwrite=overwrite, printcmd=printcmd)

def runordel(cmd, outfile, 
    outtofile=False, 
    overwrite=True,
    printcmd=False):
    if overwrite or not os.path.exists(outfile):
        try:
            if outtofile:
                with open(outfile,"w") as out:
                    run(cmd, stdout=out, printcmd=printcmd)
            else:
                run(cmd, printcmd=printcmd)
        except Exception as e:
            if os.path.exists(outfile): os.remove(outfile)
            raise e
    
def genGauss(nclus, dim, var, data, overwrite=True, printcmd=False):
    dh.Data.mkdirs(data.datadirfull, data.benchdir, data.indexdir)
    
    cmd = [cfg.gaussoraconf, 
        nclus, 
        dim, 
        var]
    runordel(cmd, data.gaussconffilepath, 
        outtofile=True, 
        overwrite=overwrite, 
        printcmd=printcmd)

    cmd = [cfg.gaussora, 
        "-gauss", data.gaussconffilepath,
        "-n", data.S,
        "-q", "0"]
    runordel(cmd, data.vecfilepath,
        outtofile=True,
        overwrite=overwrite, 
        printcmd=printcmd)
    