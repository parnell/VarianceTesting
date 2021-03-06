#!/usr/bin/env python3
import sys
import re
import collections

def key(line):
    s = line.split('\t')
    try:
        k = '{}_{}_{}_{}_{}'.format(
            s[0], # dim
            s[1], # size
            s[2], # K
            s[3], # var
            s[4] # nclus
            )
        return k
    except:
        print('failed', line, file=sys.stderr)
        return ''

if __name__ == "__main__":
    '''timestamp(0) Dim(1)	Size(2)	K(3)	Var(4)	Nclus(5)
        IdxName(6)	Cost(7)	Average(8) QueryTime(9)
        Average Calcs(10)	Precision(11)	Recall(12)
    '''
    files = []
    ks = {}
    lines = collections.OrderedDict()
    for f in sys.argv[1:]:
        n = f.split('_')[-1]
        n = re.sub(r'\D','',n)
        ks[n] = f
    bad = []
    for k in sorted(ks):
        # print(k,ks[k])
        for line in open(ks[k]):
            m = re.search('statline',line)
            if m:
                vals = line.split('\t')
                cost = float(vals[7])
                if cost > 0:
                    lines[key(line)] = line
                else:
                    bad.append(line)

    for line in bad:
        print('bad', line, end='')
    print("#########################################\n\n\n\n")
    for line in lines.values():
        print(line, end='')

