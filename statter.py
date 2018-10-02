import copy

from analyzer import StatType, FileStatter

class NOStatter():
    def __init__(self, name, data):
        self.name = name
        self.data = copy.deepcopy(data)

    @property
    def average(self): return ''

    @property
    def cost(self): return ''

    @property
    def recall(self): return ''

    @property
    def precision(self): return ''

    @property
    def querytime(self): return ''

class MSStatter(FileStatter):
    def __init__(self, filename, data):
        super().__init__(filename)
        self.data = copy.deepcopy(data)
        self.firstvalue = True
        self.setExclude('^#')
        self.size = data.S
        self.nqueries = data.Q
        self.name = data.cfg['mstype'].name.upper()

    @property
    def average(self):
        try: return self.getf('Total distances per query')
        except: return -1

    @property
    def querytime(self):
        try:
            t= self.getf('avgtime')
            if t == 0:
                return self.getf('totaltime')/self.nqueries
        except: return -1

    @property
    def cost(self):
        try: return self.average / self.size
        except: return -1

    @property
    def precision(self): return 1

    @property
    def recall(self): return 1


class PMSStatter(FileStatter):
    def __init__(self, filename, data):
        super().__init__(filename)
        self.data = copy.deepcopy(data)
        self.firstvalue = True
        self.setExclude('^#')
        self.size = data.S
        self.nqueries = data.Q
        self.name = data.cfg['mstype'].name.upper()

    @property
    def meanofall(self):
        try: return self.getf('meanofall')
        except: return -1
    @property
    def varofall(self):
        try: return self.getf('varofall')
        except: return -1
    @property
    def devofall(self):
        try: return self.getf('devofall')
        except: return -1

    @property
    def average(self):
        try: return self.getf('Total distances per query')
        except: return -1

    @property
    def querytime(self):
        try:
            t= self.getf('avgtime')
            if t == 0:
                return self.getf('totaltime')/self.nqueries
        except: return -1

    @property
    def cost(self):
        try: return self.average / self.size
        except: return -1

    @property
    def precision(self): return self.getf('nodespruned')

    @property
    def recall(self): return self.getf('pointspruned')

class LSHStatter(FileStatter):
    def __init__(self, filename, data):
        super().__init__(filename)
        self.data = copy.deepcopy(data)
        self.firstvalue = True
        self.setExclude('^#')
        self.name = data.cfg['lshtype'].name.upper()

    @property
    def average(self):
        try: return self.get('avg', StatType.mean)
        except: return -1

    @property
    def precision(self):
        try: return self.get('PRECISION', StatType.mean)
        except: return -1

    @property
    def recall(self):
        try: return self.get('RECALL', StatType.mean)
        except: return -1

    @property
    def cost(self):
        try: return self.get('COST', StatType.mean)
        except: return -1

    @property
    def querytime(self):
        try: return self.getf('meanquerytime')
        except: return -1


class KDStatter(FileStatter):
    def __init__(self, filename, data):
        super().__init__(filename)
        self.data = copy.deepcopy(data)
        self.name = 'kd'.upper()

    @property
    def average(self):
        try: return self.getf('avg')
        except: return -1

    @property
    def precision(self): return 1

    @property
    def recall(self): return 1

    @property
    def cost(self):
        try: return self.getf('cost')
        except: return -1

    @property
    def querytime(self):
        try: return self.getf('avgquerytime')
        except: return -1
