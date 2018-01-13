import sys
from cStringIO import StringIO
from collections import defaultdict


# PROBLEM 1 & 2
# here we consider the input as 2d matrix, find the starting symbol
# and follow the same direction until we encounter a + symbol, where
# we update direction followed, until reaching the end
def route(fp, n_iter=1000000):

    # update direction
    #
    # next direction is the one that has an element along it
    # and is not the previous direction
    def update_dep(scheme, x, y, dep):
        deps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        # previous elements
        xp = x - dep[0]
        yp = y - dep[1]
        xm = len(scheme)
        ym = len(scheme[0])
        # check all directions for suitability
        for k in xrange(4):
            # do not consider spaces
            if x + deps[k][0] >= 0 and x + deps[k][0] < xm and y + deps[k][0] >= 0 and y + deps[k][0] < ym:
                # do not consider outside map elements
                if not scheme[x + deps[k][0]][y + deps[k][1]].isspace():
                    # check that not falling back on previous direction
                    if x + deps[k][0] != xp or y + deps[k][1] != yp:
                        print 'found : ', scheme[x + deps[k][0]][y + deps[k][1]]
                        break
        return deps[k]

    # parse input
    scheme = []
    for line in fp.readlines():
        scheme.append(line.rstrip('\n'))
    # find start
    x = 0
    y = scheme[0].index('|')
    dep = (1, 0)
    prev = '|'
    acc = ''
    # navigate through scheme
    for k in xrange(n_iter):
        x += dep[0]
        y += dep[1] 
        elem = scheme[x][y]
        if elem.isalpha():
            acc += elem
        elif elem == '+':
            dep = update_dep(scheme, x, y, dep)
            print dep
        elif elem.isspace():
            print 'STOP'
            break

    return acc, k + 1


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('data/puzzle19.txt', 'r') as input:
            with open('sols/puzzle19.txt', 'w') as f:
                f.write(str(route(input)[0]))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle19.txt', 'r') as input:
            with open('sols/puzzle19b.txt', 'w') as f:
                f.write(str(route(input)[1]))

