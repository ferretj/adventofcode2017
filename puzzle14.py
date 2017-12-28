import sys
import numpy as np
from cStringIO import StringIO
from puzzle10 import knot_hash


# calculates sequence of binary hashes for a given file
# using knot hash function
def binary_hashes(f):

    # calculates binary version of hex hash
    def to_binary(h):

        # converts hex to binary 
        def hex_to_bin(s):
            bin = {
                '0': '0000',
                '1': '0001',
                '2': '0010',
                '3': '0011',
                '4': '0100',
                '5': '0101',
                '6': '0110',
                '7': '0111',
                '8': '1000',
                '9': '1001',
                'a': '1010',
                'b': '1011',
                'c': '1100',
                'd': '1101',
                'e': '1110',
                'f': '1111'
            }
            return bin[str(s)]

        return ''.join([hex_to_bin(s) for s in h])

    # parse input
    base = f.next().rstrip('\n')
    # create keys sequence
    keys = [base + '-' + str(i) for i in xrange(128)]
    # convert to hexadecimal knot hashes
    hashes = [knot_hash(StringIO(key), 256) for key in keys]
    # convert to binary knot hashes
    hashes = [to_binary(h) for h in hashes]
    return hashes


# PROBLEM 1
# the solution is a simple adaptation of the function
# calculating knot hashes created for puzzle 10
def used_squares(f):
    # convert input to sequence of binary hashes
    hashes = binary_hashes(f)
    # sum ones
    used = sum([sum([int(c) for c in h]) for h in hashes])
    return used


# calculates amount of distinct connected components
# in a numpy square matrix
#
# uses a state matrix to keep trace of which elements of
# the matrix have already been scanned
#
# seeds are starting elements for a connected component
def connected_components(m, n_iter=100000):

    # find starting element for an unseen component
    def search_new_seed(m, st):
        x = m * st
        xw, yw = np.where(x == 1)
        if len(xw) == 0:
            return None, None
        return xw[0], yw[0]

    # recursively puts states of elements connected to
    # a seed element to 0 (in state matrix)
    def browse_all_connections(m, st, i, j):
        n = len(m)
        # stopping criterions
        if i < 0 or i >= n:
            return st, 0
        elif j < 0 or j >= n:
            return st, 0
        elif m[i, j] == 0:
            return st, 0
        elif st[i, j] == 0:
            return st, 0
        # state update
        st[i, j] = 0
        # accumulation
        xs = [0, 1, 0, -1]
        ys = [-1, 0, 1, 0]
        for x, y in zip(xs, ys):
            browse_all_connections(m, st, i + x, j + y)
        return st

    # make state matrix
    st = np.ones_like(m)
    cc = 0
    # browse through all matrix to find all seeds
    for _ in xrange(n_iter):
        i, j = search_new_seed(m, st)
        if i is None or j is None:
            print 'no additional seed found !!'
            return cc
        st = browse_all_connections(m, st, i, j)
        cc += 1
        if np.sum(st) == 0:
            print 'all states visited !!'
            return cc
    raise ValueError('Reached max number of iterations without finding all connected components.')


# PROBLEM 2
# converts input to binary hashes, stacks hashes
# to make a numpy matrix, and apply previous function
# to calculate amount of connected components
def count_regions(f):
    # convert input to sequence of binary hashes
    hashes = binary_hashes(f)
    # convert to numpy matrix for convenience
    m = np.vstack([np.array([int(c) for c in h])[np.newaxis, :] for h in hashes])
    # count distinct connected components in matrix
    c = connected_components(m)
    return c


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle14.txt', 'r') as input:
            with open('sols/puzzle14.txt', 'w') as f:
                f.write(str(used_squares(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle14.txt', 'r') as input:
            with open('sols/puzzle14b.txt', 'w') as f:
                f.write(str(count_regions(input)))


