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
from logger import printl

def fullprocess(data, overwrite=False):
    gendata(data, overwrite)
    process(data, overwrite)

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

def gendata(data,overwrite=False):
    dh.Data.mkdirs(data.benchdir, data.indexdir)
    vec2hdf5(data, overwrite=overwrite)
    if data.cfg.synthetic:
        genGauss.process(data)

    _vec2hdf5(data.qvecfilepath, data.qhdf5filepath, overwrite=overwrite)


if __name__ == "__main__":
    overwrite = True
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)

    args, unknown = sysarg.getParsed(sys.argv, True)
    print(args)
    cfg = config.Config(vars(args))
    data = dh.Data(cfg)
    fullprocess(data, overwrite)
    st1 = lyz.FileStatter(data.kdbenchfilepath)


    printl("avgcalcs", st1.getf("avg"))
