import os

home = os.path.expanduser("~")
def args(modulename):
    a = [
        modulename,
        '--odata',
        '--synthetic',
        # "-i", "%s/data/gaussian__nclus=1_dim=2_var=0.1_size=10000.vec" %home,
        "--datadir", "%s/rdata" %home,
        "--confdir", "%s/rdata/conf" %home,
        "--resultdir", "%s/rdata/results" %home,
        "--query-filename=fromtopk",
        "-K3",
        "-D2",
        "--nclus=1",
        "--variance=0.1",
        '-S10000',
        '-F0',
        "-Q10"
        ]
    return a
