from copy import copy
import sys
import cStringIO
import numpy as np


def circular_reverse(l, start, end):
        n = len(l)
        lc = copy(l)
        indices = [elem % n for elem in xrange(start, end)]
        for idx, idxr in zip(indices, indices[::-1]):
            l[idx] = lc[idxr]
        return l


def knot_hash_first_two_elems(f, n):

    seq = [int(elem) for elem in f.next().split(',')]

    kh = range(n)
    curr = 0
    skip = 0
    for elem in seq:
        kh = circular_reverse(kh, curr, curr + elem)
        curr = (curr + skip + elem) % n
        skip += 1

    return kh[0] * kh[1]


def knot_hash(f, n):

    def char_to_ascii_num(c):
        return ord(c)

    def knot_hash_round(l, seq, n, curr, skip):
        for elem in seq:
            l = circular_reverse(l, curr, curr + elem)
            curr = (curr + skip + elem) % n
            skip += 1
        return l, curr, skip

    def binary(num, nbits=8):
        base = bin(num)[2:]
        nb = len(base)
        z = '0' * (nbits - nb) 
        return z + base

    def bitwise_xor(block):
        bits = [[int(elem) for elem in binary(num, 8)] for num in block]
        xor = np.bitwise_xor(bits[0], bits[1])
        for i in xrange(1, 15):
            xor = np.bitwise_xor(xor, bits[i + 1])
        int_xor = int(''.join([str(b) for b in xor]), 2)
        return int_xor

    # processing input
    try:
        seq = [char_to_ascii_num(elem) for elem in f.next().replace(' ', '')]
    except StopIteration:
        seq = []
    seq = seq + [17, 31, 73, 47, 23]

    # getting the sparse hash
    sph = range(n)
    curr = 0
    skip = 0
    for _ in xrange(64):
        sph, curr, skip = knot_hash_round(sph, seq, n, curr, skip)
    
    # getting the dense hash
    dph = []
    for i in xrange(16):
        dph.append(bitwise_xor(sph[i * 16: (i + 1) * 16]))

    # getting the knot hash
    kh = ''
    for num in dph:
        hexa = hex(num)[2:]
        if len(hexa) == 1:
            hexa = '0' + hexa
        kh = kh + hexa

    return kh

if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle10.txt', 'r') as input:
            with open('sols/puzzle10.txt', 'w') as f:
                f.write(str(knot_hash_first_two_elems(input, 256)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle10.txt', 'r') as input:
            with open('sols/puzzle10b.txt', 'w') as f:
                f.write(str(knot_hash(input, 256)))


