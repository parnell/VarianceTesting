import analyzer

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
        try:
            return self.get('avg', analyzer.Statter.mean)
        except:
            return -1


class KDStatter(analyzer.FileStatter):
    def __init__(self, filename):
        super().__init__(filename)

    @property
    def average(self):
        return self.getf('avg', float)


