#!/usr/bin/env python3

import sys
import os
import math
import copy

import datahelper as dh
import config
from statter import LSHStatter
from analyzer import Statter, FileStatter

import sysarg
import genGauss
from programs import runordel, runlsh, vec2bin, vec2hdf5
from timer import timeit
from logger import printl, addLogFile

@timeit
def runlshbench(data, overwrite=False):
    # Usage: ./CreateLSHBenchmark <input infile> <benchmark outfile> <k> <# queries> <query outfile>
    cmd = [ data.cfg['createLSHBenchmark'],
            data.binfilepath,
            data.topkfilepath,
            str(data.K),
            str(data.Q),
            data.qvecfilepath
          ]
    runordel(cmd, data.lshbenchfilepath,
             outtofile=True, overwrite=overwrite,
             printcmd=True)

def fullprocess(
        data,
        overwritedata=False,
        overwritebench=False,
        overwrite=False):
    dh.Data.mkdirs(data.indexdir, data.querydir,
                   data.resultdir, data.confdir)
    vec2bin(data, overwritedata)
    vec2hdf5(data, overwritedata)

    bestcfg = findbest(data)
    data = dh.Data(bestcfg)
    print("Best M, L " , bestcfg['lshM'], bestcfg['lshL'])
    return process(
        data,
        overwritedata,
        overwritebench,
        overwrite)

def process(
        data,
        overwritedata=False,
        overwritebench=False,
        overwrite=False):
    for i in range(data.cfg['nfolds']):
        data.cfg.F = i
        dh.Data.mkdirs(data.indexdir, data.querydir,
                       data.resultdir, data.confdir)
        vec2bin(data, overwritedata)
        vec2hdf5(data, overwritedata)

        runlshbench(data, overwritebench)
        runlsh(data, overwrite, True)

    return data

def findbest(
        data,
        overwritedata=False,
        overwritebench=False,
        overwrite=False):
    overwritedata=False
    overwritebench=False
    overwrite=False

    final = []
    sq = math.sqrt(data.S)
    cfg = copy.deepcopy(data.cfg)
    bestcfg = copy.deepcopy(data.cfg)
    cfg['nfolds'] = 1
    bestcost = 0
    for M in [sq*2, sq, sq/2, sq/4, sq/8]:
        cfg['lshM'] = int(M)
        for L in [4,8,16]:
            cfg['lshL'] = int(L)
            rundata = dh.Data(cfg)
            for i in range(cfg['nfolds']):
                rundata.cfg.F = i
                process(
                    rundata,
                    overwritedata=overwritedata,
                    overwritebench=overwritebench,
                    overwrite=overwrite)

            # st = FileStatter(rundata.getFoldedFiles('lshrfilepath'))
            # st.print()
            if len(final) == 0:
                a = ['config', 'avgcalcs',
                     'meanquerytime', 'precision',
                     'recall','cost', 'weightedpoints']
                final.append(a)
                printl(*a)
            st2 = LSHStatter(rundata.getFoldedFiles('lshrfilepath'))
            prec = st2.get('PRECISION', Statter.mean)
            recall = st2.get('RECALL',Statter.mean)
            cost = st2.get('COST',Statter.mean)
            weightedcost = (prec+recall+(1-cost))/3
            a = [
                rundata.lshfullname,
                st2.average,
                st2.get('meanquerytime', Statter.mean),
                prec,
                recall,
                cost,
                weightedcost]
            final.append(a)
            printl(*a)
            if weightedcost > bestcost:
                bestcost = weightedcost
                bestcfg = copy.deepcopy(cfg)

    for line in final:
        print("\t".join([ str(s) for s in line]))
    bestcfg['nfolds'] = data.cfg['nfolds']
    return bestcfg


if __name__ == "__main__":
    overwrite = False
    overwritedata = False
    overwritebench = False
    home = os.path.expanduser("~")
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    ap = sysarg.getArgParse(
        sys.argv, needsquerydata=True)

    args, unknown = ap.parse_known_args()
    runcfg = config.Config(vars(args))
    rundata = dh.Data(runcfg)
    addLogFile(rundata.logfile)

    if runcfg.synthetic:
        genGauss.process(rundata, overwritebench)

    # newcfg = findbest(rundata)
    # rundata = dh.Data(newcfg)
    # print("Best M, L " , newcfg['lshM'], newcfg['lshL'])
    rundata = fullprocess(
        rundata,
        overwritedata=overwritedata,
        overwritebench=overwritebench,
        overwrite=overwrite)

    printl('config', 'avgcalcs', 'meanquerytime', 'precision', 'recall', 'cost')
    files = rundata.getFoldedFiles('lshrfilepath')
    st2 = LSHStatter(files)
    printl(
        rundata.lshfullname,
        st2.average,
        st2.get('meanquerytime', Statter.mean),
        st2.get('PRECISION', Statter.mean),
        st2.get('RECALL',Statter.mean),
        st2.get('COST',Statter.mean))
