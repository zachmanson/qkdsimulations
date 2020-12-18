import matplotlib.pyplot as plt
import simulateQKD as sim 
import numpy as np

def plotKeyLength(N, error_rate):
    numBits = np.arange(10, N + 1)

    keyLength = []

    for i in numBits:
        lenKeyTemp = []
        count = 0
        while True:
            alice_key, bob_key = sim.simulateBB84(i, error_rate = error_rate, eve = False, eavesdrop_rate = 1.0, detailed = False)
            if alice_key[0] != 'terminated':
                lenKeyTemp.append(len(alice_key))
                count += 1

            if count == 10:
                break

        keyLength.append(sum(lenKeyTemp)/len(lenKeyTemp))


    plt.figure()
    plt.plot(numBits, keyLength)
    plt.xlabel('Number of initial bits')
    plt.ylabel('Average length of key')
    plt.grid(True)
    plt.savefig('keylength.png')

def plotEveSuccess(N, eavesdrop_rate, error_rate):
    numBits = np.arange(16, N + 1)
    eveSuccess = []
    
    for i in numBits:
        eveSuccessTemp = []
        for j in range(0, 100):
            count = 0
            while True:
                alice_key, bob_key = sim.simulateBB84(i, eve = True, eavesdrop_rate =
                        eavesdrop_rate, error_rate = error_rate, detailed = False)
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


def plot_var_eve_rate(N, error_rate):
    success = []
    eve_rate = np.linspace(0.1, 1.0, 100)
    for i in range(len(eve_rate)):
        success_temp = []
        for j in range(0, 1000):
            count = 0
            while True:
                alice_key, bob_key = sim.simulateBB84(64, eve = True, eavesdrop_rate = eve_rate[i],
                        error_rate = error_rate, detailed = False)
                count+=1

                if alice_key[0] == 'aborted' and bob_key[0] == 'aborted':
                    break

            success_temp.append(1/count)
        success.append(sum(success_temp)/len(success_temp))

    plt.figure()
    plt.plot(eve_rate, success)
    plt.xlabel('Eavesdrop Rate')
    plt.ylabel('Chance Eve is noticed')
    plt.grid(True)
    plt.savefig('vareve.png')

