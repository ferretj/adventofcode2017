import sys
from cStringIO import StringIO
from collections import defaultdict
from copy import copy


# PROBLEM 1
# Stores a list of all compatible components
# for each of them and recursively build all the
# bridges possible.
# The highest sum of parts is returned.
def strongest_bridge(f):
    comps = []
    # parse input
    for line in f.readlines():
        line = line.rstrip('\n')
        port1, port2 = line.split('/')
        comps.append((int(port1), int(port2)))
    # evaluate and keep track of compatible components
    # for each of them
    compat_l = defaultdict(list)
    compat_r = defaultdict(list)
    for i, left in enumerate(comps):
        port_l = left[0]
        port_r = left[1]
        for j, right in enumerate(comps):
            if i == j:
                continue
            if right[0] == port_l or right[1] == port_l:
                compat_l[i].append(j)
            if right[0] == port_r or right[1] == port_r:
                compat_r[i].append(j)
    # do the same for the starting component 0/0
    for j, right in enumerate(comps):
        if right[0] == 0:
            compat_l[-1].append(j)
        if right[1] == 0:
            compat_r[-1].append(j)
    # try all combinations possible
    # and return strongest one
    n_comps = len(comps)
    bridges = []
    strengths = []
    fill_bridges(comps, range(n_comps), (0, 0), -1, 'right', compat_l, compat_r, bridges, strengths)
    bridges2 = []
    strengths2 = []
    fill_bridges(comps, range(n_comps), (0, 0), -1, 'left', compat_l, compat_r, bridges2, strengths2)
    bridges.extend(bridges2)
    strengths.extend(strengths2)
    return max(strengths)


# PROBLEM 2
# Stores a list of all compatible components
# for each of them and recursively build all the
# bridges possible.
# The longest bridge (with highest sum of components if there is a draw)
# is returned.
def longest_bridge(f):
    comps = []
    # parse input
    for line in f.readlines():
        line = line.rstrip('\n')
        port1, port2 = line.split('/')
        comps.append((int(port1), int(port2)))
    # evaluate and keep track of compatible components
    # for each of them
    compat_l = defaultdict(list)
    compat_r = defaultdict(list)
    for i, left in enumerate(comps):
        port_l = left[0]
        port_r = left[1]
        for j, right in enumerate(comps):
            if i == j:
                continue
            if right[0] == port_l or right[1] == port_l:
                compat_l[i].append(j)
            if right[0] == port_r or right[1] == port_r:
                compat_r[i].append(j)
    # do the same for the starting component 0/0
    for j, right in enumerate(comps):
        if right[0] == 0:
            compat_l[-1].append(j)
        if right[1] == 0:
            compat_r[-1].append(j)
    # try all combinations possible
    # and return strongest one
    n_comps = len(comps)
    bridges = []
    strengths = []
    lengths = []
    fill_bridges(comps, range(n_comps), (0, 0), -1, 'right', compat_l, compat_r, bridges, strengths, lengths)
    bridges2 = []
    strengths2 = []
    lengths2 = []
    fill_bridges(comps, range(n_comps), (0, 0), -1, 'left', compat_l, compat_r, bridges, strengths, lengths)
    bridges.extend(bridges2)
    strengths.extend(strengths2)
    lengths.extend(lengths2)
    # find longest (and strongest in case of draw) bridge
    ind = 0
    length = 0
    strength = 0
    for i, l in enumerate(lengths):
        if l == length:
            if strengths[i] > strength:
                ind = i
                length = l
                strength = strengths[i]
        elif l > length:
            ind = i
            length = l
            strength = strengths[i]
    return strength


def bridge_hash(comps):

    def comp_hash(comp):
        return '/'.join([str(port) for port in comp])

    return '--'.join([comp_hash(comp) for comp in comps])


def fill_bridges(comps, indices, curr, curr_ind, port, compat_l, compat_r, out, out2, out3=[]):
    print 'current : ', curr
    if port == 'left':
        compatible = [compat for compat in compat_l[curr_ind] if compat in indices]
        print 'compatible : ', compatible
        if not compatible:
            acc = [elem for elem in range(len(comps)) if elem not in indices]
            out.append(bridge_hash([comps[ind] for ind in acc]))
            out2.append(sum([comps[ind][0] + comps[ind][1] for ind in acc]))
            out3.append(len(acc))
        for c in compatible:
            indices_mod = copy(indices)
            indices_mod.remove(c)
            if comps[c][0] == curr[0]:
                fill_bridges(comps, indices_mod, comps[c], c, 'right', compat_l, compat_r, out, out2, out3)
            else:
                fill_bridges(comps, indices_mod, comps[c], c, 'left', compat_l, compat_r, out, out2, out3)
    elif port == 'right':
        compatible = [compat for compat in compat_r[curr_ind] if compat in indices]
        print 'compatible : ', compatible
        if not compatible:
            acc = [elem for elem in range(len(comps)) if elem not in indices]
            out.append(bridge_hash([comps[ind] for ind in acc]))
            out2.append(sum([comps[ind][0] + comps[ind][1] for ind in acc]))
            out3.append(len(acc))
        for c in compatible:
            indices_mod = copy(indices)
            indices_mod.remove(c)
            if comps[c][0] == curr[1]:
                fill_bridges(comps, indices_mod, comps[c], c, 'right', compat_l, compat_r, out, out2, out3)
            else:
                fill_bridges(comps, indices_mod, comps[c], c, 'left', compat_l, compat_r, out, out2, out3)


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('sols/puzzle24.txt', 'w') as f:
            with open('data/puzzle24.txt', 'r') as input:
                f.write(str(strongest_bridge(input)))
    if int(sys.argv[1]) == 1:
        with open('sols/puzzle24b.txt', 'w') as f:
            with open('data/puzzle24.txt', 'r') as input:
                f.write(str(longest_bridge(input)))
