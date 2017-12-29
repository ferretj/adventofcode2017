import sys
import numpy as np
from cStringIO import StringIO


# converts integers to 32bit binary
def bin32(n):
    b = bin(n)[2:]
    nb = len(b)
    if nb > 32:
        d = nb - 32
        return b[d:]
    elif nb < 32:
        d = 32 - nb
        return '0' * d + b
    return b


# PROBLEM 1
# uses generators and string comparisons - quite
# straightforward
def judge_count(f, n):

    # dueling generator
    def duel_gen(seed, fact, n, div=2147483647):
        for _ in xrange(n):
            seed = seed * fact % div
            yield bin32(seed)

    # parse input
    seed_a = int(f.next().rstrip('\n').split()[-1])
    seed_b = int(f.next().rstrip('\n').split()[-1])
    # create generators
    gen_a = duel_gen(seed_a, 16807, n)
    gen_b = duel_gen(seed_b, 48271, n)
    # compare generators for n outputs
    c = 0
    for _ in xrange(n):
        a = gen_a.next()[16:]
        b = gen_b.next()[16:]
        if a == b:
            c += 1

    return c


# PROBLEM 2
# slight modification of above function to adapt to
# second version of problem
#
# the key here is to generate more candidates than needed
# inside generator function to cope with the selection
# mechanism
def judge_count_v2(f, n):

    # dueling generator with selection mechanism
    def duel_gen(seed, fact, n, mul, div=2147483647):
        for _ in xrange(n):
            seed = seed * fact % div
            if seed % mul == 0:
                yield bin32(seed)

    # parse input
    seed_a = int(f.next().rstrip('\n').split()[-1])
    seed_b = int(f.next().rstrip('\n').split()[-1])
    # create generators
    gen_a = duel_gen(seed_a, 16807, 100 * n, 4)
    gen_b = duel_gen(seed_b, 48271, 100 * n, 8)
    # compare generators for n outputs
    c = 0
    for _ in xrange(n):
        a = gen_a.next()[16:]
        b = gen_b.next()[16:]
        if a == b:
            c += 1

    return c

if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle15.txt', 'r') as input:
            with open('sols/puzzle15.txt', 'w') as f:
                f.write(str(judge_count(input, 40000000)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle15.txt', 'r') as input:
            with open('sols/puzzle15b.txt', 'w') as f:
                f.write(str(judge_count_v2(input, 5000000)))


