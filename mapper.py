from multiprocessing import Pool, cpu_count

def pmap(func, arglist, distributed=True):
    '''
    Wrapper around the Pool.map function
    Allows for non distributed runs for debugging
    or for use of packages that don't play well with
    multiprocessing (I'm looking at you nltk)
    '''
    if not distributed or len(arglist) == 1:
        results = []
        for arg in arglist:
            results.append(func(arg))
        return results
    else:
        with Pool(cpu_count()) as p:
            return p.map(func, arglist)
