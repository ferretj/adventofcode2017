import sys
import numpy as np


# the solution consists in finding the argmax of the actual
# sequence and to redistribute its value as explained
#
# a hash that is characteristic of the sequence is saved
# at each step
#
# when the set of the hashes contains less elements than the
# hashes, iterations stop since it means a previously seen hash was found
def memory_reallocation_cycles(f, n_iter=100000):

    def memory_hash(seq):
        h = ''
        for s in seq:
            h += str(s) + '/'
        return h

    seq = f.next().rstrip('\n').split()
    seq = [int(s) for s in seq]
    n = len(seq)
    hashes = [memory_hash(seq)]
    cpt = 0
    for k in xrange(n_iter):
        cpt += 1
        i = np.argmax(seq)
        m = seq[i]
        for j in xrange(1, m + 1):
            seq[(i + j) % n] += 1
        seq[i] -= m
        hashes.append(memory_hash(seq))
        if len(hashes) != len(list(set(hashes))):
            return cpt
    raise ValueError('Reached max number of iterations without finding two configurations alike.')


# as above, when the set of the hashes contains less elements than the
# hashes, iterations stop since it means a previously seen hash was found
#
# the hash seen twice is found via index function
def memory_reallocation_cycles_min(f, n_iter=100000):

    def memory_hash(seq):
        h = ''
        for s in seq:
            h += str(s) + '/'
        return h

    def steps_between_occurrences(seq, elem):
        return len(seq) - seq.index(elem) - 1

    seq = f.next().rstrip('\n').split()
    seq = [int(s) for s in seq]
    n = len(seq)
    hashes = [memory_hash(seq)]
    cpt = 0
    for k in xrange(n_iter):
        cpt += 1
        i = np.argmax(seq)
        m = seq[i]
        for j in xrange(1, m + 1):
            seq[(i + j) % n] += 1
        seq[i] -= m
        hashes.append(memory_hash(seq))
        if len(hashes) != len(list(set(hashes))):
            return steps_between_occurrences(hashes, hashes[-1])
    raise ValueError('Reached max number of iterations without finding two configurations alike.')


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle06.txt', 'r') as input:
            with open('sols/puzzle06.txt', 'w') as f:
                f.write(str(memory_reallocation_cycles(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle06.txt', 'r') as input:
            with open('sols/puzzle06b.txt', 'w') as f:
                f.write(str(memory_reallocation_cycles_min(input)))
