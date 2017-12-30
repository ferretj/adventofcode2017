from copy import copy
import sys
import string
from cStringIO import StringIO


# returns circular buffer mechanism result after n insertions
# for a given step input
def circular_buffering(f, n=2017):
    # parsing input
    step = int(f.next().rstrip('\n'))
    # circular buffering
    l = [0]
    curr = 0
    for i in xrange(1, n + 1):
        size = len(l)
        curr = (curr + step) % size
        l.insert(curr + 1, i)
        curr += 1
    return l


# PROBLEM 1
# sequentially inserts values in list according
# to circular buffer mechanism and gets the element
# right after 2017
def first_value_cb(f, n=2017):
    l = circular_buffering(f, n=n)
    size = len(l)
    i = l.index(n)
    x = (i + 1) % size
    return l[x]


# PROBLEM 2
# here a simplification is required to have a solution running
# in an acceptable amount of time
#
# the trick is that we do not actually need to store anything in
# a list since we only want to save the elements inserted after 0,
# which happens when curr + step == 0 mod i
def calc0(f, n=50000000):
    # parsing input
    step = int(f.next().rstrip('\n'))
    # circular buffering
    curr = 0
    aft0 = 0
    for i in xrange(1, n + 1):
        curr = (curr + step) % i
        if curr == 0:
            aft0 = i
        curr += 1
    return aft0


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('data/puzzle17.txt', 'r') as input:
            with open('sols/puzzle17.txt', 'w') as f:
                f.write(str(first_value_cb(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle17.txt', 'r') as input:
            with open('sols/puzzle17b.txt', 'w') as f:
                f.write(str(calc0(input)))

