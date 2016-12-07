#!/usr/bin/env python3

import subprocess
import sys
import os
import argparse

import datahelper as dh
import config
import analyzer as lyz
import logging as log
import sysarg

def main(data, overwrite=False):
    cfg = data.cfg

    dh.Data.mkdirs(data.indexdir, data.querydir,
                   data.resultdir, data.confdir)
    data.createBinFile()
    data.createHDF5File()

    # Usage: ./CreateLSHBenchmark <input infile> <benchmark outfile> <k> <# queries>
    cmd = [ cfg['createLSHBenchmark'],
            data.binfilepath,
            data.topkfilepath,
            str(data.K),
            str(data.Q)
          ]

    if overwrite or not os.path.exists(data.benchfilepath):
        with open(data.benchfilepath, "w") as of:
            pc = subprocess.run(cmd, stdout=of)
            if pc.returncode != 0:
                dh.Data.remove(data.benchfilepath)

    # Usage: ./LSHBox <input infile> <index outfile> <benchmark infile> <k>
    cmd = [ cfg['lshbox'],
            data.binfilepath,
            data.lshindexfilepath,
            data.topkfilepath,
            str(data.K),
            data.qvecfilepath,
          ]

    if overwrite or not os.path.exists(data.lshrfilepath):
        log.debug(" ".join(cmd))
        with open(data.lshrfilepath, "w") as of:
            pc = subprocess.run(cmd, stdout=of)
            if pc.returncode != 0:
                dh.Data.remove(data.lshrfilepath)

    return data

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    overwrite = True
    home = os.path.expanduser("~")

    sys.argv = sysarg.args
    ap.add_argument("-i", "--input-filename", required=True)
    ap.add_argument("--datadir", required=True)
    ap.add_argument("--confdir", required=True)
    ap.add_argument("--resultdir", required=True)
    ap.add_argument("-S",'--size', type=int, required=True)
    ap.add_argument("-K", type=int, required=True)
    ap.add_argument("-F",'--fold', type=int, required=True)
    ap.add_argument("-Q", "--query-size", type=int, required=True)

    args = ap.parse_args()
    print(args)

    runcfg = config.Config(
        datadir=args.datadir,
        confdir=args.confdir,
        resultdir=args.resultdir,
        K=args.K,
        Q=args.query_size,
        S=args.size,
        nclus=1,
        var=0.1,
        size=10000,
        F=args.fold,
        D=2)
    rundata = dh.Data(args.input_filename, runcfg)

    main(rundata, overwrite=overwrite)

    st1 = lyz.FileStatter(rundata.benchfilepath)
    st2 = lyz.FileStatter(rundata.lshrfilepath)
    # st1.print()
    # st2.print()
    print("avgcalcs", st2.get("avg")[0])
