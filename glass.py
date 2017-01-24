import sys
import sysarg

import config
import dataenums
import datahelper as dh


if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    args, unknown = sysarg.getParsed(sys.argv, True)
    cfg = config.Config(vars(args))

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
    for sd in SD:
        print('----', sd[0].name, *sd[1:])
        algo = sd[0]
        d = dh.DataFactory.fromAKSD(cfg, *sd)
        if isinstance(algo, dataenums.SpatialTypeEnum):
            print('bench=\t', d.kdbenchfilepath)
        elif isinstance(algo, dataenums.MSTypeEnum):
            print('bench=\t', d.msbenchfilepath)
        elif isinstance(algo, dataenums.LSHTypeEnum):
            print('bench=\t', d.lshbenchfilepath)


