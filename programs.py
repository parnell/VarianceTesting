import subprocess
import os
import sys
import tempfile
import shutil

import datahelper as dh
import configuration as config
from timer import timeit
from logger import printl, printe

def run(cmd, stdout=sys.stdout, stdin=None,stderr=None, printcmd=False):
    cmd = [str(x) for x in cmd]
    if printcmd:
        printl('\n$>'," ".join(cmd)," > ",stdout.name,'\n')
    oargs = {}
    if stdin is not None: oargs = {'stdin':stdin}
    if stderr is not None: oargs = {'stderr':stderr}
    processcomplete = subprocess.run(cmd, stdout=stdout, **oargs)
    try:
        processcomplete.check_returncode()
    except subprocess.CalledProcessError as e:
        printe("Error running process"," ".join(cmd)," > ",stdout.name)
        raise e

def runordel(   cmd,
                outfiles,
                outtofile=False,
                overwrite=True,
                printcmd=False):
    allexist = True
    if isinstance(outfiles, list):
        for outfile in outfiles:
            if not os.path.exists(outfile):
                allexist = False
                break
    else:
        allexist = os.path.exists(outfiles)
        outfiles = [outfiles]
    if overwrite or not allexist:
        try:
            if outtofile:
                with open(outfiles[0],"w") as out:
                    run(cmd,
                        stdout=out,
                        printcmd=printcmd)
            else:
                run(cmd, printcmd=printcmd)
        except Exception as e:
            for of in outfiles:
                if os.path.exists(of):
                    try: os.remove(of)
                    except: pass
            raise e
        return True
    return False

def vec2msbin(data, overwrite=True, printcmd=False):
    _vec2msbin(data.vecfilepath, data.msbinfilepath, overwrite, printcmd)

@timeit
def _vec2msbin(vecfile, msbinfile, overwrite=True, printcmd=False):
    cmd = [config.vec2msbin, vecfile, msbinfile]
    runordel(cmd, msbinfile, overwrite=overwrite, printcmd=printcmd)

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
        lshbuildbenchfilepath,
        lshbenchfilepath,
        M=521,# Hash table size
        L = 5, #Number of hash tables
        S = 100, #Size of vectors in train
        I = 50, #Training iterations
        N = 4, #Binary code bytes
        query=False,
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
    if query:
        cmd.extend(['-u','1'])
        runordel(cmd, lshbenchfilepath,
                 outtofile=True, overwrite=overwrite, printcmd=printcmd)
    else: #build
        runordel(cmd, [lshbuildbenchfilepath,lshindexfilepath],
                 outtofile=True,
                 overwrite=overwrite, printcmd=printcmd)

def buildlsh(data, overwriteindex=True, printcmd=False):
    # Usage: ./LSHBox <input infile> <index outfile> <benchmark infile> <k>
    return _runlsh(
        data.binfilepath,
        data.lshindexfilepath,
        data.topkfilepath,
        str(data.K),
        data.cfg['lshtype'],
        data.lshrfilepath,
        data.lshbenchfilepath,
        data.cfg['lshM'],
        data.cfg['lshL'],
        data.cfg['lshS'],
        data.cfg['lshI'],
        data.cfg['lshN'],
        overwrite=overwriteindex, printcmd=printcmd
        )

def querylsh(data, overwritebench=True, printcmd=False):
    # Usage: ./LSHBox <input infile> <index outfile> <benchmark infile> <k>
    return _runlsh(
        data.binfilepath,
        data.lshindexfilepath,
        data.topkfilepath,
        str(data.K),
        data.cfg['lshtype'],
        data.lshrfilepath,
        data.lshbenchfilepath,
        data.cfg['lshM'],
        data.cfg['lshL'],
        data.cfg['lshS'],
        data.cfg['lshI'],
        data.cfg['lshN'],
        query=True,
        overwrite=overwritebench, printcmd=printcmd
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
