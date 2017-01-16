import sys
import numpy as np
import sysarg
import datahelper as dh
import config
import runlsh
import runkd
import genGauss
from logger import printl, addLogFile
from statter import LSHStatter, KDStatter, NOStatter
np.set_printoptions(precision=4)

overwrite = True

def runLSH(data):
    ### Running LSH
    printl("@@@@@@@@ Running LSH @@@@@@@@")
    for lshtype in dh.LSHTypeEnum.getValidTypes():
        printl("------- Running LSH {} -------".format(lshtype))
        cfg['lshtype'] = lshtype
        try:
            data = runlsh.fullprocess(data, overwrite)
        except Exception as e:
            printl("Error running ", lshtype, " ", str(e))
    return data

def runKD(data):
    printl("@@@@ Running KD @@@@")
    runkd.fullprocess(data, overwrite)

def printStats(data):
    lshstats = {}
    for lshtype in dh.LSHTypeEnum.getValidTypes():
        cfg['lshtype'] = lshtype
        # ls = lyz.FileStatter(data.lshbenchfilepath)
        try:
            lshfs = LSHStatter(data.lshrfilepath)
            lshstats[lshtype] = lshfs
        except:
            lshstats[lshtype] = NOStatter()
        # ls.print()
        # printl("############ " , lshtype,  lshfs.getf('avg') )
        # lshfs.print()
        # printl("############")

    kd = KDStatter(data.kdbenchfilepath)
    # kd.print()
    printl("avgcalcs", 'KD', *lshstats.keys())
    a = [ stats.average for stats in lshstats.values()]
    a.append(kd.average)
    a = np.array(a)
    printl("acalcswithdev",*a)
    # printl("avgtime\t{}\t{}\t{}".format(
    #     ls.getf("totaltime"),
    #     lsh.getf("meanquerytime"),
    #     kd.getf("avgquerytime")
    # ))
    # printl("avgcalcs\t{}\t{}".format( lsh.getf("avg").split(' ')[0], kd.getf("avg")))
    printl('-#--------------------------------------#-')


if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)

    args, unknown = sysarg.getParsed(sys.argv, True)

    cfg = config.Config(vars(args))

    printl('-#--------------------------------------#-')
    printl(cfg)
    for S in [5000]:
        for D in [10,20]:
            cfg.S = S
            cfg.D = D
            data = dh.Data(cfg)
            addLogFile(data.logfile)

            if cfg['synthetic']:
                genGauss.process(data)

            data = runLSH(data)
            runKD(data)

            printStats(data)

# 2017-01-14 23:35:27,306 - INFO : avgcalcs KD KDBQ ITQ DBQ PSD SH
# 2017-01-14 23:35:27,322 - INFO : acalcswithdev 1631.97 96978.8 3178.11 58525.1 7896.36 11752.179688
