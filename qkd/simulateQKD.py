import QKDTools as tools
import bb84
import numpy as np
from random import sample
import cascade
import table
import privacy_amplification
import PySimpleGUI as sg
import time 

def create_gui_and_run():
    sg.theme("DarkAmber")
    simulate_btn = sg.Button('Simulate')
    exit_btn = sg.Button('Exit')
    protocol_menu = sg.Combo(['BB84', 'E91 (To be implemented)', 'B92 (To be implemented)'], size = (40, 20), default_value = 'BB84')
    initial_bits_slider = sg.Slider(range = (16, 2048), orientation = 'h', size = (240, 20), default_value = 128)
    eve_rate_slider = sg.Slider(range = (0, 100), orientation = 'h', size = (240, 20), default_value = 100)
    error_rate_slider = sg.Slider(range = (0, 100), orientation = 'h', size = (240, 20), default_value = 20)
    eve_checkbox = sg.Checkbox('Eve Present', size = (20, 1), default = True)
    detailed_checkbox = sg.Checkbox('Detailed', size = (20, 1), default = True)
    output = sg.Output(font = ("Courier", 20), key = '-OUTPUT-', size = (130,30))

    layout = [
        [sg.Text('Protocol       '), protocol_menu],
        [sg.Text('Initial Bits   '), initial_bits_slider],
        [sg.Text('Eavesdrop Rate '), eve_rate_slider],
        [sg.Text('Error Rate     '), error_rate_slider],
        [eve_checkbox, detailed_checkbox],
        [simulate_btn, exit_btn],
        [output]
    ]

    window = sg.Window('QKD', layout)

    while True:
        event, values = window.read()
        protocol = list(values.values())[0]
        params = list(values.values())[1:]
        params[0] = int(params[0])
        params[1] /= 100
        params[2] /= 100

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Simulate':
            window['-OUTPUT-'].Update('')
            if protocol == 'BB84':
                simulateBB84(*params)
            elif protocol == 'E91':
                print('Not yet implemented')
            else:
                print('Not yet implemented')

    window.close()

def simulateBB84(N, eavesdrop_rate, error_rate, eve, detailed):
    alice_bits = tools.generateBits(N)
    alice_bases = tools.generateBases(N)

    if detailed:
        print(f'Alice randomly generates a set of {N} bits and bases')
        print("Alice's bits:\n", tools.list_to_string(alice_bits), sep='')
        print("Alice's bases:\n", tools.list_to_string(alice_bases), sep='')
        print('Alice encodes her bits using her basis choice, and sends the encrypted bits to Bob')
    
    alice_sent = bb84.encode(alice_bits, alice_bases)
    encoded_list = bb84.get_encoded_list(alice_bits, alice_bases)

    if detailed:
        print("Encoded qubit polarizations:\n", tools.list_to_string(encoded_list), sep = '')


    if eve:
        eve_bases = tools.generateBases(int(N * eavesdrop_rate))
        if detailed:
            print("Eve's bases (based on rate of eavesdropping):\n", tools.list_to_string(eve_bases), sep='')
            print("Eve will select a subset of Alice's encoded bits to measure using her bases choices, and then re-encode them to send to Bob.")

        tempEve = np.arange(0, len(alice_sent))
        subsetAlice_sent = sample(list(tempEve), len(eve_bases))
        subsetAlice_sent.sort()

        eveCount = 0
        for i in range(len(alice_sent)):
            if i in subsetAlice_sent:
                alice_sent[i] = bb84.eavesdrop(alice_sent[i], eve_bases[eveCount])

    if detailed:
        print("Noise is introduced into the system, flipping %.2f percent of Alice's sent qubits." % (error_rate * 100))

    alice_sent = bb84.generateNoise(alice_sent, error_rate)

    bob_bases = tools.generateBases(N)

    if detailed:
        print("Bob's bases:\n", tools.list_to_string(bob_bases), sep='')

    bob_bits = bb84.decode(alice_sent, bob_bases)

    if detailed:
        print("Bob's measured bits:\n", tools.list_to_string(bob_bits), sep='')
        print("Alice and Bob share their basis choices, and generate their own keys.")

    alice_sifted, alice_sifted_for_print = tools.sift_bits(alice_bits, alice_bases, bob_bases)
    bob_sifted, bob_sifted_for_print = tools.sift_bits(bob_bits, bob_bases, alice_bases)


    if detailed:
        print("Alice's sifted key:\n",tools.list_to_string(alice_sifted), sep='')
        print("Bob's sifted key:\n", tools.list_to_string(bob_sifted), sep='')
        print('Expected error: ', error_rate)
        print("Alice and Bob publicly disclose half of their bits in order to check for error and Eve's presence.")

    alice_postDisclose, bob_postDisclose, disclosed_error = tools.discloseBits(alice_sifted, bob_sifted)

    if detailed:
        print("Alice's bits after disclosure:\n", tools.list_to_string(alice_postDisclose), sep='')
        print("Bob's bits after disclosure:\n", tools.list_to_string(bob_postDisclose), sep='')
        print("Calculated error in disclosed bits: ", disclosed_error)

    if disclosed_error > error_rate:
        if eve:
            if detailed:
                print('Eve detected!')
            return [['aborted'], ['aborted']]
        else:
            if detailed:
                print('Alice and Bob retry due to high error.')
            return [['terminated'], ['terminated']]

    else:
        alice_temp = alice_postDisclose.copy() # we want to keep the string of bits before running CASCADE for printing to table
        bob_temp = bob_postDisclose.copy()

        if error_rate == 0.0:
            alice_reconciled, bob_reconciled = alice_temp, bob_temp
        else:
            alice_reconciled, bob_reconciled = cascade.runCascade(alice_temp, bob_temp, error_rate)
            if detailed:
                print('Alice and Bob perform the CASCADE algorithm for error reconciliation')
                print("Alice's reconciled key:\n",tools.list_to_string(alice_reconciled), sep='')
                print("Bob's reconciled key:\n", tools.list_to_string(bob_reconciled), sep='')
                print('Error after CASCADE: ',tools.calculateError(alice_reconciled, bob_reconciled))

        alice_final_key, bob_final_key = privacy_amplification.privacy_amp(alice_reconciled, bob_reconciled, disclosed_error)

        if detailed:
            print("Finally, Alice and Bob randomly hash their keys for privacy amplification")
            print("Alice's private key:\n", tools.list_to_string(alice_final_key), sep='')
            print("Bob's private key:\n", tools.list_to_string(bob_final_key), sep='')
            if eve: 
                print('Eve undetected!')


        if not eve:
            eve_bases = ['-'] * len(alice_bases)


        # Only practical for small data sizes
        table.printTable(alice_bits, alice_bases, encoded_list, eve_bases, bob_bases, bob_bits,
                alice_sifted_for_print,bob_sifted_for_print, alice_postDisclose, bob_postDisclose, alice_reconciled,
                bob_reconciled, alice_final_key, bob_final_key)

        return [alice_final_key, bob_final_key]

