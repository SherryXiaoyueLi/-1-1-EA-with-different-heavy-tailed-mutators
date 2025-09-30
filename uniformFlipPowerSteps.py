import numpy as np
from random import random
import math

####### Notes #################

# This is the function for each bit flip or not
def manipulate_integer(flip,i,df):
    if flip > df.iloc[-1]['pr'] or flip < df.iloc[0]['pr']: # if the flip probability is larger than the possible probability,
        #  or smaller than the lowest, we let the step size be 1
        j = 1
    else:
        idx = np.min(np.where(flip < df['pr']))
        j = df['i'][idx]
    # flip the coin the third time to decide plus or minus
    if random()<0.5:
        i +=j
    else:
        i -= j
    return i


def manipulateEachBit(x,n,a):
    y = []
    for idx in range(n):
        if random()<1/n:
            step = math.floor(1/np.random.power(a))
            if random()<0.5:
                y.append(x[idx] + step)
            else:
                y.append(x[idx] - step)
            
        else:
            y.append(x[idx])
    return y

