import sys
import traceback
from functools import partial

import sysarg
from formdecorator import FailFree
from mapper import pmap
import numpy as np
import datahelper as dh
import config
import runlsh
import runkd
import runsisap
import genGauss
from logger import printl, addLogFile, stacktrace
from sprinter import printstats

np.set_printoptions(precision=4)

@FailFree
def runLSH(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):

    ### Running LSH
    statters = []
    printl("@@@@@@@@ Running LSH @@@@@@@@")
    for lshtype in dh.LSHTypeEnum.getValidTypes():
        printl("------- Running LSH {} -------".format(lshtype.name))
        data.cfg['lshtype'] = lshtype
        nd = dh.Data(data.cfg)
        try:
            data, st = runlsh.fullprocess(
                nd,
                overwritedata,
                overwriteindex,
                overwritebench)
            statters.append(st)

        except Exception as e:
            traceback.print_exc()
            stacktrace("LSH Problem")
            printl("Error running ", lshtype, " ", str(e))
    return data, statters

@FailFree
def runSisap(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):
    ### Running Sisap
    statters = []
    printl("@@@@@@@@ Running SISAP @@@@@@@@")
    for mstype in dh.MSTypeEnum.getValidTypes():
        printl("------- Running Sisap {} -------".format(mstype.name))
        data.cfg['mstype'] = mstype
        nd = dh.Data(data.cfg)
        try:
            st =runsisap.fullprocess(
                nd,
                overwritedata,
                overwriteindex,
                overwritebench)
            statters.append(st)
        except Exception as e:
            traceback.print_exc()
            stacktrace("Sisap Problem")
            printl("Error running ", mstype, " ", str(e))
    return statters

@FailFree
def runKD(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):

    printl("@@@@ Running KD @@@@")
    return [runkd.fullprocess(
        data,
        overwritedata,
        overwritebench)]

@FailFree
def gendata(SD, data):
    cfg = data.cfg
    cfg.K = SD[0]
    cfg.S = SD[1]
    cfg.D = SD[2]
    data = dh.Data(cfg)
    addLogFile(data.logfile)

    if cfg['synthetic']:
        genGauss.process(data)

@FailFree
def process(SD, data):
    cfg = data.cfg
    overwriteindex = 'overwriteindex' in cfg
    overwritedata = 'overwritedata' in cfg
    overwritebench = 'overwritebench' in cfg

    cfg.K = SD[0]
    cfg.S = SD[1]
    cfg.D = SD[2]
    data = dh.Data(cfg)
    sts = []
    if 'haslsh' in cfg:
        data, ss = runLSH(data, overwriteindex, overwritedata, overwritebench)
        sts.append(ss)
    if cfg.D <= 100 and 'haskd' in cfg:
        sts.append(runKD(data, overwriteindex, overwritedata, overwritebench))
    if 'hasms' in cfg:
        sts.append(runSisap(data, overwriteindex, overwritedata, overwritebench))
    statters = []
    for ss in sts:
        if ss is None or isinstance(ss, Exception):
            continue
        statters.extend(ss)
    return statters

if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    overwritei = '--overwriteindex' in sys.argv
    overwrited = '--overwritedata' in sys.argv
    overwriteb = '--overwritebench' in sys.argv

    args, unknown = sysarg.getParsed(sys.argv, True)
    print(args)
    cfg = config.Config(vars(args))

    printl('-#--------------------------------------#-')
    printl(cfg)
    final = []
    if 'srange' in cfg and cfg['srange']:
        Ss = [int(x) for x in cfg['srange'].split(',')]
    else :
        Ss = [cfg.S]
    if 'drange' in cfg and cfg['drange']:
        Ds = [int(x) for x in cfg['drange'].split(',')]
    else :
        Ds = [cfg.D]
    if 'krange' in cfg and cfg['krange']:
        Ks = [int(x) for x in cfg['krange'].split(',')]
    else :
        Ks = [cfg.K]
    SD = []
    for K in Ks:
        for S in Ss:
            for D in Ds:
                SD.append((K,S,D))

    data = dh.Data(cfg)
    dh.Data.mkdirs(data.benchdir, data.confdir, data.indexdir, data.querydir)
    pmap(
        partial(gendata, data=data), SD, cfg['parallel']
    )

    results = pmap(
        partial(process, data=data), SD, cfg['parallel']
    )

    printl('FinishedStats')
    for r in results:
        if r is None or isinstance(r, Exception):
            continue
        printstats(r)
