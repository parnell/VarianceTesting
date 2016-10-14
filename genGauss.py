#!/usr/bin/env python3

###
# Author: Lee Parnell Thompson
# Version: 1.1
# 
# Disclaimer: I use these scripts for my own use, 
#	so caveat progtor, let the programmer beware
###

import sys,os,re,getopt
from subprocess import *
import argparse
import config
import datahelper as dh
import programs as prog

overwrite = True
#def usage(out):
	#print("Usage: ./genGaussData.py <nclusters>
    # <dimensions> <variance> <size> 
    #<indexName for hdf5> <numQueryFiles>
    # <sizeOfQueryFiles>", file=sys.stderr)
home = os.path.expanduser("~")
sys.argv = [ "VarianceTesting",
    "-K3",
    "--datadir", "%s/rdata" %home,
    "--confdir", "%s/rdata/conf" %home,
    "--resultdir", "%s/rdata/results" %home,
    "--query-filename=fromtopk",
    "-D2",
    "--nclus=1",
    "--variance=0.1",
    "--fold=1",
    "--data-size=10000",
    "-Q10"
    # "--input-filename="
    #"10"
    ]


# print(" ".join(sys.argv))
ap = argparse.ArgumentParser()

ap.add_argument("--nclus", required=True)
ap.add_argument("--variance", required=True)
ap.add_argument("--fold", required=True)
ap.add_argument("--data-size", required=True)
ap.add_argument("-K", type=int, required=True)
ap.add_argument("-D", "--dimensions", type=int, required=True)
ap.add_argument("-Q", "--query-size", type=int, required=True)
ap.add_argument("-q", "--query-filename", required=True)
ap.add_argument("--datadir", required=True)
ap.add_argument("--confdir", required=True)
ap.add_argument("--resultdir", required=True)


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
    S=10000, 
    D=2,
    F=0)
data = dh.Data("gaussian", cfg)

nclus = args.nclus    # numero de clusters
dim =   args.dimensions    # la dimension de los vectores
var =   args.variance    # la varianza (devstd^2)
size = args.data_size
# hdf5IndexName = sys.argv[-3]
nQueryFiles = args.fold
sizeQueryFiles = args.query_size

confDir = data.confdir
dataDir = data.datadir
queryPath = data.querydir


prog.genGauss(
    nclus=args.nclus, 
    dim=args.dimensions,
    var=args.variance,
    data=data,
    overwrite=overwrite,
    printcmd=True
    )



prog.vec2bin(data.vecfilepath, data.binfilepath, overwrite)
prog.vec2hdf5(data.vecfilepath, data.hdf5filepath, overwrite)

# confName = "gaussoraConfig_nclus=%d_dim=%d_var=%s.txt" %(nclus,dim,var)
gcprog = "gaussoraConf.pl"
# confFile = "%s/%s" %(confDir,confName)

gprog = "gaussora"
# dataName = "gaussian_nclus=%d_dim=%d_var=%s_size=%d.vec" %(nclus,dim,var,size)
# dataFile = "%s/%s" %(dataDir,dataName)

# dataName2 = "gaussian_nclus=%d_dim=%d_var=%s_size=%d.vect" %(nclus,dim,var,size)
# dataFile2 = "%s/%s" %(dataDir,dataName2)

# convertProg1 = "vec2hdf5"
# hdf5Name = "gaussian_nclus=%d_dim=%d_var=%s_size=%d.hdf5" %(nclus,dim,var,size)
# hdf5File = "%s/%s" %(dataDir,hdf5Name)

# convertProg2 = "vec2bin"
# vbinName = "gaussian_nclus=%d_dim=%d_var=%s_size=%d.lbin" %(nclus,dim,var,size)
# vbinFile = "%s/%s" %(dataDir,vbinName)

createQueryProy = "createQueries"

# if overwrite or not os.path.exists(data.gaussconfpath):
#     cmdstr = "%s %d %d %s > %s" %(gcprog,nclus,dim,var,confFile)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)

# if not os.path.exists(dataFile):
#     cmdstr = "%s -gauss %s -n %d -q 0 > %s" %(gprog,confFile, size, dataFile)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)

# if not os.path.exists(dataFile2):
#     cmdstr = 'tail -n +2 "%s" > "%s"' %(dataFile, dataFile2)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)

# if not os.path.exists(hdf5File):
#     cmdstr = "%s %s %s %s" %(convertProg1, dataFile, hdf5File, hdf5IndexName)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)

# if not os.path.exists(vbinFile):
#     cmdstr = "%s %s %s" %(convertProg2, dataFile, vbinFile)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)

# print("queryPath=%s" %queryPath)
# if not os.path.exists(queryPath):
#     os.mkdir(queryPath)

# for i in range(1,nQueryFiles+1):
#     # "./createQueries <infile> <outfile> <indexName> <querySize> <vec|hdf5> [seed]\n"
#     queryFileBase = "gaussian-query-%d_nclus=%d_dim=%d_var=%s_size=%d" %(i,nclus,dim,var,size)
#     qvec = "%s/%s.vec" %(queryPath,queryFileBase)
#     qvec2 = "%s/%s.vect" %(queryPath,queryFileBase)
#     h5vec = "%s/%s.hdf5" %(queryPath,queryFileBase)
    
#     cmdstr = "%s %s %s %s %s %s %d" %(createQueryProy, hdf5File, qvec, hdf5IndexName, sizeQueryFiles, "vec", i)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)

#     cmdstr = 'tail -n +2 "%s" > "%s"' %(qvec, qvec2)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)
    
#     cmdstr = "%s %s %s %s %s %s %d" %(createQueryProy, hdf5File, h5vec, hdf5IndexName, sizeQueryFiles, "hdf5", i)
#     print(cmdstr)
#     retcode = call(cmdstr, shell=True)
