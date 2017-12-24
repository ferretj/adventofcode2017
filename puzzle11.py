from copy import copy
import sys
import cStringIO
import numpy as np
from collections import defaultdict


# erases moves that cancel each other
def remove_opposite_moves(counts, cs):
    cs.append(min(counts['ne'], counts['sw']))  # ne + sw = 0
    counts['ne'] -= cs[-1]
    counts['sw'] -= cs[-1]
    cs.append(min(counts['nw'], counts['se']))  # nw + se = 0
    counts['nw'] -= cs[-1]
    counts['se'] -= cs[-1]
    cs.append(min(counts['n'], counts['s']))    # n + s   = 0
    counts['n'] -= cs[-1]
    counts['s'] -= cs[-1]
    return counts, cs


# recombines moves whose combination is equivalent to a single move
def recombine_moves_to_unit(counts, cs):
    cs.append(min(counts['nw'], counts['s']))  # nw + s = sw
    counts['nw'] -= cs[-1]
    counts['s'] -= cs[-1]
    counts['sw'] += cs[-1]
    cs.append(min(counts['sw'], counts['n']))  # sw + n = nw
    counts['sw'] -= cs[-1]
    counts['n'] -= cs[-1]
    counts['nw'] += cs[-1]
    cs.append(min(counts['se'], counts['n']))  # se + n = ne
    counts['se'] -= cs[-1]
    counts['n'] -= cs[-1]
    counts['ne'] += cs[-1]
    cs.append(min(counts['ne'], counts['s']))  # ne + s = se
    counts['ne'] -= cs[-1]
    counts['s'] -= cs[-1]
    counts['se'] += cs[-1]
    cs.append(min(counts['nw'], counts['ne']))  # ne + nw = n
    counts['nw'] -= cs[-1]
    counts['ne'] -= cs[-1]
    counts['n'] += cs[-1]
    cs.append(min(counts['se'], counts['sw']))  # sw + se = s
    counts['se'] -= cs[-1]
    counts['sw'] -= cs[-1]
    counts['s'] += cs[-1]
    return counts, cs


# FIRST PROBLEM
# the solution consists in combining moves that cancel or recombine to single moves
# iteratively until no recombination is possible anymore
#
# the steps to take in the hex grid is then the amount of remaining moves
def hex_steps(f, n_iter=100):

    # parse input and count moves of each type
    n_steps = 0
    steps = f.next().split(',')
    counts = defaultdict(int)
    for step in steps:
        counts[step] += 1
    print counts
    # repeat until depletion
    for _ in xrange(n_iter):
        cs = []
        # first, get rid of opposite moves
        counts, cs = remove_opposite_moves(counts, cs)
        # second, recombine moves to unitary ones
        counts, cs = recombine_moves_to_unit(counts, cs)
        if all([c == 0 for c in cs]):
            break
    return sum(counts.values())


# SECOND PROBLEM
# the solution consists in applying the above process after each move to know
# the number of steps in the hex grid at every moment 
#
# the max amount of steps is the max of that sequence
def max_hex_steps(f, n_iter=100):

    # parse input
    max_steps = 0
    steps = f.next().split(',')
    counts = defaultdict(int)
    # calculate distance to origin at each step and save max value
    for step in steps:
        counts[step] += 1
        # repeat until depletion
        for _ in xrange(n_iter):
            cs = []
            # first, get rid of opposite moves
            counts, cs = remove_opposite_moves(counts, cs)
            # second, recombine moves to unitary ones
            counts, cs = recombine_moves_to_unit(counts, cs)
            if all([c == 0 for c in cs]):
                break
        n_steps = sum(counts.values())
        if n_steps > max_steps:
            max_steps = n_steps 
    return max_steps


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle11.txt', 'r') as input:
            with open('sols/puzzle11.txt', 'w') as f:
                f.write(str(hex_steps(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle11.txt', 'r') as input:
            with open('sols/puzzle11b.txt', 'w') as f:
                f.write(str(max_hex_steps(input)))


