import sys
import numpy as np
from cStringIO import StringIO
from copy import copy


# Object for the 2-dimensional grid of pixels described in problem.
# Should have created a subclass of numpy.ndarray.
class Grid(object):

    def __init__(self, mat):
        self.mat = mat

    def __getitem__(self, k):
        return self.mat[k]

    def __repr__(self):
        s = ''
        nl = self.size - 1
        for i, line in enumerate(self.mat):
            s += ''.join(['.' if n == 0 else '#' for n in line])
            if i != nl:
                s += '\n'
        return s

    @classmethod
    def default(cls):
        mat = np.array([[0, 1, 0],
                        [0, 0, 1],
                        [1, 1, 1]]).astype(np.uint8)
        return cls(mat)

    @classmethod
    def from_str(cls, s):
        mat = cls.str_to_numpy(s)
        return cls(mat)

    @classmethod
    def from_subgrids(cls, sg, div):
        '''Reconstruct grid from transformed subparts.'''
        if not isinstance(sg, list):
            raise TypeError('subgrid must be a list')
        ngrids = len(sg)
        ng = int(np.sqrt(ngrids))
        mat = np.zeros((ng * div, ng * div))
        for i in xrange(ng):
            for j in xrange(ng):
                k = i * ng + j
                mat[i * div: (i + 1) * div, j * div: (j + 1) * div] = sg[k].mat
        return cls(mat)

    @property
    def size(self):
        return self.mat.shape[0]

    @property
    def n_pixels(self):
        return int(np.sum(self.mat))

    @property
    def div(self):
        if self.size % 2 == 0:
            div = 2
        elif self.size % 3 == 0:
            div = 3
        else:
            err = 'Grid size must be a multiple of 2 or 3. Size is {}'
            raise ValueError(err.format(grid.size))
        return div

    def quadrants(self, div):
        '''
        Construct list of subgrids based on whether the grid
        can be divided by 2 or 3.
        '''
        if self.size == 2 or self.size == 3:
            return [self]
        else:
            parts = []
            nquad = self.size // div
            for i in xrange(nquad ** 2):
                r = i // nquad
                c = i % nquad
                parts.append(self.quadrant(r, c, div))
        return parts

    @staticmethod
    def str_to_numpy(s):
        s = s.replace('/', '')
        nc = len(s)
        size = int(np.sqrt(nc))
        mat = np.zeros((size, size), dtype=np.uint8)
        for k, c in enumerate(s):
            if c == '#':
                i = k // size
                j = k % size
                mat[i, j] = 1
        return mat

    def quadrant(self, r, c, div=None):
        if self.size == 2 or self.size == 3:
            raise ValueError('Size not sufficient. Must be > 3.')
        if div is None:
            div = self.div
        return Grid(self[r * div: (r + 1) * div, c * div: (c + 1) * div])

    def transform_full(self, tlist):
        if self.size > 3:
            raise ValueError('Size is too large for full apply.')
        for transfo in tlist:
            try:
                return transfo(self)
            except ValueError:
                pass
        raise ValueError('No single transform could be applied.')

    def transform_quadrants(self, tlist, div):
        quads = self.quadrants(div)
        new_quads = []
        for i, quad in enumerate(quads):
            print 'Quadrant {}'.format(i + 1)
            print quad
            try:
                new_quads.append(quad.transform_full(tlist))
            except ValueError:
                raise ValueError('No transform could be applied on quadrant {}.'.format(i + 1))
        return new_quads

    def transform(self, tlist, div=None):
        if div is None:
            div = self.div
        if self.size == 2 or self.size == 3:
            return self.transform_full(tlist)
        else:
            l = []
            l.extend(self.transform_quadrants(tlist, div))
            return Grid.from_subgrids(l, div + 1)

    def allclose(self, mat):
        return np.allclose(np.uint8(self.mat), 
                           np.uint8(mat))


# Class for transformation
class RuleTransform(object):

    def __init__(self, s):
        sx, _, sfx = s.rstrip('\n').split()
        self.x = Grid.str_to_numpy(sx)
        self.fx = Grid.str_to_numpy(sfx)
        if len(sx) == 5:
            self.size = 2
        elif len(sx) == 11:
            self.size = 3
        else:
            raise ValueError('{}'.format(len(sx)))
        self.str = s

    def __repr__(self):
        return self.str

    def __call__(self, grid):
        if grid.size == self.size:
            try:
                gridr = self.rotate_flip_apply(grid, 0)
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 0, 'lr')
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 0, 'ud')
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 90)
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 90, 'lr')
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 90, 'ud')
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 180)
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                pass
            try:
                gridr = self.rotate_flip_apply(grid, 270)
                print 'transfo applied : ' + str(self)
                return Grid(gridr)
            except ValueError:
                err = 'Could not apply transform after flips nor after rotations.'
                raise ValueError(err)
        else:
            err = 'Grid size ({}) must be equal to transform size ({}).'
            raise ValueError(err.format(grid.size, self.size))

    @property
    def n_pixels(self):
        return np.sum(self.x)

    def rotate_flip_apply(self, grid, rot=0, flip=None):
        mat = grid.mat
        try:
            if rot == 0:
                new_grid = grid
            elif rot == 90:
                new_grid = Grid(np.rot90(mat))
            elif rot == 180:
                new_grid = Grid(np.rot90(mat, k=2))
            elif rot == 270:
                new_grid = Grid(np.rot90(mat, k=3))
            mat = new_grid.mat
            if flip == 'lr':
                new_grid = Grid(np.fliplr(mat))
            elif flip == 'ud':
                new_grid = Grid(np.flipud(mat))
            return self.apply(new_grid)
        except ValueError:
            raise ValueError('Matrix config not corresponding.')

    def apply(self, mat):
        if mat.allclose(self.x):
            return self.fx
        else:
            raise ValueError('Matrix not corresponding.')


# PROBLEM 1 & 2
# Opted for the bruteforce solution where you calculate
# the results of the successive grid transformations and
# count the amount of pixels on by summing their values.
# Runs in less than 20 minutes for problem 2 on my laptop. 
def fractal_augment(fp, n_apply):
    funcs2 = []
    funcs3 = []
    # parse input
    lines = fp.readlines()
    for line in lines:
        func = RuleTransform(line.rstrip('\n'))
        if func.size == 2:
            funcs2.append(func)
        elif func.size == 3:
            funcs3.append(func)
        else:
            raise ValueError('Wrong parsing ?')
    print 'transfos :'
    for tsf in funcs2:
        print tsf
    for tsf in funcs3:
        print tsf
    # define starting grid
    grid = Grid.default()
    print 'start :'
    print grid
    # chain apply transforms
    nfc2 = len(funcs2)
    nfc3 = len(funcs3)
    funcs = funcs2 + funcs3
    for i in xrange(n_apply):
        grid = grid.transform(funcs)
        print 'new grid :'
        print grid
    return grid


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('data/puzzle21.txt', 'r') as input:
            with open('sols/puzzle21.txt', 'w') as f:
                f.write(str(fractal_augment(input, 5).n_pixels))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle21.txt', 'r') as input:
            with open('sols/puzzle21b.txt', 'w') as f:
                f.write(str(fractal_augment(input, 18).n_pixels))

