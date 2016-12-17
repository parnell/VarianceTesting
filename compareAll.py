import sys
import os
import argparse

import datahelper as dh
import config
import analyzer as lyz
import runlsh
import runkd

home = os.path.expanduser("~")
ap = argparse.ArgumentParser()
overwrite = True
sys.argv = [
    "runlsh.py",
    "-i", "%s/r/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec" %home,
    "--datadir", "%s/r/data" %home,
    "--confdir", "%s/r/data/conf" %home,
    "--resultdir", "%s/r/data/results" %home,
    "-K3",
    "--query-filename=fromtopk",
    "-Q10",
    "-D2"
    ]

ap.add_argument("-D", "--dimensions", type=int, required=True)
ap.add_argument("-i", "--input-filename", required=True)
ap.add_argument("--datadir", required=True)
ap.add_argument("--confdir", required=True)
ap.add_argument("--resultdir", required=True)
ap.add_argument("-K", type=int, required=True)
ap.add_argument("-Q", "--query-size", type=int, required=True)
ap.add_argument("-q", "--query-filename", required=True)

args = ap.parse_args()
print(args)

cfg = config.Config(
    datadir=args.datadir,
    confdir=args.confdir,
    resultdir=args.resultdir,
    K=args.K,
    Q=args.query_size,
    nclus=1,
    var=0.1,
    size=10000,
    D=2,
    F=0)
data = dh.Data(args.input_filename, cfg)

print("@@@@ Running LSH @@@@")
runlsh.main(data, overwrite)
print("@@@@ Running KD @@@@")
runkd.main(data, overwrite)

# N0692-ZY350-78988-0XAK6-992NN
ls = lyz.FileStatter(data.lshbenchfilepath)
lsh = lyz.FileStatter(data.lshrfilepath)
kd = lyz.FileStatter(data.kdbenchfilepath)
ls.print()
print("############")
lsh.print()
print("############")
kd.print()
print("avgtime", ls.getf("totaltime"), lsh.getf("meanquerytime"), kd.getf("avgquerytime"),sep="\t")
print("avgcalcs", "-", lsh.getf("avg"), kd.getf("avg"), sep="\t")
