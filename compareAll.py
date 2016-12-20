import sys
import os

import sysarg
import datahelper as dh
import config
import analyzer as lyz
import runlsh
import runkd
import genGauss
from logger import printl
overwrite = True
sys.argv = sysarg.args(__file__)
args, unknown = sysarg.getParsed(sys.argv, True)

cfg = config.Config(vars(args))
data = dh.Data(cfg)
printl('-#--------------------------------------#-')
printl(cfg)
genGauss.process(data)
printl("@@@@ Running LSH @@@@")
runlsh.process(data, overwrite)
printl("@@@@ Running KD @@@@")
runkd.fullprocess(data, overwrite)

# N0692-ZY350-78988-0XAK6-992NN
ls = lyz.FileStatter(data.lshbenchfilepath)
lsh = lyz.FileStatter(data.lshrfilepath)
kd = lyz.FileStatter(data.kdbenchfilepath)
ls.print()
printl("############")
lsh.print()
printl("############")
kd.print()
printl("avgcalcs", 'LSH', 'KD')
printl("acalcswithdev\t{}\t{}".format( lsh.getf("avg"), kd.getf("avg")))
printl("avgtime\t{}\t{}\t{}".format(
    ls.getf("totaltime"),
    lsh.getf("meanquerytime"),
    kd.getf("avgquerytime")
))
printl("avgcalcs\t{}\t{}".format( lsh.getf("avg").split(' ')[0], kd.getf("avg")))
printl('-#--------------------------------------#-')
