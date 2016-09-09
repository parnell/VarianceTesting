#!/usr/bin/env python3

import subprocess
import sys
import os
import datahelper as dh
import programs as progs
import config

overwrite = False
sys.argv = [ "runlsh.py",
    "/Users/parnell/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec",
    "/Users/parnell/data",
    "3",
    "10"]
print(" ".join(sys.argv))

if len(sys.argv) < 4:
    print("./prog <infile vec> <data directory> <outfile benchmark> <k> <Q>")
    sys.exit(1)

binfile = sys.argv[1]
datadir = sys.argv[2]
K = int(sys.argv[3])
Q = int(sys.argv[4])

cfg = config.Config(datadir=datadir, K=K, Q=Q, nclus=1, var=0.1, size=10000, D=2)
data = dh.Data(binfile, cfg)

data.mkdirs(data.benchdir, data.indexdir)
data.createBinFile()

# Usage: ./CreateLSHBenchmark <input infile> <benchmark outfile> <k> <# queries>
cmd = [cfg['createLSHBenchmark'], 
    data.binfilepath,
    data.topkfilepath, 
    str(data.K), 
    str(data.Q)
    ]

if overwrite or not os.path.exists(data.benchfilepath):
    with open(data.benchfilepath, "w") as of:
        retcode = subprocess.run(cmd, stdout=of)


# Usage: ./LSHBox <input infile> <index outfile> <benchmark infile> <k>
cmd = [cfg['lshbox'], 
    data.binfilepath,
    data.lshindexfilepath, 
    data.topkfilepath,
    str(data.K) 
    ]

if overwrite or not os.path.exists(data.lshrfilepath):
    print(" ".join(cmd))
    with open(data.lshrfilepath, "w") as of:
        subprocess.run(cmd, stdout=of)


# for l in open(data.benchfile):
#     print(l)
