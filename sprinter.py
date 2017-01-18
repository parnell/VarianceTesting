from statter import LSHStatter, KDStatter, NOStatter, MSStatter
import datahelper as dh
from logger import printl, addLogFile, stacktrace

def getlsh(data):
    allv = []
    for t in dh.LSHTypeEnum.getValidTypes():
        data.cfg['lshtype'] = t
        nd = dh.Data(data.cfg)
        try:
            fs = LSHStatter(nd.getFoldedFiles('lshbenchfilepath'), nd)
            allv.append(fs)
        except:
            allv.append(NOStatter(t.name.upper(), nd))
    return allv

def getms(data):
    allv = []
    for t in dh.MSTypeEnum.getValidTypes():
        data.cfg['mstype'] = t
        nd = dh.Data(data.cfg)
        try:
            fs = MSStatter(nd.getFoldedFiles('msbenchfilepath'), nd)
            allv.append(fs)
        except:
            allv.append(NOStatter(t.name.upper(), nd))
    return allv

def printstats(stats):
    if not isinstance(stats, list):
        stats = [stats]
    a = [
        'headerline',
        'Dim', 'Size', 'K', 'Var', 'NClus', 'IdxName',
        'Cost', 'Average QueryTime', 'Average Calcs', 'Precision', 'Recall'
    ]

    final = [a]
    for s in stats:
        if 'synthetic' in s.data.cfg:
            c = s.data.cfg
            a = [   'statline',
                    c.D, c.S, c.K, c['variance'], c['nclus'],s.name,
                    s.cost, s.querytime, s.average, s.precision, s.recall]
            final.append(a)
        else:
            pass ### TODO

    for s in final:
        printl('\t'.join([str(x) for x in s]))
    # for s in final:
    #     print("\t".join([str(s) for s in s]))

    return final
