#!/usr/bin/env python3

import subprocess
import sys
import os
import datahelper as dh
from programs import runordel, vec2hdf5, _vec2hdf5
import config
import sysarg
import analyzer as lyz
import genGauss
from logger import printl, addLogFile
import copy
from statter import KDStatter
import sprinter

def fullprocess(data, overwritedata=False, overwritebench=False):
    gendata(data, overwritedata)
    process(data, overwritebench)
    st = KDStatter(data.getFoldedFiles('kdbenchfilepath'),data)
    sprinter.printstats(st)
    return st

def process(data, overwrite=False):
    cfg = data.cfg

    #VarianceTesting -q/filename/ -k3 -d5 -i/data/gaussian_1_5_0.1_1000000.hdf5 -ngauss -f1
    cmd = [
        cfg['kdtree'],
        "-i%s" %data.hdf5filepath,
        "-ndata",
        "-k3",
        "-q%s" %data.qhdf5filepath
        ]
    runordel(cmd, data.kdbenchfilepath,
             outtofile=True, overwrite=overwrite,
             printcmd=True)

def gendata(data, overwrite=False):
    dh.Data.mkdirs(data.benchdir,data.confdir, data.indexdir, data.querydir)
    vec2hdf5(data, overwrite=overwrite)
    if data.cfg.synthetic:
        genGauss.process(data, overwrite)

    _vec2hdf5(
        data.qvecfilepath, data.qhdf5filepath,
        overwrite=overwrite, printcmd=True)

if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    overwrited = '--overwritedata' in sys.argv
    overwritei = '--overwriteindex' in sys.argv
    overwriteb = '--overwritebench' in sys.argv

    args, unknown = sysarg.getParsed(sys.argv, True)
    print(args)
    cfg = config.Config(vars(args))
    ocfg = copy.deepcopy(cfg)
    data = dh.Data(cfg)
    addLogFile(data.logfile)

    fullprocess(data, overwrited, overwriteb)
