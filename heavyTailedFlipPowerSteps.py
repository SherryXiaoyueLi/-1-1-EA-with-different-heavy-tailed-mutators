import numpy as np
import pandas as pd
import math
from random import random, randrange
from mpmath import nsum,inf,log

def hurdle_bit(x,w):
#     first we find which integer position has the odd number
    originalX = x.copy()
    idxList = np.where(x*np.mod(x,w))[0]
    for i in range(len(idxList)):
        x[idxList[i]]-= w
        # print(x[idxList[i]])
    l = []
    for i in x:
        l.append(math.ceil(i/w))
    return originalX, sum(l)

# def newHurdle(x,w):
#     l = []
#     for j in range (len(x)):
#         i = x[j]
#         l.append(abs(-math.ceil(i/w) - math.ceil(np.mod(i,w)/w)))
#     return sum(l)
def newHurdle(x,w):
    n = len(x)
    l = []
    for j in range (len(x)):
        i = x[j]
        l.append(abs(-math.ceil(i/w)+ math.ceil(np.mod(i,w)/w))+np.count_nonzero(x)/n)
    return sum(l)
def newHurdle_noPlateu(x,w):
    l = []
    for j in range (len(x)):
        i = x[j]
        l.append(abs(-math.ceil(i/w) - np.mod(i,w)/w))
    return sum(l)

def newHurdle_withTrap(x,w):
    l = []
    for j in range (len(x)):
        i = x[j]
        l.append(abs(-math.ceil(i/w)-np.mod((w-i),w)/w))
#     print(l)
    return sum(l)
# things to change
def sample_heavyTail(n):
    select_k_list = np.arange(0,math.ceil(np.log2(n)),1, dtype = np.int64)
    k = np.random.choice(select_k_list)
    # print(k)
    number_of_bit_change = n+1
    # print(f'before {number_of_bit_change}')
    while number_of_bit_change > n:
        uniformChooseOther =  np.random.choice(2**k)
        number_of_bit_change = 2**k + uniformChooseOther - 1 
        # print(f'end {number_of_bit_change}')
    return number_of_bit_change

def doubleHeavyTailedMutator(n,a,x):
    num_bits_to_change = sample_heavyTail(n) # number of integer in the string we change
    # instead choose element, choose index
    idxRandomSelectBit = np.random.choice(n,size = num_bits_to_change) # u.a.r choose num_bits_integer in the string
    # print(f'{idxRandomSelectBit} bits need to change')
    y = x.copy()
    # print(f'before {y}')
    ST = []
    for i in idxRandomSelectBit:
        # here we let the parameter of pareto distribution as 1, a = 1
        step = math.floor(1/np.random.power(a))
        # print(step)
        ST.append(step)
        if random()<0.5:
            # print(f'for {i} + step')
            y[i] = y[i] + step
        else:
            # print(f'for {i} - step')
            y[i] = y[i] - step
    # print(f'after {y}')
    if len(idxRandomSelectBit) == 0:
        ST.append(0)
    return y, x, ST
