from mpmath import nsum,inf,log
import numpy as np
import pandas as pd
from random import random


# first we calculate the converging value for the constant 
def cons(x):
    #notice here the episilion need to be reconsidered, 
    #here is an exampler value. We choose 0.001 for linear step size because this will have the maximum number of steps (67). This is due to the precision of Python 3
    # as for 
    eq = 0.001 
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
     # here the range is 30 is because of the precision limit of python if we take the exponential step size. If it is linear, it will be 67
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

# This is the function for each bit flip or not
def manipulate_integer(flip,i,df):
    if flip> df.iloc[-1]['pr']: # if the flip probability is larger than the possible probability, nothing happen
        j = 0
    else:
        idx = np.min(np.where(flip < df['pr']))
        j = df['i'][idx]
    # flip the coin the third time to decide plus or minus
    if random()<0.5:
        i += j
    else:
        i -= j
    return i
