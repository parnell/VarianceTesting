import os
import argparse

home = os.path.expanduser("~")
# def args(modulename):
#     a = [
#         str(modulename),
#         "--datadir", "%s/data/rdata" %home,
#         "--confdir", "%s/data/rdata/conf" %home,
#         "--resultdir", "%s/data/rdata/results" %home,
#         '--odata',"%s/data/rdata/audio.vec" %home,
#         '--querying',
#         '--shortname=audio',
#         # "-i", "%s/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec" %home,
#         "--query-filename=fromtopk",
#         "-K3",
#         '-F0',
#         '--nfolds=1',
#         "-Q100",
#         '--haslsh',
#         '--lshM=512',
#         '--lshL=5',
#         '--lshS=100',
#         '--lshI=50',
#         '--lshN=6',
#         '--lshT=1',
#         '--lshtype=SH',
#         ]
#     return a

def args(modulename):
    a = [
        str(modulename),
        "--datadir", "%s/data/rdata" %home,
        "--confdir", "%s/data/rdata/conf" %home,
        "--resultdir", "%s/data/rdata/results" %home,
        '--synthetic',
        '--querying',
        '--shortname=gaussian',
        # "-i", "%s/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec" %home,
        "--query-filename=fromtopk",
        "-K3",
        "-D10",
        "--nclus=1",
        "--variance=0.1",
        '-S10000',
        '-F0',
        '--nfolds=1',
        "-Q100",
        '--haslsh',
        '--lshM=512',
        '--lshL=5',
        '--lshS=100',
        '--lshI=50',
        '--lshN=6',
        '--lshT=1',
        '--lshtype=SH',
        ]
    return a

def getArgParse(args, needsquerydata=False):
    ap = argparse.ArgumentParser()
    if '--synthetic' in args:
        ap.add_argument("--nclus", type=int, required=True)
        ap.add_argument("--variance", type=float, required=True)
        ap.add_argument('-S', "--size", type=int, required=True)
        ap.add_argument("-D", "--dimensions", type=int, required=True)
        ap.add_argument('--shortname', required=True)
        ap.add_argument('--synthetic',action='store_true',required=True)
    else:
        ap.add_argument('--odata', required=True)
        ap.add_argument('--shortname', required=True)

    if needsquerydata or '--querying' in args:
        ap.add_argument("-Q", "--query-size", type=int, required=True)
        ap.add_argument("-q", "--query-filename", required=True)
        ap.add_argument('-F',"--fold", type=int, required=True)
        ap.add_argument("--nfolds", type=int, required=True)
        ap.add_argument("-K", type=int, required=True)
    if '--haslsh' in args:
        ap.add_argument('--lshtype', required=True)
        ap.add_argument('--lshM', type=int, required=True)
        ap.add_argument('--lshL', type=int, required=True)
        ap.add_argument('--lshS', type=int)
        ap.add_argument('--lshI', type=int)
        ap.add_argument('--lshN', type=int)
    ap.add_argument("--datadir", required=True)
    ap.add_argument("--confdir", required=True)
    ap.add_argument("--resultdir", required=True)

    return ap

def getParsed(args, needsquerydata=False):
    ap = getArgParse(args, needsquerydata=needsquerydata)
    return ap.parse_known_args()


