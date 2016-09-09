import configuration as cfg
import os

def isGauss(name):
    return "gauss" in name

class Config(dict):
    def __init__(self, datadir, *arg, **kw):
        super(Config, self).__init__(*arg, **kw)
        self.loadFromModule(cfg)
        self["datadir"] = datadir
    
    def loadFromModule(self, module):
        for v in dir(module):
            if v.startswith('__'):
                continue
            self[v] = getattr(module,v)

    def getDataDirFull(self, dataname, datatype):
        # "{datadir}/{datatype}/{dataname}"
        return self["DATADIRFULL_FORMAT"].format(
            datadir=self["datadir"],
            datatype=str(datatype),
            dataname=dataname
        )

    def getIndexDir(self, dataname, datatype):
        datadirfull = self.getDataDirFull(dataname, datatype)
        return self["INDEXDIR_FORMAT"].format(datadirfull=datadirfull)

    def getBenchDir(self, dataname, datatype):
        datadirfull = self.getDataDirFull(dataname, datatype)
        return self["BENCHMARKDIR_FORMAT"].format(datadirfull=datadirfull)

    def getBenchFilePath(self, dataname, fullname, datatype):
        bdir = self.getBenchDir(dataname, datatype)
        bname = self["BENCHMARK_NAME"].format(fullname=fullname,K=self["K"])
        return "{bdir}/{bname}".format(bdir=bdir, bname=bname)

    def getLSHRFilePath(self, dataname, fullname, datatype):
        bdir = self.getBenchDir(dataname, datatype)
        name = self["LSHRFILE_NAME"].format(fullname=fullname,K=self["K"])
        return "{bdir}/{name}".format(bdir=bdir, name=name)

    def getTopKFilePath(self, dataname, fullname, datatype):
        datadirfull = self.getDataDirFull(dataname, datatype)
        bdir = self["BENCHMARKDIR_FORMAT"].format(datadirfull=datadirfull)
        bname = self["TOPK_NAME"].format(fullname=fullname,K=self["K"])
        return "{bdir}/{bname}".format(bdir=bdir, bname=bname)

    def getFullName(self, dataname):
        if isGauss(dataname):
            # "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"
            return self["GAUSSDATA_NAME"].format(
                name=dataname, 
                dimensions=self["D"],
                size=self["size"],
                nclus=self["nclus"],
                var=self["var"]
                )
        else:
            assert(0)            
