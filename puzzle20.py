import sys
import numpy as np
from cStringIO import StringIO
from collections import defaultdict


# simple class to manage particles
class Particle(object):

    def __init__(self, p, v, acc):
        self.p  = np.array(p)
        self.v  = np.array(v)
        self.acc  = np.array(acc)

    # returns particle pos, speed and acceleration after some ticks
    # /!\ no need to calculate all intermediate updates
    #     a simple recurrence can show this
    def update(self, nsteps):
        pm = self.p + nsteps * self.v + (nsteps * (nsteps + 1) // 2) * self.acc
        vm = self.v + nsteps * self.acc
        return pm, vm, self.acc

    # distance to origin
    def dist(self, nsteps=0):
        if nsteps == 0:
            return np.abs(self.p).sum()
        pm, vm, _ = self.update(nsteps)
        return np.abs(pm).sum()


# simple class to manage particle swarm
class ParticleSwarm(object):

    def __init__(self, ps, vs, accs):
        self.sw = [Particle(p, v, acc) for p, v, acc in zip(ps, vs, accs)]

    @property
    def n_particles(self):
        return len(self.sw)

    # rank particles from closest to farthest from origin
    def rank_particles(self, nsteps):
        dists = [part.dist(nsteps) for part in self.sw]
        return np.argsort(dists)

    # remove particles colliding at a specific tick
    def remove_current_colliding(self, step):

        # finds all duplicate elements in a list
        def duplicates(l):
            seen = set()
            dups = set()
            for x in l:
                if x not in seen:
                    seen.add(x)
                else:
                    dups.add(x)
            return dups

        ps = [tuple(part.update(step)[0]) for part in self.sw]
        dp = duplicates(ps)
        self.sw = [part for i, part in enumerate(self.sw) if ps[i] not in dp]

    # remove all particles that collide between start and a given tick
    def remove_colliding(self, nsteps):
        print '{} particles at initialization'.format(self.n_particles)
        for i in xrange(nsteps):
            self.remove_current_colliding(i)
        print '{} particles after {} steps'.format(self.n_particles, nsteps)
        return self.n_particles


# takes 'x=<x0,x1,x2>' and returns (x0, x1, x2)
def parse_vector(vect):
    bcont = vect.split('<')[1].split('>')[0]
    coords = [int(val) for val in bcont.split(',')]
    return tuple(coords)


# PROBLEM 1
# the assumption we make is that after a high enough
# number of steps, the rank of particles becomes 
# stationary
#
# we could make a simple heuristic to find that moment,
# but in our case 10000 is largely enough
def find_closest_particle(fp, nsteps=10000):
    # parse input
    ps = []
    vs = []
    accs = []
    for line in fp.readlines():
        elems = line.rstrip('\n').split(', ')
        # position
        ps.append(parse_vector(elems[0]))
        # speed
        vs.append(parse_vector(elems[1]))
        # acceleration
        accs.append(parse_vector(elems[2]))
    swarm = ParticleSwarm(ps, vs, accs)
    rank = swarm.rank_particles(nsteps)
    return rank[0]


# PROBLEM 2
# same reasoning as above
def remove_colliding_particles(fp, nsteps=4):
    # parse input
    ps = []
    vs = []
    accs = []
    for line in fp.readlines():
        elems = line.rstrip('\n').split(', ')
        # position
        ps.append(parse_vector(elems[0]))
        # speed
        vs.append(parse_vector(elems[1]))
        # acceleration
        accs.append(parse_vector(elems[2]))
    swarm = ParticleSwarm(ps, vs, accs)
    np = swarm.remove_colliding(nsteps)
    return np  


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('data/puzzle20.txt', 'r') as input:
            with open('sols/puzzle20.txt', 'w') as f:
                f.write(str(find_closest_particle(input, 10000)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle20.txt', 'r') as input:
            with open('sols/puzzle20b.txt', 'w') as f:
                f.write(str(remove_colliding_particles(input, 10000)))

