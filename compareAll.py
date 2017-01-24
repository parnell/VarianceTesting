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
import dataenums

np.set_printoptions(precision=4)

@FailFree
def gendata(SD, data):
    cfg = data.cfg
    __ = SD[0]
    cfg.K = SD[1]
    cfg.S = SD[2]
    cfg.D = SD[3]
    data = dh.Data(cfg)
    addLogFile(data.logfile)

    overwritedata = 'overwritedata' in cfg
    if cfg['synthetic']:
        genGauss.process(data, overwritedata)

@FailFree
def process(SD, data):
    cfg = data.cfg
    overwritedata = 'overwritedata' in cfg
    overwriteindex = 'overwriteindex' in cfg
    overwritebench = 'overwritebench' in cfg
    algorithm = SD[0]
    cfg.K = SD[1]
    cfg.S = SD[2]
    cfg.D = SD[3]
    st = None
    if isinstance(algorithm, dataenums.MSTypeEnum):
        cfg['mstype'] = algorithm
        st = runsisap.fullprocess(
            dh.Data(cfg),
            overwritedata,
            overwriteindex,
            overwritebench)
    elif isinstance(algorithm, dataenums.LSHTypeEnum):
        cfg['lshtype'] = algorithm
        data, st = runlsh.fullprocess(
            dh.Data(cfg),
            overwritedata,
            overwriteindex,
            overwritebench)
    elif isinstance(algorithm, dataenums.SpatialTypeEnum):
        cfg['spatialtype'] = algorithm
        st = runkd.fullprocess(
            dh.Data(cfg),
            overwritedata,
            overwritebench)
    return st

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

    algos = []
    if 'haslsh' in cfg:
        algos.extend(dataenums.LSHTypeEnum.getValidTypes())
    if 'hasspatial' in cfg:
        algos.extend(dataenums.SpatialTypeEnum.getValidTypes())
    if 'hasms' in cfg:
        algos.extend(dataenums.MSTypeEnum.getValidTypes())
    if 'indexes' in cfg and cfg['indexes'] is not None:
        for idx in cfg['indexes'].split(','):
            print("algos", algos, idx)
            algos.append(dataenums.getEnumType(idx))
    SD = []
    for K in Ks:
        for D in Ds:
            for S in Ss:
                for a in algos:
                    SD.append((a,K,S,D))
    print(SD)
    data = dh.Data(cfg)
    dh.Data.mkdirs(data.benchdir, data.confdir, data.indexdir, data.querydir)
    pmap(
        partial(gendata, data=data), SD, cfg['parallel']
    )

    results = pmap(
        partial(process, data=data), SD, cfg['parallel']
    )
    statters = []
    printl('FinishedStats')
    for r in results:
        if r is None or isinstance(r, Exception):
            continue
        statters.append(r)
    printstats(statters)
