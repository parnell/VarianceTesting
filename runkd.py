#!/usr/bin/env python3

import subprocess
import sys
import os
import datahelper as dh
import programs as progs
import config
import argparse
import analyzer as lyz
import logging as log


def main(data, overwrite=False):
    cfg = data.cfg
    dh.Data.mkdirs(data.benchdir, data.indexdir)
    data.createHDF5File()

    #VarianceTesting -q/filename/ -k3 -d5 -i/Users/parnell/workspace/data/gaussian_1_5_0.1_1000000.hdf5 -ngauss -f1
    cmd = [cfg['kdtree'], 
        "-i%s" %data.hdf5filepath,
        "-ndata", 
        "-k3",
        "-q%s" %data.qhdf5filepath
        ]
    log.debug(" ".join(cmd))
    if overwrite or not os.path.exists(data.kdbenchfilepath):
        with open(data.kdbenchfilepath, "w") as of:
            pc = subprocess.run(cmd, stdout=of)
            if pc.returncode != 0:
                dh.Data.remove(data.kdbenchfilepath)

    # lyz.Analyzer(data)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    overwrite = True
    #parms, type=%s, dim=%d, nclusters=%d, size=%d, knn=%d, radius=%f, filename=%s, qfilename=%s
    # example:  -k3 -d5 -i/Users/parnell/workspace/data/gaussian_1_5_0.1_1000000.hdf5 -ngauss -f1
    sys.argv = [ "VarianceTesting",
        "-K3",
        "-i","/Users/parnell/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec",
        "--datadir", "/Users/parnell/data",
        "--confdir", "/Users/parnell/data/conf",
        "--resultdir", "/Users/parnell/data/results",
        "--query-filename=fromtopk",
        "-D2",
        "-Q10"
        # "--input-filename="
        #"10"
        ]
    print(" ".join(sys.argv))


    ap.add_argument("-K", type=int, required=True)
    ap.add_argument("-D", "--dimensions", type=int, required=True)
    ap.add_argument("-q", "--query-filename", required=True)
    ap.add_argument("-i", "--input-filename", required=True)
    ap.add_argument("--datadir", required=True)
    ap.add_argument("--confdir", required=True)
    ap.add_argument("--resultdir", required=True)
    ap.add_argument("-Q", "--query-size", type=int, required=True)


    args = ap.parse_args()
    print(args)

    # if len(sys.argv) < 4:
    #     print("./prog <infile vec> <data directory> <outfile benchmark> <k> <Q>")
    #     sys.exit(1)


    # binfile = sys.argv[1]
    # datadir = sys.argv[2]
    # K = int(sys.argv[3])
    # Q = int(sys.argv[4])

    cfg = config.Config(datadir=args.datadir, 
        confdir=args.confdir,
        resultdir=args.resultdir,
        K=args.K, 
        Q=args.query_size, 
        nclus=1, 
        var=0.1, 
        size=10000, 
        D=args.dimensions)
    data = dh.Data(args.input_filename, cfg)

    if args.query_filename == "fromtopk":
        dh.Data.vec2hdf5(data.qvecfilepath, data.qhdf5filepath, overwrite=overwrite)
        args.query_filename = data.qhdf5filepath

    main(data)

    st1 = lyz.FileStatter(data.kdbenchfilepath)

    # st1.print()

    log.info("avgcalcs", st1.get("avg")[0])
