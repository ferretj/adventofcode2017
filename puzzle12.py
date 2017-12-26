from copy import copy
import sys


# PROBLEM 1
# the solution consists in recursively scanning the connections of new programs
# 
# we start with 0, find its direct connections, add 0 to a set so that we don't perform useless lookups.
# Then we apply the same process to its direct connections.
#
# we stop when the set containing scanned programs doesn't evolve anymore 
def zero_connected_programs(f, n_iter=100):
    # parse input and get program connections
    lines = [line.rstrip('\n').replace(',', '').split() for line in f.readlines()]
    links = {int(line[0]): [int(l) for l in line[2:]] for line in lines} 
    # recursively add programs that have a connection to 0
    #
    # start with a set containing only 0
    pgs = set([0])
    pgs_upd = copy(pgs)
    pgs_scanned = set()
    # recursively add the programs connected to 0 to pgs_upd
    for _ in xrange(n_iter):
        n = len(pgs)
        for pg in pgs:
            # only perform a lookup on unseen programs
            if pg not in pgs_scanned:
                ls = links[pg]
                # since pg is connected to 0
                # its connections are shared with 0 
                pgs_upd.update(ls)
                # pg is considered scanned
                pgs_scanned.update([pg])
        pgs = copy(pgs_upd)
        if len(pgs) == n:
            return n
    raise ValueError('Reached max number of iterations without converging.')


# PROBLEM 2
# we take each input line as groups of connected programs
#
# we then proceed to merge all the overlapping groups until convergence
def program_groups(f, n_iter=100):

    # function that merges all lists with shared elements (in a list)
    def fusion_overlapping_groups(pgs, n_iter):

        def are_overlapping(gp1, gp2):
            inter = set(gp1) & set(gp2)
            if len(inter) != 0:
                return True
            return False

        # taking sets to avoid useless repetitions
        sets = [set(pg) for pg in pgs]
        
        # process must be applied until all lists are independent
        for _ in xrange(n_iter):
            n = len(sets)
            i = 0
            j = 1
            max_iter = n * (n - 1) // 2
            # we check all pairs of sets for intersection
            #
            # overlapping sets are merged
            for k in xrange(max_iter):
                pg1 = sets[i]
                pg2 = sets[j]
                if are_overlapping(pg1, pg2):
                    sets[i] = sets[i] | sets[j]
                    del sets[j]
                else:
                    j += 1

                if j == len(sets):
                    i += 1
                    j = i + 1
                if i >= len(sets) - 1:
                    break

            # stopping criterion
            t1 = sum([len(pg) for pg in sets])
            t2 = len(set.union(*sets))
            if t1 == t2:
                return sets
        raise ValueError('Reached max number of iterations...')

    # parse input and get program connections
    lines = [line.rstrip('\n').replace(',', '').split() for line in f.readlines()]
    links = {int(line[0]): [int(l) for l in line[2:]] for line in lines}
    # init groups as programs + connections
    groups = [[k] + v for k, v in links.iteritems()]
    # fusion groups that have overlapping items
    groups = fusion_overlapping_groups(groups, n_iter)
    return len(groups)


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle12.txt', 'r') as input:
            with open('sols/puzzle12.txt', 'w') as f:
                f.write(str(zero_connected_programs(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle12.txt', 'r') as input:
            with open('sols/puzzle12b.txt', 'w') as f:
                f.write(str(program_groups(input)))


