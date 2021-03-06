import configuration as cfg
from dataenums import LSHTypeEnum, MSTypeEnum

def isGauss(name):
    return "gauss" in name


class Config(dict):
    def __init__(self, *arg, **kw):
        '''
        S, size: datasize
        Q, query-size: query size
        F, fold: which fold are we using
        '''
        super(Config, self).__init__(*arg, **kw)
        self.loadFromModule(cfg)
        try:
            self['lshtype'] = LSHTypeEnum.fromValue(self['lshtype'])
        except:
            pass
        try:
            self['mstype'] = MSTypeEnum.fromValue(self['mstype'])
        except:
            pass
        assert self.Q is not None
        assert self.S is not None
        assert self.F is not None

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

    def getLSHBenchFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["LSH_BENCHMARK_NAME"].format(
            fullname=fullname,
            K=self["K"],
            lshtype=self['lshtype'].name,
            Q=self.Q,
            fold=self.F)
        return "%s/%s" %(dir,name)

    def getKBenchFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["K_BENCHMARK_NAME"].format(
            fullname=fullname,
            K=self["K"],
            Q=self.Q,
            fold=self.F)
        return "%s/%s" %(dir,name)

    def getKDBenchFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["KD_BENCHMARK_NAME"].format(
            fullname=fullname,
            K=self["K"],
            Q=self.Q,
            fold=self.F)
        return "%s/%s" %(dir,name)

    def getMSBenchFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["MS_BENCHMARK_NAME"].format(
            fullname=fullname,
            K=self["K"],
            Q=self.Q,
            fold=self.F,
            mstype=self['mstype'].name)
        return "%s/%s" %(dir,name)

    def getLSHRFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["LSHRFILE_NAME"].format(
            fullname=fullname,
            K=self["K"],
            lshtype=self['lshtype'].name,
            Q=self.Q,
            fold=self.F)
        return "%s/%s" %(dir,name)

    def getTopKFilePath(self, dataname, fullname, datatype):
        dir = self.getBenchDir(dataname, datatype)
        name = self["TOPK_NAME"].format(
            fullname=fullname,
            K=self["K"],
            Q=self.Q,
            fold=self.F)
        return "%s/%s" %(dir,name)

    def getLogFile(self, dataname, fullname):
        if isGauss(dataname):
            # "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"
            return self["LOG_NAME"].format(
                fullname=fullname,
                Q=self.Q,
                fold=self.F,
                K=self.K
                )
        else:
            assert 0


    # def getFinalResultFile(self, dataname, fullname):
    #     dir = self.getBenchDir(dataname, datatype)
    #     if isGauss(dataname):
    #         # "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"
    #         name = self["FINAL_RESULT_NAME"].format(
    #             fullname=fullname,
    #             Q=self.Q,
    #             fold=self.F,
    #             K=self.K
    #             )
    #         return "%s/%s" %(dir,name)
    #     else:
    #         assert 0

    def _getQFile(self, fullname, ftype):
        return self["QNAME"].format(
            fullname=fullname, Q=self.Q,fold=self.F,dataformat=ftype)

    def getQVecFile(self, fullname):
        return self._getQFile(fullname, 'vec')

    def getQMSVecFile(self, fullname):
        return self._getQFile(fullname, 'msvec')

    def getQBinFile(self, fullname):
        return self._getQFile(fullname, 'bin')

    def getQHDF5File(self, fullname):
        return self._getQFile(fullname, 'hdf5')

    def getGaussConfFile(self, fullname):
        return self["GAUSSCONF_NAME"].format(fullname=fullname)

    def getQVecFilePath(self, dataname, fullname, datatype):
        dir = self.getQueryDir(dataname, datatype)
        name = self.getQVecFile(fullname)
        return "%s/%s" %(dir,name)

    def getQBinFilePath(self, dataname, fullname, datatype):
        dir = self.getQueryDir(dataname, datatype)
        name = self.getQBinFile(fullname)
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
                dimensions=self.D,
                size=self.S,
                nclus=self["nclus"],
                var=self["variance"]
                )
        else:
            return self["GAUSSDATA_NAME"].format(name=dataname)

    def getLSHFullName(self, dataname):
        if isGauss(dataname):
            return self["GAUSSLSHDATA_NAME"].format(
                name=dataname,
                dimensions=self.D,
                size=self.S,
                nclus=self["nclus"],
                var=self["variance"],
                lshtype=self['lshtype'].name,
                lshM=self['lshM'],
                lshL=self['lshL'],
                lshS=self['lshS'],
                lshI=self['lshI'],
                lshN=self['lshN']
                )
        else:
            assert 0

    def getMSFullName(self, dataname):
        if isGauss(dataname):
            return self["GAUSSMSDATA_NAME"].format(
                name=dataname,
                dimensions=self.D,
                size=self.S,
                nclus=self["nclus"],
                var=self["variance"],
                mstype=self['mstype'].name
                )
        else:
            assert 0
    @property
    def nclus(self): return self['nclus']

    @property
    def variance(self): return self['variance']

    @property
    def Q(self): return self['query_size']

    @property
    def D(self): return self['dimensions']

    @D.setter
    def D(self, v): self['dimensions'] = v

    @property
    def F(self): return self['fold']

    @F.setter
    def F(self, v): self['fold'] = v

    @property
    def S(self): return self['size']

    @S.setter
    def S(self, v): self['size'] = v

    @property
    def K(self): return self['K']

    @K.setter
    def K(self, v): self['K'] = v


    @property
    def dim(self): return self['dimensions']

    @property
    def synthetic(self): return self['synthetic']

