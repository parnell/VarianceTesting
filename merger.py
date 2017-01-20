import sys



if __name__ == "__main__":
    files = []
    ks = {}
    for f in sys.argv:
        ks[f.split('_')[-1]] = f
    for k in sorted(ks):
        print(k)
