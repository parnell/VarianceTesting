import configuration as cfg
import os

def isGauss(name):
    return "gauss" in name

class Config(dict):
    def __init__(self, datadir, confdir, resultdir, *arg, **kw):
        super(Config, self).__init__(*arg, **kw)
        self.loadFromModule(cfg)
        self["datadir"] = datadir
        self["confdir"] = confdir
        self["resultdir"] = resultdir
        assert(self["Q"] is not None)
        assert(self["S"] is not None)
        assert(self["F"] is not None)
    
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

    def getResultDirFull(self, dataname, datatype):
        # "{resultdir}/{datatype}/{dataname}"
        return self["RESULTDIRFULL_FORMAT"].format(
            resultdir=self["resultdir"],
            datatype=str(datatype),
            dataname=dataname
        )

    def getConfDirFull(self, dataname, datatype):
        # "{confdir}/{datatype}/{dataname}"
        return self["CONFDIRFULL_FORMAT"].format(
            confdir=self["confdir"],
            datatype=str(datatype),
            dataname=dataname
        )

    def getIndexDir(self, dataname, datatype):
        dir = self.getDataDirFull(dataname, datatype)
        return self["INDEXDIR_FORMAT"].format(datadirfull=dir)

    def getQueryDir(self, dataname, datatype):
        dir = self.getDataDirFull(dataname, datatype)
        return self["QDIR_FORMAT"].format(datadirfull=dir)

    def getBenchDir(self, dataname, datatype):
        dir = self.getResultDirFull(dataname, datatype)
        return self["BENCHMARKDIR_FORMAT"].format(resultdirfull=dir)

    def getConfDir(self, dataname, datatype):
        dir = self.getConfDirFull(dataname, datatype)
        return self["CONFDIR_FORMAT"].format(confdirfull=dir)

    def getBenchFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["BENCHMARK_NAME"].format(fullname=fullname,K=self["K"])
        return "%s/%s" %(dir,name)

    def getKDBenchFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["KD_BENCHMARK_NAME"].format(fullname=fullname,K=self["K"])
        return "%s/%s" %(dir,name)

    def getLSHRFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["LSHRFILE_NAME"].format(fullname=fullname,K=self["K"])
        return "%s/%s" %(dir,name)

    def getTopKFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["TOPK_NAME"].format(fullname=fullname,K=self["K"])
        return "%s/%s" %(dir,name)

    def getQVecFile(self, fullname):
        return self["QNAME"].format(fullname=fullname,
            Q=self["Q"],F=self["F"],dataformat="vec")

    def getQHDF5File(self, fullname):
        return self["QNAME"].format(fullname=fullname,
            Q=self["Q"],F=self["F"],dataformat="hdf5")

    def getGaussConfFile(self, fullname):
        return self["GAUSSCONF_NAME"].format(fullname=fullname)

    def getQVecFilePath(self, dataname, fullname, datatype):
        dir = self.getQueryDir(dataname, datatype)
        name = self.getQVecFile(fullname)
        return "%s/%s" %(dir,name)

    def getQHDF5FilePath(self, dataname, fullname, datatype):
        dir = self.getQueryDir(dataname, datatype)
        name = self.getQHDF5File(fullname)
        return "%s/%s" %(dir,name)

    def getFullName(self, dataname):
        if isGauss(dataname):
            # "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"
            return self["GAUSSDATA_NAME"].format(
                name=dataname, 
                dimensions=self["D"],
                size=self["S"],
                nclus=self["nclus"],
                var=self["var"]
                )
        else:
            assert(0)            
