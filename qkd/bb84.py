import numpy as np
import QKDTools as tools
import qit
import random

def encodeBit(bit, basis):
    q = qit.state('0')

    if bit == 1:
        #Pauli-X gate maps |0> to |1> and |1> to |0>
        q = q.u_propagate(qit.sx)
    if basis == 'X':
        #Hadamard gate maps |0> to 1/sqrt(2) [|0> + |1>] and |1> to 1/sqrt(2) [|0> - |1>]
        q = q.u_propagate(qit.H) 

    return q

def encode(bits, bases):
    encodedBits = []
    for i in range(len(bits)):
        encodedBits.append(encodeBit(bits[i], bases[i]))

    return encodedBits

def decodeQubit(bit, basis):
    if basis == 'X':
        bit = bit.u_propagate(qit.H)

    _, result = bit.measure()

    return result

def decode(bits, bases):
    decodedMessage = []
    for i in range(len(bits)):
        decodedMessage.append(decodeQubit(bits[i], bases[i]))
    
    return decodedMessage

def eavesdrop(bit, basis):
    result = decodeQubit(bit, basis)
    return encodeBit(result, basis)

def flipState(state):
    """
    |Z+> <-> |Z->
    |X+> <-> |X->
    """
    if tools.equals(state, qit.state('0')) or tools.equals(state, qit.state('1')):
        return state.u_propagate(qit.sx)
    else:
        return state.u_propagate(qit.sz)


def generateNoise(bits, rate):
    for i in range(len(bits)):
        randomNum = random.uniform(0,1)
        if randomNum <= rate:
            bits[i] = flipState(bits[i])

    return bits


