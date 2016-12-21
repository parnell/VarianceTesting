#!/usr/bin/env python3

###
# Author: Lee Parnell Thompson
# Version: 1.1
#
# Disclaimer: I use these scripts for my own use,
#	so caveat progtor, let the programmer beware
###

import sys
import config
import datahelper as dh
import programs as prog
import sysarg
from logger import addLogFile

overwrite = True
#def usage(out):
	#print("Usage: ./genGaussData.py <nclusters>
    # <dimensions> <variance> <size>
    #<indexName for hdf5> <numQueryFiles>
    # <sizeOfQueryFiles>", file=sys.stderr)

def process(data, overwrite=False):

    prog.genGauss(data,overwrite=overwrite,printcmd=True)
    prog.vec2bin(data, overwrite,printcmd=True)
    prog.vec2hdf5(data, overwrite,printcmd=True)
    prog.vec2vect(data, overwrite, printcmd=True)

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

if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)

    args, unknown = sysarg.getParsed(sys.argv)

    cfg = config.Config(vars(args))
    data = dh.Data(cfg)
    addLogFile(data.logfile)

    process(data)
