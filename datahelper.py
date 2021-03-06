import os
import copy
import dataenums

class DataFactory():
    @staticmethod
    def fromAKSD(cfg, a,k,s,d):
        cfg = copy.deepcopy(cfg)
        cfg[a.cfgkey()] = a
        cfg.K = k
        cfg.S = s
        cfg.D = d
        return Data(cfg)

def getStem(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def getExtension(filename):
    return os.path.splitext(os.path.basename(filename))[1]

def getRawExtension(filename):
    return os.path.splitext(os.path.basename(filename))[1][1:]

def getBasename(filename):
    return os.path.basename(filename)

def isGauss(name):
    return "gauss" in name

class File():
    def __init__(self, filename):
        self.filename = filename

    @property
    def stem(self):
        return os.path.splitext(os.path.basename(self.filename))[0]

    def getExtension(self):
        return os.path.splitext(os.path.basename(self.filename))[1]

    def getRawExtension(self):
        return os.path.splitext(os.path.basename(self.filename))[1][1:]

    def getBasename(self):
        return os.path.basename(self.filename)

class Data():
    def __init__(self, cfg):
        self.cfg = cfg
        self.dataname = cfg['shortname']

        self.type = dataenums.DataTypeEnum.type(self.dataname)
        self.fullname = cfg.getFullName(self.dataname)

        # self.oname = os.path.abspath(dataname)
        # assert(os.path.exists(self.oname))
        n = getStem(self.vecfilepath)
        self.dataname = n if "__" not in n else n.split("__")[0]

    @property
    def msfullname(self):
        return self.cfg.getMSFullName(self.dataname)

    @property
    def lshfullname(self):
        return self.cfg.getLSHFullName(self.dataname)

    @property
    def lshbestfilepath(self):
        return self.cfg.getLSHBenchFilePath(self.dataname, self.lshfullname, self.type)

    @property
    def lshbenchfilepath(self):
        return self.cfg.getLSHBenchFilePath(self.dataname, self.lshfullname, self.type)

    @property
    def kbenchfilepath(self):
        return self.cfg.getKBenchFilePath(self.dataname, self.fullname, self.type)

    @property
    def lshrfilepath(self):
        return self.cfg.getLSHRFilePath(self.dataname, self.lshfullname, self.type)

    def getFoldedFiles(self, path):
        oldF = self.cfg.F
        res = []
        for i in range(self.cfg['nfolds']):
            self.cfg.F = i
            s = self.__getattribute__(path)
            res.append(s)
        self.cfg.F = oldF
        return res

    @property
    def kdbenchfilepath(self):
        return self.cfg.getKDBenchFilePath(self.dataname, self.fullname, self.type)

    @property
    def msbenchfilepath(self):
        return self.cfg.getMSBenchFilePath(self.dataname, self.fullname, self.type)

    @property
    def topkfilepath(self):
        return self.cfg.getTopKFilePath(self.dataname, self.fullname, self.type)

    @property
    def logfile(self):
        return self.cfg.getLogFile(self.dataname, self.fullname)

    @property
    def K(self):
        return self.cfg.K

    @property
    def Q(self):
        return self.cfg.Q

    @property
    def S(self):
        return self.cfg.S

    @property
    def var(self):
        return self.cfg.variance

    # @property
    # def format(self):
    #     return DataFormatEnum.format(self.oname)

    @property
    def datadir(self):
        return self.cfg["datadir"]

    @property
    def datadirfull(self):
        return self.cfg.getDataDirFull(self.dataname, self.type)

    @property
    def benchdir(self):
        return self.cfg.getBenchDir(self.dataname, self.type)

    @property
    def resultdir(self):
        return self.cfg.getBenchDir(self.dataname, self.type)

    @property
    def confdir(self):
        return self.cfg.getConfDir(self.dataname, self.type)

    @property
    def indexdir(self):
        return self.cfg.getIndexDir(self.dataname, self.type)

    @property
    def querydir(self):
        return self.cfg.getQueryDir(self.dataname, self.type)

    @property
    def lshindexfilepath(self):
        return "%s/%s" %(self.indexdir, self.lshindexfile)

    @property
    def lshindexfile(self):
        return "%s_t=%s.lsh" %(self.lshfullname, self.cfg['lshtype'].name)

    @property
    def msindexfilepath(self):
        return "%s/%s" %(self.indexdir, self.msindexfile)

    @property
    def msbuildbenchfilepath(self):
        return "%s/%s" %(self.benchdir, self.msbuildbenchfile)

    @property
    def msindexfile(self):
        return "%s.idx.ms" %(self.msfullname)

    @property
    def msbuildbenchfile(self):
        return "%s.build.bench.txt" %(self.msfullname)

    @property
    def hdf5file(self):
        return "%s.hdf5" %self.fullname

    @property
    def binfile(self):
        return "%s.bin" %self.fullname

    @property
    def msbinfile(self):
        return "%s.ms.bin" %self.fullname

    @property
    def vecfile(self):
        return "%s.vec" %self.fullname

    @property
    def vectfile(self):
        return "%s.vect" %self.fullname

    @property
    def qhdf5file(self):
        return self.cfg.getQHDF5File(self.fullname)

    @property
    def qvecfile(self):
        return self.cfg.getQVecFile(self.fullname)

    @property
    def qmsvecfile(self):
        return self.cfg.getQMSVecFile(self.fullname)

    @property
    def qbinfile(self):
        return self.cfg.getQBinFile(self.fullname)

    @property
    def gaussconffile(self):
        return self.cfg.getGaussConfFile(self.fullname)

    @property
    def binfilepath(self):
        return "%s/%s" %(self.datadirfull, self.binfile)

    @property
    def msbinfilepath(self):
        return "%s/%s" %(self.datadirfull, self.msbinfile)

    @property
    def vecfilepath(self):
        return "%s/%s" %(self.datadirfull, self.vecfile)

    @property
    def vectfilepath(self):
        return "%s/%s" %(self.datadirfull, self.vectfile)

    @property
    def hdf5filepath(self):
        return "%s/%s" %(self.datadirfull, self.hdf5file)

    @property
    def qvecfilepath(self):
        return "%s/%s" %(self.querydir, self.qvecfile)

    @property
    def qmsvecfilepath(self):
        return "%s/%s" %(self.querydir, self.qmsvecfile)

    @property
    def qbinfilepath(self):
        return "%s/%s" %(self.querydir, self.qbinfile)

    @property
    def qhdf5filepath(self):
        return "%s/%s" %(self.querydir, self.qhdf5file)

    @property
    def gaussconffilepath(self):
        return "%s/%s" %(self.confdir, self.gaussconffile)

    @staticmethod
    def remove(*args):
        for arg in args:
            if os.path.exists(arg):
                try:
                    os.remove(arg)
                except:
                    pass

    @staticmethod
    def mkdirs(*args):
        for arg in args:
            if not os.path.exists(arg):
                try:
                    os.makedirs(arg)
                except:
                    pass
