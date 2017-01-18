#!/usr/bin/env python3
import math
import statistics
import os
import re
import collections
from collections import OrderedDict
import traceback
import sys
import argparse
import locale
locale.setlocale(locale.LC_ALL, '')

try:
    import numpy as np
    from scipy import stats as scipystats
    numpy=True
except:
    numpy=False

currency=False


class Analyzer():
    def __init__(self, data):
        self.data = data

class Statter():
    def __init__(self):
        self.kv = collections.OrderedDict()
        self.isparsed = False
        self.defaults= {}
        self.print_precision = 4
        self.exclude_kvs = None
        self.exclude_lines = None
        self.include_kvs = None
        self.include_lines = None
        self.tail = None
        self.head = None
        self.colheaders = False
        self.headers = None
        self.linregress=True
        self.ikeys = None
        self.ekeys = None
        self.delimiter = None
        self.ddelimiter = None
        self.remove = None
        ## only use the first value
        ## useful for removing units etc. Example: 45 (seconds),becomes 45
        self.firstvalue = False
        self.trimkeywhitespace = True
        self.setDelimiter(',\t')

    def setDelimiter(self, d, kvsep='='):
        wsns = r'\n\r\f\v' if '\t' in d else r'\s' ## whitespace (but with space)
        wsb = r'[ \n\r\f\v]' if '\t' in d else r'\s' ## whitespace in brackes
        exp = r"({}*([^{}{}{}]+){}*{}{}*([^{}{}]*))".format(
            wsb,wsns,d,kvsep,wsb,kvsep,wsb,wsns,d)
        # print(exp)
        self.PT_S = re.compile(exp)
        self.PT_E = re.compile(r"{}*([^{}{}]+){}*".format(
            wsb, wsns, d, wsb))
        # PT_E = re.compile(r"([^\t]+)".format())
        # print(PT_E)
        self.delimiter = d
        self.ddelimiter = '{}{}'.format(self.delimiter,self.delimiter)

    def next(self):
        '''
        Overwrite with subclass
        '''
        pass

    def get(self, key, method=None):
        if not self.isparsed:
            self.parse()
        if method is not None:
            return method(self.kv[key])
        return self.kv[key]

    def getf(self, key, typ = None):
        """
        get first value from key
        """
        v = self.get(key)[0]
        return v if typ is None else typ(v)

    def getfv(self, key, typ = None):
        """
        get first value from key, from first split
        """
        v = self.get(key)[0].split(' ')[0]
        return v if typ is None else typ(v)


    def setExclude(self, line):
        self.exclude_kvs = []
        self.exclude_lines = []
        self._setIE(line, self.exclude_kvs, self.exclude_lines)
        if len(self.exclude_kvs) ==0: self.exclude_kvs=None
        if len(self.exclude_lines) ==0: self.exclude_lines=None

    def setInclude(self, line):
        self.include_kvs = []
        self.include_lines = []
        self._setIE(line, self.include_kvs, self.include_lines)
        if len(self.include_kvs) ==0: self.include_kvs=None
        if len(self.include_lines) ==0: self.include_lines=None

    def _setIE(self, line, kvs, ls):
        matches = self.PT_S.findall(line)
        if matches:
            for m in matches:
                ptk = re.compile(m[1])
                ptv = re.compile(m[2])
                kvs.append((ptk, ptv))
        matches = self.PT_E.findall(line)
        if matches:
            for m in matches:
                if '=' in m:
                    continue
                ptk = re.compile(m)
                ls.append(ptk)

    def __formatPrint(self, a):
        fmtarray = []
        for x in a:
            try:
                if float(x).is_integer():
                    fmtarray.append("{}")
                else:
                    fmtarray.append('{:.%df}'%self.print_precision)
            except:
                fmtarray.append('{:.%df}'%self.print_precision)
        s = "tsum={}\tmean={}\tmin={}\tmax={}\tstddev={}"
        if numpy and self.linregress:
            s += '\tslope={}\tintercept={}\trvalue={}\tpvalue={}\tstderr={}'
        s = '{} :\tn={}\t'+s.format(*fmtarray)
        return s

    @staticmethod
    def mean(v):
        return v.mean() if numpy and not isinstance(v,list) else statistics.mean(v)

    @staticmethod
    def var(v):
        try: return statistics.stdev(v) if len(v) > 1 and sum(v) != 0 else math.nan
        except: return math.nan

    def print(self, ikeys=None, icols=None, iranges=None):
        if not self.isparsed:
            self.parse()
        for idx, (k,v) in enumerate(self.kv.items()):
            if icols is not None and (idx+1) not in icols \
                    or ikeys is not None and not k in ikeys:
                continue
            if iranges is not None:
                found = False
                for r in iranges:
                    if idx+1 in r:
                        found = True
                        break
                if not found:
                    continue
            # if self.ekeys and re.match(self.ekeys
            try:
                if self.head:
                    v = v[:self.head]
                if self.tail:
                    v = v[-self.tail:]
                n = v.shape[0] if numpy and not isinstance(v,list) else len(v)
                if n == 0:
                    print(k,":",v)
                    continue
                mean = Statter.mean(v)
                var = Statter.var(v)
                a = [n, sum(v), mean, min(v), max(v), var]
                # if currency:
                #     a = [ locale.currency(val, grouping=True) for val in v]
                if n > 1:
                    if numpy and self.linregress:
                        try:
                            x = [i for i in range(n)]
                            a2 = scipystats.linregress(x,v)
                            a.extend(list(a2))
                        except:
                            traceback.print_exc()
                    fmt = self.__formatPrint(a[1:])
                    # fmt = self.__formatPrint(a)

                    s = fmt.format(k, *a)
                    print(s)
                else:
                    print(k,":",v[0])
            except TypeError:
                if len(v) > 10:
                    print(k,': [',*v[0:5],"...",*v[-5:],']')
                else:
                    print(k,":",v)
            except:
                if len(v) > 10:
                    print(k+'*',': [',*v[0:5],"...",*v[-5:],']')
                else:
                    print(k+'*',":",v)
                traceback.print_exc()

    @staticmethod
    def __v2bool(v):
        if v.lower() in ('true', 't','yes'):
            return True
        elif v.lower() in ('false', 'f','no'):
            return False
        raise TypeError("%r is not a bool"%v)

    @staticmethod
    def __totype(v):
        try:
            return [Statter.__v2bool(x) for x in v]
        except:
            pass
        if currency:
            try:
                v = [ locale.atof(val.replace('$','')) for val in v]
            except:
                pass
        if numpy:
            a = np.array(v)
            try:
                return a.astype(int)
            except:
                try:
                    return a.astype(float)
                except:
                    pass
        else:
            try:
                return [int(x) for x in v]
            except:
                try:
                    return [float(x) for x in v]
                except:
                    pass
        return v

    def _exclude(self, key, value):
        for k,v in self.exclude_kvs:
            if (v is None and k.match(key)) \
                or (v is not None and k.match(key) and v.match(value)):
                return True
        return False

    def _include(self, key, value):
        for k,v in self.include_kvs:
            # print('v==', key,value, k.match(key), v.match(value), k, v)
            if (v is None and k.match(key)) \
                or (v is not None and k.match(key) and v.match(value)):
                return True
        return False

    def _getmatches(self, line, idx):
        if self.exclude_lines:
            for r in self.exclude_lines:
                # print(r, line, r.match(line))
                if r.search(line) is not None:
                    return None
        if self.include_lines:
            for r in self.include_lines:
                if r.search(line) is None:
                    return None
        # print('--', line.strip(), self.exclude_kvs)

        if re.search(self.ddelimiter,line):
            # print(line)
            line = re.sub(self.ddelimiter,self.delimiter[0]+chr(0)+self.delimiter[0],line)
        matches = self.PT_S.findall(line)
        kvs = {}
        shouldInclude = True if not self.include_kvs else False
        if matches:
            for __, k, v in matches:
                if self.remove is not None:
                    v = self.remove.sub('',v)
                if self.trimkeywhitespace and ' ' in k:
                    k = k.strip()
                if self.exclude_kvs and self._exclude(k,v):
                    return None
                if not shouldInclude and self.include_kvs and self._include(k,v):
                    shouldInclude = True
                if self.firstvalue and ' ' in v:
                    v = v.split(' ')[0]
                if k not in kvs:
                    kvs[k] = [v]
                else:
                    kvs[k].append(v)
        matches = self.PT_E.findall(line)
        # print(matches)

        if matches:
            if self.colheaders and idx==0:
                self.headers = matches
                return None
            for i, v in enumerate(matches):
                if '=' in v or v== chr(0):
                    continue
                si = str(i) \
                    if not self.colheaders or i >= len(self.headers) \
                    else self.headers[i]
                if self.exclude_kvs and self._exclude(si,v):
                    return None
                if not shouldInclude and self.include_kvs and self._include(si,v):
                    shouldInclude = True
                if self.remove is not None:
                    v = self.remove.sub('',v)
                if si not in kvs:
                    kvs[si] = [v]
                else:
                    kvs[si].append(v)
        return kvs if shouldInclude else None

    def parse(self):
        dicts = []

        for i,l in enumerate(self.next()):
            m = self._getmatches(l, i)
            if m:
                dicts.append(m)
        if not self.colheaders:
            keys = set()
            for d in dicts:
                keys |= d.keys()
        else:
            keys = self.headers
        # print('keys', keys)
        # print([ (k,[]) for k in keys])
        # k:[] for k in keys
        self.kv = OrderedDict([ (k,[]) for k in keys])
        el = [] # empty list
        for k in keys:
            [self.kv[k].extend(d.get(k,el)) for d in dicts]

        ### turn into np array of ints or floats if possible
        for k,v in self.kv.items():
            self.kv[k] = Statter.__totype(v)
        self.isparsed = True

class FileStatter(Statter):
    def __init__(self, *filenames):
        super(FileStatter, self).__init__()
        self.filenames = []
        for t in filenames:
            if isinstance(t, list):
                for fn in t:
                    if not os.path.exists(fn):
                        raise FileNotFoundError(fn)
                    self.filenames.append(fn)
            else:
                if not os.path.exists(t):
                    raise FileNotFoundError(t)
                self.filenames.append(t)


    def next(self):
        for fn in self.filenames:
            for line in open(fn):
                yield line

class StrStatter(Statter):
    def __init__(self, val):
        super(StrStatter, self).__init__()
        self.val = val

    def next(self):
        if not isinstance(self.val, list):
            splits = re.split(r'[\r\n]',self.val)
            for split in splits:
                yield split
        else:
            for line in self.val:
                splits = re.split(r'[\r\n]',line)
                for split in splits:
                    yield split


def __setarraysplit(line):
    ranges = line.split(',')
    a = []
    v = set()
    for r in ranges:
        if '-' in r:
            b, e = r.split('-')
            a.append(range(int(b), int(e)))
        else:
            v.add(int(r))
    if len(a) == 0:
        a = None
    if len(v) == 0:
        v = None
    return v,a


class IOStatter(Statter):
    def __init__(self, stream):
        super(IOStatter, self).__init__()
        self.stream = stream

    def next(self):
        for line in self.stream:
            yield line
# s = 'Race ID	Session ID	Total Races\n1\t2\t3'
# s = 'time=45.36 (s)'
# st = StrStatter(s)
# st.firstvalue = True
# # st.colheaders = True
# st.print()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d",'--delimiter', default=None)
    ap.add_argument("-s",'--key-value-separator', default="=")
    ap.add_argument('--currency',action='store_true', default=False)
    ap.add_argument('-k', default=None, help='print only the specified keys')
    ap.add_argument('-f', default=None, help='print only the specified columns')
    ap.add_argument('--print-precision', default=4)
    ap.add_argument('--exclude',default=None, help='exclude lines that contain regex search')
    ap.add_argument('--include',default=None, help='only include lines that contain regex search')
    ap.add_argument('--ikeys',default=None, help='only include k,v pair that contain regex match')
    ap.add_argument('--ekeys',default=None, help='exclude k,v pair that contain regex match')
    ap.add_argument('--head',default=None, type=int, help='print only first x stats')
    ap.add_argument('--tail',default=None, type=int, help='print only the last x stats')
    ap.add_argument('--remove',default=None, help='remove chars from values with the given regex')
    ap.add_argument('--linregress',action='store_true', default=False)
    ap.add_argument('--colheaders',action='store_true', default=False,
                    help='Column names given from header')
    ap.add_argument('infile', nargs='?',
                    type=argparse.FileType('r'),default=sys.stdin)

    args = ap.parse_args()
    stats = IOStatter(args.infile)
    if args.currency:
        currency = True
        if args.delimiter is None:
            stats.setDelimiter('\t')
    if args.delimiter is not None:
        stats.setDelimiter(args.delimiter, args.key_value_separator)

    stats.tail = args.tail
    stats.head = args.head
    stats.print_precision = args.print_precision
    stats.linregress = args.linregress
    stats.colheaders = args.colheaders
    stats.ikeys = args.ikeys
    stats.ekeys = args.ekeys
    if args.remove is not None:
        stats.remove = re.compile(args.remove)
    if numpy:
        np.set_printoptions(precision=args.print_precision)
    if args.exclude:
        stats.setExclude(args.exclude)
    if args.include:
        stats.setInclude(args.include)
    includekeys = None if args.k is None else set(args.k.split(','))
    includecols, includeranges = None, None
    if args.f is not None:
        includecols, includeranges = __setarraysplit(args.f)
    stats.print(includekeys, includecols, includeranges)
