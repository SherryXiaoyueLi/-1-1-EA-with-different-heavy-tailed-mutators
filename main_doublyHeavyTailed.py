import numpy as np
import pandas as pd
import math
from random import random, randrange
from mpmath import nsum,inf,log
import heavyTailFlipPowerSteps as func
from joblib import Parallel, delayed

# parameter setup

NUM_WORKERS = 20
f =func.newHurdle
n = 100
r = 100
W = [j for j in range (1,8)]
a = 0.5
numberOfRuns = 101

iX = []
# since we need 101 independent runs, we need each time initialized x the same, we first generate a lists of initialized x
for w in W:
    up = r-2*w
    down = r+2*w
    x = []
    for j in range (n):
        x.append(np.random.choice(np.arange(up,down, dtype = np.int64)))
    iX.append(x)
# print(f'intialized lists of x with different w is {iX}')
def main(w,n,iX,r,a,it):
    idx = W.index(w)
    x = iX[idx]
    # print(f'intialized x is {x}')
    f_x = f(x,w)
    Y = [f_x]
    YY = []
    yST = []
    t = 0
    while Y[-1] !=0:
        f_x = Y[-1]
        y,x,ST = func.doubleHeavyTailedMutator(n,a,x)
        # print(y,x,ST)
        yST.append(ST)
        f_y = f(y,w)
        # print(f_y)
        if f_y <= f_x:
            x = y
            Y.append(f_y)
            # YY.append(x)
        else:
            Y.append(f_x)
            # YY.append(x)
            # pass
        # if t % 100 == 0:
            # print(f'at {t} time fitness is {Y[-1]}')
        t+=1
    print(f'n = {n}, r is {r}, t/n is {t/n}={np.log10(t/n)}')
    # Some observation logging dataframe
    #if  it == 0:
        #processDf = pd.DataFrame(data = {'t': np.arange(0,t+1,1),'fitness':Y})
        # flipY = pd.DataFrame(YY)
        # flipY.to_csv(f'1StepAway_{n}n_{np.log2(r)}r_{it}.csv')
        #processDf.to_csv(f'process_{n}n_{r}r_{w}w_{it}.csv')
    #     dfYST = pd.DataFrame(yST)
    #     dfYST.to_csv(f'stepSize_{n}n_{np.log2(r)}r_{w}w_{it}.csv')
    endDf = pd.DataFrame(data = {'it': it,'time':[t]})     
    endDf.to_csv(f'{n}n_{a}a_{r}r_{w}w_{it}.csv')
    return -1

Parallel(n_jobs=NUM_WORKERS)(delayed(main)(w,n,iX,r,a,it) for w in W for it in range (0,numberOfRuns))
