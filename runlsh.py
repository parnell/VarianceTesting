#!/usr/bin/env python3

import sys
import math
import copy
import traceback


import datahelper as dh
import config
from statter import LSHStatter
from analyzer import Statter
import sprinter

import sysarg
import genGauss
from programs import runordel, querylsh,buildlsh, vec2bin, vec2hdf5
from timer import timeit
from logger import printl, addLogFile

@timeit
def runkbench(data, overwrite=False):
    # Usage: ./CreateLSHBenchmark <input infile> <benchmark outfile> <k> <# queries> <query outfile>
    cmd = [ data.cfg['createLSHBenchmark'],
            data.binfilepath,
            data.topkfilepath,
            str(data.K),
            str(data.Q),
            str(data.cfg.F),
            '-V', data.qvecfilepath,
            '-M', data.qmsvecfilepath,
            '-k', str(data.K)
          ]
    runordel(cmd, data.kbenchfilepath,
             outtofile=True, overwrite=overwrite,
             printcmd=True)

def fullprocess(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):
    dh.Data.mkdirs(data.indexdir, data.querydir,
                   data.resultdir, data.confdir)
    vec2bin(data, overwritedata)
    vec2hdf5(data, overwritedata)

    bestcfg = findbest(
        data,
        overwritedata,
        overwriteindex,
        overwritebench)
    data = dh.Data(bestcfg)
    print("Best M, L " , bestcfg['lshM'], bestcfg['lshL'])
    d= process(
        data,
        overwritedata,
        overwriteindex,
        overwritebench)
    st = LSHStatter(d.getFoldedFiles('lshbenchfilepath'), d)
    sprinter.printstats(st)
    return d, st

def process(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):
    for i in range(data.cfg['nfolds']):
        data.cfg.F = i
        dh.Data.mkdirs(data.indexdir, data.querydir,
                       data.resultdir, data.confdir)
        vec2bin(data, overwritedata)
        vec2hdf5(data, overwritedata)

        runkbench(data, overwritedata) ## create data
        buildlsh(data, overwriteindex, True)
        querylsh(data, overwritebench, True)

    return data

def findbest(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):

    sq = math.sqrt(data.S)
    cfg = copy.deepcopy(data.cfg)
    bestcfg = copy.deepcopy(data.cfg)
    cfg['nfolds'] = 2
    bestcost = 0
    grid = []
    for M in [sq/8]:
        for L in [4]:
            for N in [6]:
                grid.append((M,L,N))
    for M,L,N in grid:
        try:
            cfg['lshM'] = int(M)
            cfg['lshL'] = int(L)
            cfg['lshN'] = int(N)
            print("cfg", cfg['lshM'])

            for i in range(cfg['nfolds']):
                cfg.F = i
                rundata = process(
                    dh.Data(cfg))

            st = LSHStatter(rundata.getFoldedFiles('lshbenchfilepath'), data)
            weightedcost = (st.precision+st.recall+(1-st.cost))/3
            if weightedcost > bestcost:
                bestcost = weightedcost
                bestcfg = copy.deepcopy(cfg)
        except:
            traceback.print_exc()

    bestcfg['nfolds'] = data.cfg['nfolds']
    return bestcfg


if __name__ == "__main__":
    overwritei = True
    overwrited = False
    overwriteb = True
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    ap = sysarg.getArgParse(
        sys.argv, needsquerydata=True)
    args, unknown = ap.parse_known_args()
    runcfg = config.Config(vars(args))
    rundata = dh.Data(runcfg)
    addLogFile(rundata.logfile)

    if runcfg.synthetic:
        genGauss.process(rundata, overwrited)

    rundata = fullprocess(
        rundata,
        overwritedata=overwrited,
        overwriteindex=overwritei,
        overwritebench=overwriteb)

    # printl('config', 'avgcalcs', 'meanquerytime', 'precision', 'recall', 'cost')
    files = rundata.getFoldedFiles('lshbenchfilepath')
    # print(rundata.lshbenchfilepath)
    # print(files)
    st = LSHStatter(files, rundata)
    sprinter.printstats(st)
