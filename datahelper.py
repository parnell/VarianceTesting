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

    def fromValue(idx, enumType):
        if isinstance(idx, bytes):
            idx = idx.decode('utf-8')

        if isinstance(idx, str) and idx.isdigit():
            idx = int(idx)
        else:
            for name, member in enumType.__members__.items():
                if name == idx:
                    return member
        raise ("Index " + str(idx)+" not found in "+ str(enumType) +" " + str(type(idx)))

def isGauss(name):
    return "gauss" in name

class DataFormatEnum(BaseEnum):
    bin = 0
    hdf5 = 1
    vec = 2
    vect = 3

    def format(name):
        return DataFormatEnum.fromValue(getRawExtension(name), DataFormatEnum)

class DataTypeEnum(BaseEnum):
    vec = 0
    graph = 1

    def type(name):
        try:
            return DataTypeEnum.fromValue(getRawExtension(name),DataTypeEnum)
        except Exception as e:
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
    def __init__(self, dataname, cfg):
        self.oname = os.path.abspath(dataname)
        # assert(os.path.exists(self.oname))
        self.cfg = cfg
        n = getStem(dataname)
        self.dataname = n if "__" not in n else n.split("__")[0]
        self.fullname = cfg.getFullName(self.dataname)
        self.datatype = DataTypeEnum.type(self.oname)


    def createBinFile(self, overwrite=False):
        n = self.binfilepath
        if overwrite or not os.path.exists(n):
            progs.vec2bin(self.oname,n)

    def createHDF5File(self, overwrite=False):
        Data.vec2hdf5(self.oname, self.hdf5filepath, overwrite)

    def vec2hdf5(src, dest, overwrite=False):
        if overwrite or not os.path.exists(dest):
            progs.vec2hdf5(src, dest, True)

    @property
    def type(self):
        return DataTypeEnum.type(self.oname)

    @property
    def benchfilepath(self):
        return self.cfg.getBenchFilePath(self.dataname, self.fullname, self.type)

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
    def K(self):
        return self.cfg["K"]

    @property
    def Q(self):
        return self.cfg["Q"]

    @property
    def var(self):
        return self.cfg["var"]

    @property
    def format(self):
        return DataFormatEnum.format(self.oname)

    @property
    def datadir(self):
        return self.cfg["datadir"]

    @property
    def datadirfull(self):
        return self.cfg.getDataDirFull(self.dataname, self.datatype)

    @property
    def benchdir(self):
        return self.cfg.getBenchDir(self.dataname, self.datatype)

    @property
    def resultdir(self):
        return self.cfg.getBenchDir(self.dataname, self.datatype)

    @property
    def confdir(self):
        return self.cfg.getConfDir(self.dataname, self.datatype)

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
    def qhdf5file(self):
        return "%s.hdf5" %self.fullname

    @property
    def qvecfile(self):
        return self.cfg.getQVecFile(self.fullname) 

    @property
    def qhdf5file(self):
        return self.cfg.getQHDF5File(self.fullname) 

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
    def hdf5filepath(self):
        return "%s/%s" %(self.datadirfull, self.hdf5file)

    @property
    def qvecfilepath(self):
        return "%s/%s" %(self.querydir, self.qvecfile)

    @property
    def qhdf5filepath(self):
        return "%s/%s" %(self.querydir, self.qhdf5file)

    @property
    def gaussconffilepath(self):
        return "%s/%s" %(self.confdir, self.gaussconffile)

    def remove(*args):
        for arg in args:
            if os.path.exists(arg):
                os.remove(arg)

    def mkdirs(*args):
        for arg in args:
            if not os.path.exists(arg):
                os.makedirs(arg)
