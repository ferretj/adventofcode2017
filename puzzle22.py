import numpy as np
import sys


def line_to_binary(line):
    line = line.rstrip('\n')
    binary = [0 if char == '.' else 1 for char in line]
    return binary


def left(direc):
    if direc == (-1, 0):
        direc = (0, -1)
    elif direc == (1, 0):
        direc = (0, 1)
    elif direc == (0, -1):
        direc = (1, 0)
    elif direc == (0, 1):
        direc = (-1, 0)
    else:
        raise ValueError('direc invalid.')
    return direc


def right(direc):
    if direc == (-1, 0):
        direc = (0, 1)
    elif direc == (1, 0):
        direc = (0, -1)
    elif direc == (0, -1):
        direc = (-1, 0)
    elif direc == (0, 1):
        direc = (1, 0)
    else:
        raise ValueError('direc invalid.')
    return direc


def over_bounds(mat, r, c):
    R = mat.shape[0]
    C = mat.shape[1]
    if r < 0:
        return True
    elif r >= R:
        return True
    elif c < 0:
        return True
    elif c >= C:
        return True
    return False


def upsize(mat, direc, r, c):
    R = mat.shape[0]
    C = mat.shape[1]
    if direc == (-1, 0):
        newmat = np.zeros((R * 2, C))
        newmat[R: 2 * R] = mat
        r += R
    elif direc == (1, 0):
        newmat = np.zeros((R * 2, C))
        newmat[:R] = mat
    elif direc == (0, -1):
        newmat = np.zeros((R, C * 2))
        newmat[:, C: 2 * C] = mat
        c += C
    elif direc == (0, 1):
        newmat = np.zeros((R, C * 2))
        newmat[:, :C] = mat
    else:
        raise ValueError('direc invalid.')
    return newmat, r, c


# PROBLEM 1
# Quite straightforward solution, using a numpy
# 2d array to represent cell states and updating
# them as indicated in problem setting.
def activity_bursts(fp, n_iter):
    bursts = 0
    # parse input
    mat = []
    lines = fp.readlines()
    for line in lines:
        mat.append(line_to_binary(line))
    mat = np.vstack(mat).astype(int)
    # apply bursts
    h = len(mat) // 2
    r, c = h, h
    direc = (-1, 0)
    for i in xrange(n_iter):
        cell = mat[r, c]
        # turn according to cell state
        if cell == 0:
            direc = left(direc)
            bursts += 1
        else:
            direc = right(direc)
        # update cell
        mat[r, c] = 1 - cell
        # update coordinates
        r, c = r + direc[0], c + direc[1]
        # upsize matrix if needed and update coordinates
        if over_bounds(mat, r, c):
            mat, r, c = upsize(mat, direc, r, c)
    return bursts


def reverse(direc):
    return (-direc[0], -direc[1])


def update_cell_state(cell):
    if cell == 0:
        cell = 2
    elif cell == 1:
        cell = 3
    elif cell == 2:
        cell = 1
    elif cell == 3:
        cell = 0
    else:
        raise ValueError('Cell state is not valid.')
    return cell


# weakened = 2
# flagged = 3
#
# PROBLEM 2
# As above with minor modifications to
# take into account weakened and flagged
# states.
def activity_bursts_updated(fp, n_iter):
    bursts = 0
    # parse input
    mat = []
    lines = fp.readlines()
    for line in lines:
        mat.append(line_to_binary(line))
    mat = np.vstack(mat).astype(int)
    # apply bursts
    h = len(mat) // 2
    r, c = h, h
    direc = (-1, 0)
    for i in xrange(n_iter):
        cell = mat[r, c]
        # turn according to cell state
        if cell == 0:
            direc = left(direc)
        elif cell == 1:
            direc = right(direc)
        elif cell == 2:
            bursts += 1
        elif cell == 3:
            direc = reverse(direc)
        # update cell
        mat[r, c] = update_cell_state(cell)
        # update coordinates
        r, c = r + direc[0], c + direc[1]
        # upsize matrix if needed and update coordinates
        if over_bounds(mat, r, c):
            mat, r, c = upsize(mat, direc, r, c)
    return bursts


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('data/puzzle22.txt', 'r') as input:
            with open('sols/puzzle22.txt', 'w') as f:
                f.write(str(activity_bursts(input, 10000)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle22.txt', 'r') as input:
            with open('sols/puzzle22b.txt', 'w') as f:
                f.write(str(activity_bursts_updated(input, 10000000)))