import sys
import numpy as np


# SOLUTION TO FIRST PBM
# the approach developed consists in decomposing the spiral in squares with cardinal points
#
# a square is complete once the spiral reaches a square configuration
#
# cardinal points of a square are the intersection between 2D axes and the square 
#
# finding the Manhattan distance between the center and a given element
# is equivalent to summing the indice of the square on which the element is
# and the smallest difference between a cardinal point of this square and the element 
def spiral_memory_steps(n):
    nsteps = 0
    c = 1
    found = False
    # calculates the indice of the square
    # the input number is on
    while not found:
        if n > c:
            nsteps += 1
            c += 8 * nsteps
        else:
            found = True
    # s is the value of the south cardinal point of the square
    # the other cardinal points are found via s - i * q
    s = c - nsteps
    q = 2 * nsteps
    # calculates the smallest difference between cardinal points and the input
    d = min([abs(s - i * q - n) for i in xrange(4)])
    nsteps += d
    return nsteps


# SOLUTION TO SECOND PBM
# calculates the following element of the spiral until a value higher than the input is found
#
# a square numpy matrix is used to store the elements, its size is updated each time it is needed  
def spiral_additive_higher(n, niter=1000):

    # calculates next element of the spiral
    def fill_next_elem(m, addd, i, j, c):
        d = addd[c]
        i += d[0]
        j += d[1]
        next = np.sum(m[max(0, i - 1): i + 2, max(0, j - 1): j + 2])
        m[i, j] = next
        return m, i, j, next

    # updates the length of the moves to do in each direction
    # to traverse the spiral
    def update(addv, v, c):
        if v == addv[c] - 1:
            c += 1
            v = 0
            if c == 4:
                c = 0
                addv = [av + 2 for av in addv]
        else:
            v += 1
        return addv, v, c

    # updates the matrix size when full
    def upsize(m, l, i, j):
        k = m.shape[0]
        up = np.zeros((k + 2, k + 2))
        up[1: k + 1, 1: k + 1] = m
        l += 2
        i += 1
        j += 1
        return up, l, i, j

    m = np.zeros((1, 1))
    i = 0
    j = 0
    c = 0
    v = 0
    l = 1
    addv = [1, 1, 2, 2]  # contains the length of the moves to do in each direction
    addd = {0: (0, 1),
            1: (-1, 0),
            2: (0, -1),
            3: (1, 0)}   # contains the vector corresponding to a move in each direction 
    m[i, j] = 1
    for ni in xrange(niter):
        # check for when the matrix is full
        if ni == l ** 2 - 1:
            m, l, i, j = upsize(m, l, i, j)
        m, i, j, next = fill_next_elem(m, addd, i, j, c)
        # stop when a value higher than the input is found
        if next > n:
            return int(next)
        addv, v, c = update(addv, v, c)


# toy function to fill a square matrix with the spiral elements
def fill_matrix(k):

    def fill_line(m, addd, addv, i, j, c, final=False):
        d = addd[c]
        v = addv[c] - int(final)
        for l in xrange(v):
            i += d[0]
            j += d[1]
            m[i, j] = np.sum(m[max(0, i - 1): i + 2, max(0, j - 1): j + 2])
        return m, i, j

    assert k % 2 == 1
    m = np.zeros((k, k))
    i = k // 2
    j = k // 2
    niter = k // 2
    m[i, j] = 1
    addv = [1, 1, 2, 2]
    addd = {0: (0, 1), 1: (-1, 0), 2: (0, -1), 3: (1, 0)}
    for _ in xrange(niter):
        for c in xrange(4):
            m, i, j = fill_line(m, addd, addv, i, j, c)
        addv = [v + 2 for v in addv]
    m, _, _ = fill_line(m, addd, addv, i, j, 0, final=True)
    return m


# toy function to iteratively fill a matrix with the spiral elements
def fill_matrix_iter(niter):

    def fill_next_elem(m, addd, i, j, c):
        d = addd[c]
        i += d[0]
        j += d[1]
        m[i, j] = np.sum(m[max(0, i - 1): i + 2, max(0, j - 1): j + 2])
        return m, i, j

    def update(addv, v, c):
        if v == addv[c] - 1:
            c += 1
            v = 0
            if c == 4:
                c = 0
                addv = [av + 2 for av in addv]
        else:
            v += 1
        return addv, v, c

    def upsize(m, l, i, j):
        k = m.shape[0]
        up = np.zeros((k + 2, k + 2))
        up[1: k + 1, 1: k + 1] = m
        l += 2
        i += 1
        j += 1
        return up, l, i, j

    m = np.zeros((1, 1))
    i = 0
    j = 0
    c = 0
    v = 0
    l = 1
    addv = [1, 1, 2, 2]
    addd = {0: (0, 1), 1: (-1, 0), 2: (0, -1), 3: (1, 0)}
    m[i, j] = 1
    for n in xrange(niter):
        if n == l ** 2 - 1:
            m, l, i, j = upsize(m, l, i, j)
        m, i, j = fill_next_elem(m, addd, i, j, c)
        addv, v, c = update(addv, v, c)
    return m


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle03.txt', 'r') as data:
            square = int(data.next())
            with open('sols/puzzle03.txt', 'w') as f:
                f.write(str(spiral_memory_steps(square)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle03.txt', 'r') as data:
            square = int(data.next())
            with open('sols/puzzle03b.txt', 'w') as f:
                f.write(str(spiral_additive_higher(square)))
