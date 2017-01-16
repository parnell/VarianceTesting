import numpy as np
# import matplotlib.pyplot as plt
from scipy import stats
from scipy import integrate
# from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import os
import sys
import glob
# import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
# %matplotlib inline
# %precision 4
# plt.style.use('ggplot')

def int1(kernel, x1, y1):
    # Sample KDE distribution
    sample = kernel.resample(size=100)

    include = (sample < np.repeat([[x1],[y1]],sample.shape[1],axis=1)).all(axis=0)
    integral = include.sum() / float(sample.shape[1])
    return integral

def expon_pdf(x, lmabd=1):
    """PDF of exponential distribution."""
    return lmabd*np.exp(-lmabd*x)

def expon_cdf(x, lambd=1):
    """CDF of exponetial distribution."""
    return 1 - np.exp(-lambd*x)

def expon_icdf(p, lambd=1):
    """Inverse CDF of exponential distribution - i.e. quantile function."""
    return -np.log(1-p)/lambd

def main():
    x = 10000
    data = np.random.normal(0, 1, (1,x))
    kernel = stats.gaussian_kde(data)
    sample = kernel.resample(size=x*5)
    print(kernel, sample.shape, data.shape)

    # Define the threshold point that determines the integration limits.
    # print(int1(data,-10,-10))
    print(int1(kernel,-10,-10))
    # bar(x, np.array(data.shape[1]))
    # plot(x)
    # show()
    dist = stats.expon()
    x = np.linspace(0,4,100)
    y = np.linspace(0,1,100)

    with plt.xkcd():
        plt.figure(figsize=(12,4))
        plt.subplot(121)
        plt.plot(x, expon_cdf(x))
        plt.axis([0, 4, 0, 1])
        for q in [0.5, 0.8]:
            plt.arrow(0, q, expon_icdf(q)-0.1, 0, head_width=0.05, head_length=0.1, fc='b', ec='b')
            plt.arrow(expon_icdf(q), q, 0, -q+0.1, head_width=0.1, head_length=0.05, fc='b', ec='b')
        plt.ylabel('1: Generate a (0,1) uniform PRNG')
        plt.xlabel('2: Find the inverse CDF')
        plt.title('Inverse transform method')

        plt.subplot(122)
        u = np.random.random(10000)
        v = expon_icdf(u)
        plt.hist(v, histtype='step', bins=100, normed=True, linewidth=2)
        plt.plot(x, expon_pdf(x), linewidth=2)
        plt.axis([0,4,0,1])
        plt.title('Histogram of exponential PRNGs')
        plt.show()

if __name__ == "__main__":
    main()
