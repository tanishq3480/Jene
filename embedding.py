import numpy as np

mapping = {'A':0, 'T':1, 'G':2, 'C':3}

def encode_sequence(seq, max_len=300):
    encoded = [mapping.get(base, 0) for base in seq[:max_len]]
    
    if len(encoded) < max_len:
        encoded += [0] * (max_len - len(encoded))
    
    return np.array(encoded)