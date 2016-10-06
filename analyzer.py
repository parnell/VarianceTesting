#!/usr/bin/env python3
import numpy as np
import os
import re
import collections
import traceback
PT_S = re.compile("(([^\s,]+)\s*=\s*([^\s,]+))")

class Analyzer():
    def __init__(self, data):
        self.data = data


class Statter():
    def __init__(self):
        self.kv = collections.OrderedDict()
        self.isparsed = False

    def get(self, key):
        if not self.isparsed: 
            self.parse()
        return self.kv[key]

    def getf(self, key):
        """
        get first value from key
        """
        return self.get(key)[0]

    def print(self):
        if not self.isparsed: 
            self.parse()
        for k,v in self.kv.items():
            try:
                if v.shape[0] > 1:
                    s = "{} : n={}, mean={}, min={}, max={}".format(
                        k,
                        v.shape[0],
                        v.mean(),
                        min(v),
                        max(v)
                    )
                    print(s)
                else:
                    print(k,":",v[0])
            except Exception as e:
                print(k,":",v)
                # traceback.print_exc()
                

    def parse(self):
        for l in self.next():
            matches = PT_S.findall(l)
            if not matches:
                continue
            for __, k, v in matches:
                if k not in self.kv:
                    self.kv[k] = []
                self.kv[k].append(v)

        ### turn into np array of ints or floats if possible
        for k,v in self.kv.items():
            a = np.array(v)
            try:
                a = a.astype(int)
            except:
                try:
                    a = a.astype(float)
                except:
                    pass
            self.kv[k] = a

        self.isparsed = True

class FileStatter(Statter):
    def __init__(self, filename):
        super(FileStatter, self).__init__()
        self.filename = filename
        if not os.path.exists(self.filename):
            raise FileNotFoundError(filename)

    def next(self):
        for line in open(self.filename):
            yield line

class StrStatter(Statter):
    def __init__(self, val):
        super(StrStatter, self).__init__()
        self.val = val
    
    def next(self):
        if not isinstance(self.val, list):
            yield self.val
        else:
            for line in self.val:
                yield line


# st = StrStatter(["RECALL   = +0.7 +/- 0.102598 something=nothing, space=0.3, time=0.00085","RECALL=-3", "T=4","T=Zot"])
# st.print()