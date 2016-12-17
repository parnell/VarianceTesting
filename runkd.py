#!/usr/bin/env python3

import subprocess
import sys
import os
import datahelper as dh
from programs import runordel
import config
import sysarg
import analyzer as lyz
import genGauss

def process(data, overwrite=False):
    cfg = data.cfg
    dh.Data.mkdirs(data.benchdir, data.indexdir)
    data.createHDF5File()

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


if __name__ == "__main__":
    overwrite = True

    sys.argv = sysarg.args(__file__)
    ap = sysarg.getArgParse(
        sys.argv, needsquerydata=True)

    args, unknown = ap.parse_known_args()
    print(args)
    cfg = config.Config(vars(args))
    data = dh.Data(cfg)

    if cfg.synthetic:
        genGauss.process(data)

    if args.query_filename == "fromtopk":
        dh.Data.vec2hdf5(data.qvecfilepath, data.qhdf5filepath, overwrite=overwrite)
        args.query_filename = data.qhdf5filepath

    process(data)

    st1 = lyz.FileStatter(data.kdbenchfilepath)

    st1.print()

    print("avgcalcs", st1.get("avg"))
