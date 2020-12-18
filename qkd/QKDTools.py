import numpy as np
import qit
from numpy.random import randint
import time
from random import sample
import math

seed = int(time.time())
np.random.seed(seed = seed)

def generateBits(N):
    return randint(2,size=N)

def generateBases(N): 
    randomList = randint(2, size = N)
    bases = []
    
    for i in range(0, N):
        if randomList[i] == 0:
            bases.append("X")
        else:
            bases.append("Z")
        
    return bases

def sift_bits(bits, bases, other_bases):
    key = []
    key_for_print = []

    for i in range(len(bits)):
        if bases[i] == other_bases[i]:
            key.append(bits[i])
            key_for_print.append(str(bits[i]))
        else:
            key_for_print.append(' ')

    return key, key_for_print

def discloseBits(alice_bits, bob_bits):
    temp = np.arange(0, len(alice_bits))
    subsetSize = int(len(temp) // 2)

    subset = sample(list(temp), subsetSize)
    subset.sort()       

    alice_key = []
    bob_key = []

    alice_disclosed = []
    bob_disclosed = []

    for i in subset:
        alice_disclosed.append(alice_bits[i])
        bob_disclosed.append(bob_bits[i])

    for i in range(len(alice_bits)):
        if i in subset:
            pass
        else:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_bits[i])

    error = calculateError(alice_disclosed, bob_disclosed)
    
    return alice_key, bob_key, error

def equals(stateA, stateB):
    return (stateA.prob() == stateB.prob())[0]

def calculateError(bitsA, bitsB):
    flippedBits = 0
    for i in range(len(bitsA)):
        if bitsA[i] != bitsB[i]:
            flippedBits += 1

    return flippedBits / len(bitsA)

def list_to_string(lst):
    return ''.join(str(i) for i in lst)


