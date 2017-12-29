from copy import copy
import sys
import string
from cStringIO import StringIO


# PROBLEM 1
# here we simply parse the input and apply
# all the transformations defined to the list
# of characters
def dancing_permutation(l, fp):

    def spin(l, n):
        l = l[-n:] + l[:-n]
        return l

    def exchange(l, i, j):
        c = l[i]
        l[i] = l[j]
        l[j] = c
        return l

    def partner(l, a, b):
        i = l.index(a)
        j = l.index(b)
        l = exchange(l, i, j)
        return l

    # parse input
    if type(fp) is file:
        moves = fp.next().rstrip('\n').split(',')
    elif isinstance(fp, str):
        moves = fp.split(',')
    else:
        raise TypeError('Wrong type for fp argument.')
    
    # define and sequentially apply list operations
    for move in moves:
        if 's' in move:
            n = int(move[1:])
            l = spin(l, n)
        elif 'x' in move:
            pgs = move[1:].split('/')
            i = int(pgs[0])
            j = int(pgs[1])
            l = exchange(l, i, j)
        else:
            pgs = move[1:].split('/')
            a = pgs[0]
            b = pgs[1]
            l = partner(l, a, b)

    return l


# PROBLEM 2
# 1 billion iterations of the dancing permutation would take an awful lot of time
# 
# the solution consists in finding the number of iterations of
# the dancing permutation that are necessary to get to the initial
# list again ; let's call that number p
#
# then we apply k times the dancing permutation to get the result, 
# where k is the rest in the euclidean division of n (1 billion here) by p
def n_dances(l, fp, n, n_iter=100):

    lc = copy(l)
    lh = ''.join(l)
    p = -1
    inp = fp.next().rstrip('\n')
    
    # finding p
    for i in xrange(n_iter):
        l = dancing_permutation(l, inp)
        if ''.join(l) == lh:
            p = i + 1
            break
    if p == -1:
        raise ValueError('Reached max number of iterations without finding mod of dancing sort')

    # applying k times the dancing perm
    k = n % mod
    for _ in xrange(k):
        lc = dancing_permutation(lc, inp)

    return lc


if __name__ == '__main__':

    l = list(string.ascii_lowercase)[:16]

    if int(sys.argv[1]) == 0:
        with open('data/puzzle16.txt', 'r') as input:
            with open('sols/puzzle16.txt', 'w') as f:
                ll = dancing_permutation(l, input)
                f.write(''.join(ll))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle16.txt', 'r') as input:
            with open('sols/puzzle16b.txt', 'w') as f:
                ll = n_dances(l, input, 1000000000)
                f.write(''.join(ll))


