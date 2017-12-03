import sys
import numpy as np


def spiral_memory_steps(n):
    nsteps = 0
    c = 1
    found = False
    while not found:
        if n > c:
            nsteps += 1
            c += 8 * nsteps
        else:
            found = True
    s = c - nsteps
    q = 2 * nsteps
    d = min([abs(s - i * q - n) for i in xrange(4)])
    nsteps += d
    return nsteps


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


def spiral_additive_higher(n, niter=1000):

    def fill_next_elem(m, addd, i, j, c):
        d = addd[c]
        i += d[0]
        j += d[1]
        next = np.sum(m[max(0, i - 1): i + 2, max(0, j - 1): j + 2])
        m[i, j] = next
        return m, i, j, next

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
    for ni in xrange(niter):
        if ni == l ** 2 - 1:
            m, l, i, j = upsize(m, l, i, j)
        m, i, j, next = fill_next_elem(m, addd, i, j, c)
        if next > n:
            return int(next)
        addv, v, c = update(addv, v, c)


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
