from copy import copy
import sys
from collections import defaultdict


# PROBLEM 1
# solution consists in encoding the state of each layer 
# in the firewall (direction and position of scanner) in
# two dictionaries
#
# severity is increased each time the current layer has a scanner
# in position 0
#
# for a cleverer solution see problem 2
def firewall_severity(f):

    # update position and direction of scanners in each layer
    def update_scanners(wall_states, wall_dirs, depths):

        def change_dir(d):
            if d == 'up':
                return 'down'
            elif d == 'down':
                return 'up'
            else:
                return d

        for depth, scan in wall_states.iteritems():
            rng = ranges[depth]
            d = wall_dirs[depth]
            # do nothing for layers with no scanners
            if rng >= 2:
                # move scanner
                if d == 'down':
                    wall_states[depth] = scan + 1
                elif d == 'up':
                    wall_states[depth] = scan - 1
                else:
                    raise ValueError('Unauthorized value for direction of scanner.')
                # update direction of scanner
                if wall_states[depth] == rng - 1 and d == 'down':
                    wall_dirs[depth] = 'up'
                elif wall_states[depth] == 0 and d == 'up':
                    wall_dirs[depth] = 'down'

        return wall_states, wall_dirs

    # parse input
    ranges = defaultdict(int)
    for line in f.readlines():
        line = line.rstrip('\n')
        depth, rng = [int(elem) for elem in line.split(': ')]
        ranges[depth] = rng
    # calculate depths
    max_depth = max(list(ranges.keys()))
    depths = set(list(ranges.keys()))
    # encode scanners direction and position
    wall_states = {i: 0 if i in depths else -1 for i in xrange(max_depth + 1)}
    wall_dirs = {i: 'down' if i in depths else None for i in xrange(max_depth + 1)}
    sev = 0
    for depth in xrange(max_depth + 1):
        scan = wall_states[depth]
        if scan == 0:
            sev += depth * ranges[depth]
        wall_states, wall_dirs = update_scanners(wall_states, wall_dirs, ranges)

    return sev


# PROBLEM 2
# test each picosecond setup until passing the firewall
#
# collision are detected via modulo ; a collision occurrs
# in a layer when current time (in picoseconds) modulo 2n - 2
# equals 0, n being the depth of the layer
#
# 2n - 2 stands for the amount of steps a scanner takes to
# reach 0 position again 
def find_delay(f, max_iter=100000000):
    # initialize dicts
    ranges = defaultdict(int)
    mods = defaultdict(int)
    # parse input
    for line in f.readlines():
        line = line.rstrip('\n')
        depth, rng = [int(elem) for elem in line.split(': ')]
        ranges[depth] = rng
        mods[depth] = 2 * rng - 2
    max_depth = max(list(ranges.keys()))
    # test all picosecond setups until finding a solution
    for k in xrange(max_iter):
        curr = k
        found = True
        # checking that there are no collisions until last layer
        for depth in xrange(max_depth + 1):
            mod = mods[depth]
            # case layer has no scanner
            if mod == 0:
                pass
            # case there is a collision
            elif curr % mod == 0:
                found = False
                break
            curr += 1
        if found:
            return k
    raise ValueError('Reached max number of iterations without finding solution.')


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle13.txt', 'r') as input:
            with open('sols/puzzle13.txt', 'w') as f:
                f.write(str(firewall_severity(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle13.txt', 'r') as input:
            with open('sols/puzzle13b.txt', 'w') as f:
                f.write(str(find_delay(input)))


