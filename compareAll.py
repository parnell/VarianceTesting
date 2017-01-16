import sys
import numpy as np
import sysarg
import datahelper as dh
import config
import runlsh
import runkd
import genGauss
from logger import printl, addLogFile, stacktracem
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
            data = runlsh.fullprocess(data, overwrite,overwrite,overwrite)
        except Exception as e:
            stacktracem("LSH Problem")
            printl("Error running ", lshtype, " ", str(e))
    return data

def runKD(data):
    printl("@@@@ Running KD @@@@")
    runkd.fullprocess(data, overwrite)

def printStats(data):
    lshstats = {}
    for lshtype in dh.LSHTypeEnum.getValidTypes():
        data.cfg['lshtype'] = lshtype
        nd = dh.Data(data.cfg)
        # ls = lyz.FileStatter(data.lshbenchfilepath)
        try:
            lshfs = LSHStatter(nd.getFoldedFiles('lshrfilepath'))
            lshstats[lshtype] = lshfs
        except:
            lshstats[lshtype] = NOStatter()
        # ls.print()
        # printl("############ " , lshtype,  lshfs.getf('avg') )
        # lshfs.print()
        # printl("############")
    kd = KDStatter(data.kdbenchfilepath)
    allv = [kd]
    allv.extend(lshstats.values())

    printl('-#--------------------------------------#-')
    final = [('params', [data.lshrfilepath])]
    # kd.print()
    final.append(('name', ['KD', *lshstats.keys()]))
    final.append(('cost',[ stats.cost for stats in allv]))
    final.append(('average',[ stats.average for stats in allv]))
    final.append(('precision',[ stats.precision for stats in allv]))
    final.append(('recall',[ stats.recall for stats in allv]))
    final.append(('querytime',[ stats.querytime for stats in allv]))

    for name, stats in final:
        printl(name, *stats)
        print(name+"\t"+"\t".join([str(s) for s in stats]))

    printl('-#--------------------------------------#-')
    return final

if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)

    args, unknown = sysarg.getParsed(sys.argv, True)
    print(args)
    cfg = config.Config(vars(args))

    printl('-#--------------------------------------#-')
    printl(cfg)
    final = []
    for S in [10000]:
        for D in [10]:
            cfg.S = S
            cfg.D = D
            data = dh.Data(cfg)
            addLogFile(data.logfile)

            if cfg['synthetic']:
                genGauss.process(data)

            data = runLSH(data)
            runKD(data)

            f = printStats(data)
            final.append(f)

    for finalstats in final:
        for name, stats in finalstats:
            printl(name, *stats)

    for finalstats in final:
        for name, stats in finalstats:
            print(name+"\t"+"\t".join([str(s) for s in stats]))



# 2017-01-14 23:35:27,306 - INFO : avgcalcs KD KDBQ ITQ DBQ PSD SH
# 2017-01-14 23:35:27,322 - INFO : acalcswithdev 1631.97 96978.8 3178.11 58525.1 7896.36 11752.179688
