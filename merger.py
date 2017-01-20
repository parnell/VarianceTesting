import sys
import re
import collections

def key(line):
    s = line.split('\t')
    try:
        print('{}_{}_{}_{}_{}'.format(
            s[0], # dim
            s[1], # size
            s[2], # K
            s[3], # var
            s[4] # nclus
            ))
    except:
        print('failed', line, file=sys.stderr)

if __name__ == "__main__":
    files = []
    ks = {}
    lines = collections.OrderedDict()
    for f in sys.argv:
        n = f.split('_')[-1]
        n = re.sub(r'\D','',n)
        ks[n] = f
    for k in sorted(ks):
        # print(k,ks[k])
        for line in open(ks[k]):
            m = re.search('statline',line)
            if m:
                lines[key(line)] = line

    for line in lines.values():
        print(line)
