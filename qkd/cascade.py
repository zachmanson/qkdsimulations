from random import randint
import time

seed = int(time.time())

def shuffle(bits):
    shuffleIndex = []
    shuffledBits = [None] * len(bits)
    for i in range(len(bits)):
        tempIndex = randint(0, len(bits) - 1)
        if tempIndex in shuffleIndex:
            while True:
                tempIndex = randint(0, len(bits) - 1)
                if tempIndex not in shuffleIndex:
                    break

        shuffledBits[i] = bits[tempIndex]
        shuffleIndex.append(tempIndex)

    return [shuffledBits, shuffleIndex]

def createTLBlock(bits, i, errorRate):
    size = getTLBlockSize(i, errorRate)
    TLBlocks = [bits[j * size:(j + 1) * size] for j in range((len(bits) + size - 1) // size)]
    return TLBlocks

def getTLBlockSize(i, errorRate):
    k1 = int(0.73 / errorRate)

    if(i > 0):
        k2 = 2 * k1
        if(i > 1):
            k3 = 2 * k2
            if(i > 2):
                k4 = 2 * k3
                return k4
            return k3
        return k2
    return k1

def getParity(bits):
    return sum(bits) % 2

def getCorrectParity(aliceBits, indices):
    return sum(aliceBits[i] for i in indices) % 2

def getErrorParity(bits, aliceBits, indices):
    return (getParity(bits) + getCorrectParity(aliceBits, indices)) % 2

def split(block):
    middleIndex = (len(block) // 2) + (len(block) % 2)
    return block[:middleIndex], block[middleIndex:]

def flip(bits, index):
    if bits[index] == 0:
        bits[index] = 1
    else:
        bits[index] = 0

def runCascade(aliceBits, bobBits, errorRate):
    shuffledPermutations = []
    shuffledIndexPermutations = []
    errorIndices = []

    for i in range(0, 4):
        if i == 0:
            shuffledPermutations.append(bobBits)
            shuffledIndexPermutations.append([i for i in range(len(bobBits))])
        else:
            a, b = shuffle(bobBits)
            shuffledPermutations.append(a)
            shuffledIndexPermutations.append(b)

        TLBlocks = createTLBlock(shuffledPermutations[i], i, errorRate)
        TLBlocksIndex = createTLBlock(shuffledIndexPermutations[i], i, errorRate)


        for j in range(len(TLBlocks)):
            if getErrorParity(TLBlocks[j], aliceBits, TLBlocksIndex[j]) == 1:
                errorIndex = binaryAlgorithm(TLBlocks[j], TLBlocksIndex[j], aliceBits)
                errorIndices.append(errorIndex)
                flip(bobBits, errorIndex)

                for k in reversed(range(0, i)):
                   TLBlocks = createTLBlock(shuffledPermutations[k], k, errorRate)
                   TLBlocksIndex = createTLBlock(shuffledIndexPermutations[k], k, errorRate)

                   for l in range(len(TLBlocks)):
                       if getErrorParity(TLBlocks[l], aliceBits, TLBlocksIndex[l]) == 1:
                           errorIndex = binaryAlgorithm(TLBlocks[l], TLBlocksIndex[l], aliceBits)
                           errorIndices.append(errorIndex)
                           flip(bobBits, errorIndex)

    errorIndices.sort()

    alicePrivateKey = []
    bobPrivateKey = []

    for i in range(0, len(aliceBits)):
        if i in errorIndices:
            pass
        else:
            alicePrivateKey.append(aliceBits[i])
            bobPrivateKey.append(bobBits[i])

    return alicePrivateKey, bobPrivateKey


def binaryAlgorithm(block, indices, aliceBits):
    left, right = split(block)
    leftIndex, rightIndex = split(indices)

    if len(right) == 0:
        return leftIndex[0]
    elif len(left) == 1 and getErrorParity(left, aliceBits, leftIndex) == 1:
        return leftIndex[0]
    elif len(right) == 1 and getErrorParity(right, aliceBits, rightIndex) == 1:
        return rightIndex[0]
    else:
        if getErrorParity(left, aliceBits, leftIndex) == 1:
            return binaryAlgorithm(left, leftIndex, aliceBits)
        else:
            return binaryAlgorithm(right, rightIndex, aliceBits)

