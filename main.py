import numpy as np
import pandas as pd
from random import random
import objFunction as op 
import time as time
from joblib import Parallel, delayed

# import different mutator
import uniformFlipOriginalSteps as func

# This is the main file testing the (1+1) EA with uniform flip original steps
# optimizing interger-valued OneMax function with different target position r
# input: dimension: n, a set of r: R, number of independent runs: numberOfRuns
# output: optimization process (optional), datafram: process, runtime: t

NUM_WORKERS = 20
n = 40
R = [2**i for i in range (3,20)]
# R = [10]
# N = np.arange(10,100,10)
f = op.fitness
numberOfRuns = 51

def main(n,r,f,it):
    x = r*np.ones(n,dtype = np.int64)
    stepList = func.generate_step_list()
    opt = np.zeros(n,dtype = np.int64)
    # Y is the fitness at each iteration
    Y = [f(x,opt)]
    # YY is to log the integer string for each iteration
    YY = []
    t = 0
    start = time.time()
    while Y[-1] !=0:
        f_x = Y[-1]
        y = []
        for idx in range(n):
            if random()<1/n:
                flip = random()
                i = func.manipulate_integer(flip,x[idx],stepList)
                y.append(i)
            else:
                y.append(x[idx])
        f_y = f(y,opt)
        #print(f'after mute fitness {f_y} with string {y}')
        if f_y<=f_x:
            #print(f'at {t} make a progress')
            YY.append(y)
            x = y
            Y.append(f_y)
        else:
            YY.append(x)
            Y.append(f_x)
            pass
        t+=1
    end = time.time()
    print(f'for n = {n}, r = {r}, {it}runs take {end-start} physical time with {np.log10(t)} time')
    if it == 0:
        processDf = pd.DataFrame(data = {'t': np.arange(0,t+1,1),'fitness':Y})
        #flipY = pd.DataFrame(YY)
        #flipY.to_csv(f'string_{n}n_{np.log10(r)}r_{it}.csv')
        processDf.to_csv(f'process__{n}n_{np.log2(r)}r_{it}.csv')
    endDf = pd.DataFrame(data = {'it': it,'time':[t]})
    endDf.to_csv(f'{n}n_{np.log2(r)}r_{it}.csv')
    return -1


Parallel(n_jobs=NUM_WORKERS)(delayed(main)(n,r,f,it) for r in R for it in range (0,numberOfRuns))
