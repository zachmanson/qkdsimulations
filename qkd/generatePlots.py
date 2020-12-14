import matplotlib.pyplot as plt
import simulateQKD as sim 
import numpy as np

def plotKeyLength(N, errorRate):
    numBits = np.arange(10, N + 1)

    keyLength = []

    for i in numBits:
        lenKeyTemp = []
        count = 0
        while True:
            alice_key, bob_key = sim.simulateBB84(i, errorRate = errorRate)
            if alice_key[0] != 'terminated':
                lenKeyTemp.append(len(alice_key))
                count += 1

            if count == 100:
                break

        keyLength.append(sum(lenKeyTemp)/len(lenKeyTemp))


    plt.figure()
    plt.plot(numBits, keyLength)
    plt.xlabel('Number of initial bits')
    plt.ylabel('Average length of key')
    plt.grid(True)
    plt.savefig('keylength.png')

def plotEveSuccess(N, eavesdropRate):
    numBits = np.arange(10, N + 1)
    eveSuccess = []
    
    for i in numBits:
        eveSuccessTemp = []
        for j in range(0, 100):
            count = 0
            while True:
                alice_key, bob_key = sim.simulateBB84(i, eve = True, eavesdropRate = eavesdropRate)
                count += 1

                if alice_key[0] == 'aborted' and bob_key[0] == 'aborted':
                    break

            eveSuccessTemp.append(1/count)

        eveSuccess.append(sum(eveSuccessTemp)/len(eveSuccessTemp))

    plt.figure()
    plt.plot(numBits, eveSuccess)
    plt.xlabel('Number of initial bits')
    plt.ylabel('Chance Eve is noticed')
    plt.grid(True)
    plt.savefig('evesuccess.png')

