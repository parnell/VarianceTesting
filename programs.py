import subprocess
import os
import sys
import datahelper as dh
import configuration as config
from timer import timeit
from logger import printl, printe

def run(cmd, stdout=sys.stdout, printcmd=False):
    cmd = [str(x) for x in cmd]
    if printcmd:
        printl('\n$>'," ".join(cmd)," > ",stdout.name,'\n')
    processcomplete = subprocess.run(cmd, stdout=stdout)
    try:
        processcomplete.check_returncode()
    except subprocess.CalledProcessError as e:
        printe("Error running process"," ".join(cmd)," > ",stdout.name)
        raise e

def runordel(   cmd,
                outfile,
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
            if os.path.exists(outfile):
                os.remove(outfile)
            raise e

def vec2bin(data, overwrite=True, printcmd=False):
    _vec2bin(data.vecfilepath, data.binfilepath, overwrite, printcmd)

@timeit
def _vec2bin(vecfile, binfile, overwrite=True, printcmd=False):
    cmd = [config.vec2bin, vecfile, binfile]
    runordel(cmd, binfile, overwrite=overwrite, printcmd=printcmd)

def vec2vect(data, overwrite=True, printcmd=False):
    _vec2vect(data.vecfilepath, data.vectfilepath, overwrite, printcmd)

@timeit
def _vec2vect(vecfile, vectfile, overwrite=True, printcmd=False):
    cmd = [config.vec2vect, vecfile, vectfile]
    runordel(cmd, vectfile, overwrite=overwrite, printcmd=printcmd)

def vec2hdf5(data, overwrite=True, printcmd=False):
    _vec2hdf5(data.vecfilepath, data.hdf5filepath, overwrite, printcmd)

@timeit
def _vec2hdf5(vec, hdf5, overwrite=True, printcmd=False):
    cmd = [config.vec2hdf5, vec, hdf5, "data"]
    runordel(cmd, hdf5, overwrite=overwrite, printcmd=printcmd)

@timeit
def _runlsh(
        binfilepath,
        lshindexfilepath,
        topkfilepath,
        k,
        lshtype,
        lshrfilepath,
        M=521,# Hash table size
        L = 5, #Number of hash tables
        S = 100, #Size of vectors in train
        I = 50, #Training iterations
        N = 4, #Binary code bytes
        overwrite=True,
        printcmd=False):
    cmd = [ config.lshbox,
            '-i', binfilepath,
            '-x', lshindexfilepath,
            '-b', topkfilepath,
            '-K', str(k),
            '-t', lshtype.value,
            '-M', M,
            '-L', L,
            '-S', S,
            '-I', I,
            '-N', N
          ]
    runordel(cmd, lshrfilepath,
             outtofile=True, overwrite=overwrite, printcmd=printcmd)

def runlsh(data, overwrite=True, printcmd=False):
    # Usage: ./LSHBox <input infile> <index outfile> <benchmark infile> <k>
    return _runlsh(
        data.binfilepath,
        data.lshindexfilepath,
        data.topkfilepath,
        str(data.K),
        data.cfg['lshtype'],
        data.lshrfilepath,
        data.cfg['lshM'],
        data.cfg['lshL'],
        data.cfg['lshS'],
        data.cfg['lshI'],
        data.cfg['lshN'],
        overwrite=overwrite, printcmd=printcmd
        )

def genGauss(data, overwrite=True, printcmd=False):
    cfg = data.cfg
    _genGauss(
        cfg.nclus,
        cfg.dim,
        cfg.variance,
        data,
        overwrite,
        printcmd
    )

@timeit
def _genGauss(nclus, dim, var, data, overwrite=True, printcmd=False):
    dh.Data.mkdirs(
        data.confdir,
        data.datadirfull,
        data.benchdir,
        data.indexdir)

    cmd = [ config.gaussoraconf,
            nclus,
            dim,
            var]
    runordel(
        cmd, data.gaussconffilepath,
        outtofile=True,
        overwrite=overwrite,
        printcmd=printcmd)

    cmd = [ config.gaussora,
            "-gauss", data.gaussconffilepath,
            "-n", data.S,
            "-q", "0"]
    runordel(   cmd, data.vecfilepath,
                outtofile=True,
                overwrite=overwrite,
                printcmd=printcmd)
