#!/usr/bin/env python3

import subprocess
import sys
import os

import datahelper as dh
import config
import analyzer as lyz
import sysarg
import genGauss
from programs import runordel, runlsh, vec2bin, vec2hdf5
from timer import timeit
from logger import printl

@timeit
def runlshbench(data, overwrite=False):
    # Usage: ./CreateLSHBenchmark <input infile> <benchmark outfile> <k> <# queries>
    cmd = [ data.cfg['createLSHBenchmark'],
            data.binfilepath,
            data.topkfilepath,
            str(data.K),
            str(data.Q)
          ]
    runordel(cmd, data.lshbenchfilepath,
             outtofile=True, overwrite=overwrite,
             printcmd=True)

def process(data, overwrite=False):
    dh.Data.mkdirs(data.indexdir, data.querydir,
                   data.resultdir, data.confdir)
    vec2bin(data, overwrite)
    vec2hdf5(data, overwrite)

    runlshbench(data, overwrite)
    runlsh(data, overwrite, True)

    return data

if __name__ == "__main__":
    overwrite = False
    home = os.path.expanduser("~")

    sys.argv = sysarg.args(__file__)
    ap = sysarg.getArgParse(
        sys.argv, needsquerydata=True)

    args, unknown = ap.parse_known_args()

    runcfg = config.Config(vars(args))
    rundata = dh.Data(runcfg)

    if runcfg.synthetic:
        genGauss.process(rundata)

    process(rundata, overwrite=overwrite)

    st1 = lyz.FileStatter(rundata.lshbenchfilepath)
    st2 = lyz.FileStatter(rundata.lshrfilepath)
    st1.print()
    st2.print()
    printl("avgcalcs", st2.getf("avg"))
