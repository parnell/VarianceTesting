from enum import Enum, IntEnum
import os
import subprocess
import programs as progs

def getStem(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def getExtension(filename):
    return os.path.splitext(os.path.basename(filename))[1]

def getRawExtension(filename):
    return os.path.splitext(os.path.basename(filename))[1][1:]

def getBasename(filename):
    return os.path.basename(filename)

class BaseEnum(IntEnum):
    def __str__(self):
        return os.path.splitext(os.path.basename(Enum.__str__(self)))[1][1:]

    @staticmethod
    def fromValue(idx, enumType):
        if isinstance(idx, bytes):
            idx = idx.decode('utf-8')

        if isinstance(idx, str) and idx.isdigit():
            idx = int(idx)
        else:
            for name, member in enumType.__members__.items():
                if name == idx:
                    return member
        raise "Index " + str(idx)+" not found in "+ str(enumType) +" " + str(type(idx))

def isGauss(name):
    return "gauss" in name

class DataFormatEnum(BaseEnum):
    bin = 0
    hdf5 = 1
    vec = 2
    vect = 3

    @staticmethod
    def format(name):
        return DataFormatEnum.fromValue(getRawExtension(name), DataFormatEnum)

class DataTypeEnum(BaseEnum):
    vec = 0
    graph = 1

    @staticmethod
    def type(name):
        try:
            return DataTypeEnum.fromValue(getRawExtension(name),DataTypeEnum)
        except:
            if "gauss" in name:
                return DataTypeEnum.vec
            raise Exception("data type not known")

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
        self.dataname = cfg['shortname']
        self.type = DataTypeEnum.type(self.dataname)
        self.fullname = cfg.getFullName(self.dataname)
        # self.oname = os.path.abspath(dataname)
        # assert(os.path.exists(self.oname))
        self.cfg = cfg
        n = getStem(self.vecfilepath)
        self.dataname = n if "__" not in n else n.split("__")[0]


    # def createBinFile(self, overwrite=False):
    #     n = self.binfilepath
    #     if overwrite or not os.path.exists(n):
    #         progs.vec2bin(self.vecfilepath,n)

    # def createHDF5File(self, overwrite=False):
    #     Data.vec2hdf5(self.vecfilepath, self.hdf5filepath, overwrite)

    @property
    def lshbenchfilepath(self):
        return self.cfg.getLSHBenchFilePath(self.dataname, self.fullname, self.type)

    @property
    def lshrfilepath(self):
        return self.cfg.getLSHRFilePath(self.dataname, self.fullname, self.type)

    @property
    def kdbenchfilepath(self):
        return self.cfg.getKDBenchFilePath(self.dataname, self.fullname, self.type)

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
        return "%s.lsh" %self.fullname

    @property
    def hdf5file(self):
        return "%s.hdf5" %self.fullname

    @property
    def binfile(self):
        return "%s.bin" %self.fullname

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
    def qbinfile(self):
        return self.cfg.getQBinFile(self.fullname)

    @property
    def gaussconffile(self):
        return self.cfg.getGaussConfFile(self.fullname)

    @property
    def binfilepath(self):
        return "%s/%s" %(self.datadirfull, self.binfile)

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
                os.remove(arg)

    @staticmethod
    def mkdirs(*args):
        for arg in args:
            if not os.path.exists(arg):
                os.makedirs(arg)
