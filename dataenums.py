from enum import IntEnum, Enum
import os

def getRawExtension(filename):
    return os.path.splitext(os.path.basename(filename))[1][1:]

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

def getEnumType(val):
    try:
        return LSHTypeEnum.fromValue(val)
    except:
        pass
    try:
        return MSTypeEnum.fromValue(val)
    except:
        pass
    try:
        return SpatialTypeEnum.fromValue(val)
    except:
        pass
    raise "Index " + str(val)+" not found in Index enums " + str(type(val))


class DataFormatEnum(BaseEnum):
    bin = 0
    hdf5 = 1
    vec = 2
    vect = 3

    @staticmethod
    def format(name):
        return DataFormatEnum.fromValue(getRawExtension(name), DataFormatEnum)


class AlgoType(BaseEnum):
    pass

class SpatialTypeEnum(AlgoType):
    kd = 0

    @staticmethod
    def getValidTypes():
        return [SpatialTypeEnum.kd]

    @staticmethod
    def fromValue(idx):
        return BaseEnum.fromValue(idx, SpatialTypeEnum)

class MSTypeEnum(AlgoType):
    mvp = 0
    pivots = 1
    sat = 2
    lcluster = 3
    ght = 4
    aesa = 5
    iaesa = 6
    bkt = 7
    dyn = 8
    fqh = 9
    fqt = 10

    @staticmethod
    def prog(name):
        if str(name) == str(MSTypeEnum.dyn.name):
            return 'dyn-sat'
        else:
            return name

    @staticmethod
    def fromValue(idx):
        return BaseEnum.fromValue(idx, MSTypeEnum)

    @staticmethod
    def getValidTypes():
        return [
            MSTypeEnum.mvp,
            # MSTypeEnum.lcluster,
            MSTypeEnum.sat,
            MSTypeEnum.dyn
            # MSTypeEnum.iaesa,
            ]

class LSHTypeEnum(AlgoType):
    KDBQ = 0
    ITQ = 1
    DBQ = 2
    PSD = 3
    RBS = 4
    RHP = 5
    SH = 6
    TH = 7

    @staticmethod
    def fromValue(idx):
        return BaseEnum.fromValue(idx, LSHTypeEnum)

    @staticmethod
    def getValidTypes():
        return [
            LSHTypeEnum.KDBQ,
            LSHTypeEnum.ITQ,
            LSHTypeEnum.DBQ,
            LSHTypeEnum.PSD,
            LSHTypeEnum.SH
            ]


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
