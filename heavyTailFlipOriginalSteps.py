from mpmath import nsum,inf,log
import numpy as np
import pandas as pd
from random import random
import math

####### Notes #################
# For the hurdle function, following things are changed. 
# - The step size is linearly distributed rather than exponential to 2
# - The epsilon value changes to 0.001

# first we calculate the converging value for the constant 
def cons(x):
    eq = 0.001 #notice here the episilion need to be reconsidered, here is an exampler value
    bottom = (x+2)*(log(x+2)**(1+eq))
    return 1/bottom

# This function generate a dataframe which contains the step size with its related probability
# input: the converging function
# output: a dataframe helping for deciding the step size according to probability
# a dataframe contains two column: "i":step size; "pr": probability, which is the upper bound of the 
# compared probability. In our algorithm, we compare the random generated probability to all df['pr'] and select the 
# smallest df['df'] related step size. 
# generated probability is smaller than the smallest of all df['pr'] value. 
def generate_step_list():
    c = float(nsum(cons, [1, inf]))
    P = []
    eq = 0.001
     # here the range is 63 is because of the precision limit of python if we take the exponential step size. If it is linear, it will be 67
    for i in range(0,50):
    # for i in range(0,67):
        bottom = (i+2)*(log(i+2)**(1+eq))*c
        P.append(float(1/bottom))
    new = []
    for k in range (len(P)):
        new.append(sum(P[0:k+1]))
    i = [2**x for x in (np.arange(0,50,1, dtype = np.int64))] 
    # i = [x for x in (np.arange(1,68,1,dtype = np.int64))]
    new = []
    for k in range (len(P)):
        new.append(sum(P[0:k+1]))
    data = {'i':i,'pr':new}
    df = pd.DataFrame(data = data)
    return df

def manipulateEachBit(x,n,N,a,df,stepLists):
    # first we decide how many intergers need to be changed
    sampling = np.random.power(a)
    idx = np.min(np.where(sampling < df['l']))
    num_bits_to_change = N[idx-1]
    idxRandomSelectBit = np.random.choice(n,size = num_bits_to_change)
    y = x.copy()
    for i in idxRandomSelectBit:
        # here we let the parameter of pareto distribution as 1, a = 1
        flip = random()
        if flip> stepLists.iloc[-1]['pr']: # if the flip probability is larger than the possible probability, nothing happen
            step = 0
        else:
            idx = np.min(np.where(flip < stepLists['pr']))
            step = stepLists['i'][idx]
        # flip the coin the third time to decide plus or minus
        # print(step)
        if random()<0.5:
            y[i] = y[i] + step
        else:
            y[i] = y[i] - step
    return y


