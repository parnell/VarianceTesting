import os
import argparse
import platform

if platform.system() == 'Darwin':
    home = os.path.expanduser("~")
else:
    home = os.getenv('SCRATCH')


def args(modulename):
    a = [
        str(modulename),
        '--overwritedata',
        # '--overwriteindex',
        # '--overwritebench',
        # '--hasspatial',
        # '--haslsh',
        # '--hasms',
        '--indexes=psd,kdbq',
        # '--indexes=lcluster',
        # '--parallel',
        "--datadir", "%s/data/rdata" %home,
        "--confdir", "%s/data/rdata/conf" %home,
        "--resultdir", "%s/data/rdata/results" %home,
        '--synthetic',
        '--querying',
        '--shortname=gaussian',
        # "-i", "%s/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec" %home,
        "--query-filename=fromtopk",
        "-K1",
        "-D10",
        "--nclus=1",
        "--variance=0.1",
        '-S100000',
        '--srange=1000000',
        '--drange=10,12,14,16,18,20',
        # '--krange=1,2,3,5,10,25,50',
        '-F0',
        '--nfolds=1',
        "-Q10",
        '--lshM=512',
        '--lshL=5',
        '--lshS=100',
        '--lshI=50',
        '--lshN=8',
        '--lshT=1',
        '--lshtype=SH',
        '--mstype=mvp'
        ]
    return a

def getArgParse(args, needsquerydata=False):
    ap = argparse.ArgumentParser()
    if '--synthetic' in args:
        ap.add_argument("--nclus", type=int, required=True)
        ap.add_argument("--variance", type=float, required=True)
        ap.add_argument('-S', "--size", type=int, required=True)
        ap.add_argument('--srange')
        ap.add_argument('--drange')
        ap.add_argument('--krange')
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
        ap.add_argument("--querying", action='store_true', required=True)

    if '--hasspatial' in args:
        ap.add_argument('--hasspatial',action='store_true')

    if '--hasms' in args:
        ap.add_argument('--hasms',action='store_true')
        ap.add_argument('--mstype', required=True)

    if '--haslsh' in args:
        ap.add_argument('--haslsh',action='store_true')
        ap.add_argument('--lshtype', required=True)
        ap.add_argument('--lshM', type=int, required=True)
        ap.add_argument('--lshL', type=int, required=True)
        ap.add_argument('--lshS', type=int)
        ap.add_argument('--lshI', type=int)
        ap.add_argument('--lshN', type=int)
    if '--overwriteindex' in args:
        ap.add_argument('--overwriteindex',action='store_true')
    if '--overwritedata' in args:
        ap.add_argument('--overwritedata',action='store_true')
    if '--overwritebench' in args:
        ap.add_argument('--overwritebench',action='store_true')

    ap.add_argument('--indexes', default=None)
    ap.add_argument("--datadir", required=True)
    ap.add_argument("--confdir", required=True)
    ap.add_argument("--resultdir", required=True)
    ap.add_argument("--parallel", action='store_true')

    return ap

def getParsed(args, needsquerydata=False):
    ap = getArgParse(args, needsquerydata=needsquerydata)
    return ap.parse_known_args()

