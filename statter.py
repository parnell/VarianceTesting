import analyzer
from analyzer import Statter

class NOStatter():

    @property
    def average(self):
        return -1

class LSHStatter(analyzer.FileStatter):
    def __init__(self, filename):
        super().__init__(filename)
        self.firstvalue = True
        self.setExclude('^#')

    @property
    def average(self):
        try: return self.get('avg', Statter.mean)
        except: return -1

    @property
    def precision(self):
        try: return self.get('PRECISION', Statter.mean)
        except: return -1

    @property
    def recall(self):
        try: return self.get('RECALL', Statter.mean)
        except: return -1

    @property
    def cost(self):
        try: return self.get('COST', Statter.mean)
        except: return -1

    @property
    def querytime(self):
        try: return self.getf('meanquerytime')
        except: return -1


class KDStatter(analyzer.FileStatter):
    def __init__(self, filename):
        super().__init__(filename)

    @property
    def average(self):
        try: return self.getf('avg')
        except: return -1

    @property
    def precision(self):
        return 1

    @property
    def recall(self):
        return 1

    @property
    def cost(self):
        try: return self.getf('cost')
        except: return -1

    @property
    def querytime(self):
        try: return self.getf('avgquerytime')
        except: return -1

