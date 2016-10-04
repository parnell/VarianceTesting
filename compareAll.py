import subprocess
import sys
import os
import datahelper as dh
import programs as progs
import config
import analyzer as lyz
import argparse
import runlsh
import runkd


ap = argparse.ArgumentParser()
overwrite = False
sys.argv = [ "runlsh.py",
    "-i", "/Users/parnell/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec",
    "--datadir", "/Users/parnell/data",
    "-K3",
    "--query-filename=fromtopk",
    "-Q10",
    "-D2"
    ]

ap.add_argument("-D", "--dimensions", type=int, required=True)
ap.add_argument("-i", "--input-filename", required=True)
ap.add_argument("--datadir", required=True)
ap.add_argument("-K", type=int, required=True)
ap.add_argument("-Q", "--query-size", type=int, required=True)
ap.add_argument("-q", "--query-filename", required=True)

args = ap.parse_args()    
print(args)

cfg = config.Config(
    datadir=args.datadir,
    K=args.K, 
    Q=args.query_size, 
    nclus=1, 
    var=0.1, 
    size=10000, 
    D=2)
data = dh.Data(args.input_filename, cfg)

runlsh.main(data, overwrite)
runkd.main(data, overwrite)

ls = lyz.FileStatter(data.benchfilepath)
lsh = lyz.FileStatter(data.lshrfilepath)
kd = lyz.FileStatter(data.kdbenchfilepath)

print("avgcalcs", lsh.get("avg")[0], kd.get("avg")[0])    



