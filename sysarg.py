import os
import argparse

home = os.path.expanduser("~")
def args(modulename):
    a = [
        str(modulename),
        "--datadir", "%s/data/rdata" %home,
        "--confdir", "%s/data/rdata/conf" %home,
        "--resultdir", "%s/data/rdata/results" %home,
        '--odata',
        '--synthetic',
        '--querying',
        '--shortname=gaussian',
        # "-i", "%s/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec" %home,
        "--query-filename=fromtopk",
        "-K3",
        "-D2",
        "--nclus=1",
        "--variance=0.1",
        '-S100000',
        '-F0',
        '--num-folds=10',
        "-Q10"
        ]
    return a

def getArgParse(args, needsquerydata=False):
    ap = argparse.ArgumentParser()
    if '--synthetic' in args:
        ap.add_argument("--nclus", required=True)
        ap.add_argument("--variance", required=True)
        ap.add_argument('-S', "--size", required=True)
        ap.add_argument("-D", "--dimensions", type=int, required=True)
        ap.add_argument('--shortname', required=True)
        ap.add_argument('--synthetic',action='store_true',required=True)
    if needsquerydata or '--querying' in args:
        ap.add_argument("-Q", "--query-size", type=int, required=True)
        ap.add_argument("-q", "--query-filename", required=True)
        ap.add_argument('-F',"--fold", required=True)
        ap.add_argument("--num-folds", required=True)
        ap.add_argument("-K", type=int, required=True)

    ap.add_argument("--datadir", required=True)
    ap.add_argument("--confdir", required=True)
    ap.add_argument("--resultdir", required=True)

    return ap

