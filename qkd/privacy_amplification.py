import numpy as np
from numpy.random import randint
import time

seed = int(time.time())
np.random.seed(seed = seed)

def get_hash_matrix(rows, cols):
    return np.random.randint(0, 2, (rows, cols))

def privacy_amp(alice_key, bob_key, error):
    cols = len(alice_key)
    rows = int(np.floor((1 - error) * len(alice_key)))

    hash_m = get_hash_matrix(rows, cols)

    alice_hashed_key = (hash_m @ alice_key) % 2
    bob_hashed_key = (hash_m @ bob_key) % 2

    return alice_hashed_key, bob_hashed_key
