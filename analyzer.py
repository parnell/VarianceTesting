#!/usr/bin/env python3
import math
import statistics
import os
import re
import collections
import traceback
import sys
import argparse
import locale
locale.setlocale(locale.LC_ALL, '')

try:
    import numpy as np
    np.set_printoptions(precision=4)
    numpy=True
except:
    numpy=False

PT_S = ""
PT_E = ""
currency=False

def setDelimiter(d):
    global PT_S
    global PT_E
    PT_S = re.compile("(([^\s{}]+)\s*=\s*([^\s{}]+))".format(d,d))
    PT_E = re.compile("\s*([^\s{}]+)\s*".format(d))

setDelimiter(',\t')    

class Analyzer():
    def __init__(self, data):
        self.data = data

class Statter():
    def __init__(self):
        self.kv = collections.OrderedDict()
        self.isparsed = False
        self.defaults= {}

    def get(self, key):
        if not self.isparsed: 
            self.parse()
        return self.kv[key]

    def getf(self, key):
        """
        get first value from key
        """
        return self.get(key)[0]

    def print(self, keys=None):
        if not self.isparsed: 
            self.parse()
        fmt = "{} : n={}\tsum={}\tmean={}\tmin={}\tmax={}"\
                "\tstddev={:5f}"
        for k,v in self.kv.items():
            if keys is not None and not k in keys:
                continue
            try:
                n = v.shape[0] if numpy and not isinstance(v,list) else len(v)
                mean = v.mean() if numpy and not isinstance(v,list) else statistics.mean(v)
                var = statistics.stdev(v) if len(v) > 1 else math.nan
                a = [n, sum(v), mean, min(v), max(v), var]
                # if currency:
                #     a = [ locale.currency(val, grouping=True) for val in v] 
                if n > 1:
                    s = fmt.format(k, *a)
                    print(s)
                else:
                    print(k,":",v[0])
            except TypeError as e:
                if len(v) > 10:
                    print(k,': [',*v[0:5],"...",*v[-5:],']')
                else:
                    print(k,":",v)    
            except Exception as e:
                if len(v) > 10:
                    print(k,': [',*v[0:5],"...",*v[-5:],']')
                else:
                    print(k,":",v)    
                traceback.print_exc()
                
    def __totype(v):
        if currency:
            try:
                v = [ locale.atof(val.replace('$','')) for val in v]
            except:
                traceback.print_exc()
        if numpy:
            a = np.array(v)
            try:
                return a.astype(int)
            except:
                try:
                    return a.astype(float)
                except:
                    try:
                        a= a.astype("|S5")
                        return (a==b'True').astype(bool)
                    except:
                        traceback.print_exc()
        else:
            try:
                return [int(x) for x in v]
            except:
                try:
                    return [float(x) for x in v]
                except:
                    pass
        return v

    def parse(self):
        for l in self.next():
            matches = PT_S.findall(l)
            if matches:               
                for __, k, v in matches:
                    if k not in self.kv:
                        self.kv[k] = []
                    self.kv[k].append(v)
            matches = PT_E.findall(l)
            if matches:
                for i, v in enumerate(matches):
                    if '=' in v: 
                        continue
                    si = str(i)
                    if si not in self.kv:
                        self.kv[si] = []
                    self.kv[si].append(v)
        ### turn into np array of ints or floats if possible
        for k,v in self.kv.items():
            self.kv[k] = Statter.__totype(v)
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

class IOStatter(Statter):
    def __init__(self, stream):
        super(IOStatter, self).__init__()
        self.stream = stream

    def next(self):
        for line in self.stream:
            yield line


# st = StrStatter(["RECALL   = +0.7 +/- 0.102598 something=nothing, space=0.3, time=0.00085","RECALL=-3", "T=4","T=Zot"])
# st.print()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d",'--delimiter', default=None)
    ap.add_argument('--currency',action='store_true', default=False)
    ap.add_argument('-f', default=None)
    ap.add_argument('infile', nargs='?', 
        type=argparse.FileType('r'),
        default=sys.stdin)

    args = ap.parse_args()
    if args.currency:
        currency = True
        if args.delimiter is None:
            setDelimiter('\t')
    if args.delimiter is not None:
        setDelimiter(args.delimiter)

    stats = IOStatter(args.infile)

    if args.f is None:
        stats.print()
    else:
        stats.print(args.f.split(','))
