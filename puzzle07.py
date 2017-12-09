import sys
from copy import copy


# FIRST PROBLEM
# the key idea is that the bottom program is the only
# one that is not listed among children of other programs
#
# the method consists in browsing through the whole input
# and save all programs in one list, children programs
# in another list, and return the only element outside
# the intersection
def find_bottom_program(f):
    pg1 = []  # all programs
    pg2 = []  # children programs
    
    for line in f.readlines():
        elems = line.rstrip('\n').split()
        
        # saving all programs
        bp = elems[0]
        pg1.append(bp)

        # saving children
        if len(elems) > 2:
            hps = [elem.rstrip(',') for elem in elems[3:]]
            pg2.extend(hps)

    pg1 = set(pg1)
    pg2 = set(pg2)
    
    # return the only element outside intersection
    return (pg1 - pg2).pop()


# SECOND PROBLEM
# here we have to browse recursively through the program tree
# to calculate subtower total weights and identify the faulty node
# 
# first we reuse the solution above to get the tree root node
#
# then we use depth-first search with accumulation to calculate
# each subtree total weight. We save the first child node found
# whose subtree weight is different from its siblings, and the
# difference between the subtree weights
def balance_weight(f, debug=False):

    # finds index of only different element in list
    def diff_elem_index(l):
        cpt = -1
        s = []
        for _ in xrange(len(l)):
            p = l.pop()
            s = list(set(s))
            if p not in l and p not in s:
                return cpt
            else:
                cpt -= 1
                s.append(p)

    def tower_search_depth_first(bottom, pg_children, pg_weights, acc=[], debug=False):
        cs = pg_children[bottom]
        w = pg_weights[bottom]
        if len(cs) == 0:
            return w
        else:
            cws = [tower_search_depth_first(c, pg_children, pg_weights, acc, debug) for c in cs]
            if len(set(cws)) > 1 and len(acc) == 0:
                i = diff_elem_index(copy(cws))
                acc.append((cs[i], cws[i + 1] - cws[i]))
                if debug:
                    print 'b : ', bottom
                    print 'cs : ', cs
                    print 'cws : ', cws
                    print 'diff elem index : ', i
                    print 'faulty child : ', cs[i]
            return w + sum(cws)

    # reusing first problem solution to compute bottom program
    pg_weights = dict()
    pg_children = dict()
    pg_parents = dict()
    pg1 = []
    pg2 = []

    for line in f.readlines():
        elems = line.rstrip('\n').split()
        bp = elems[0]
        w = int(elems[1].strip('()'))
        pg1.append(bp)
        pg_weights[bp] = w
        if len(elems) > 2:
            hps = [elem.rstrip(',') for elem in elems[3:]]
            pg2.extend(hps)
            pg_children[bp] = hps
            for hp in hps:
                pg_parents[hp] = bp
        else:
            pg2.append(bp)
            pg_children[bp] = []
    pg1 = set(pg1)
    pg2 = set(pg2)
    bottom = (pg1 - pg2).pop()

    # depth-first tree traversal with accumulation
    acc = []
    tower_search_depth_first(bottom, pg_children, pg_weights, acc)
    faulty, offset = acc[0]
    if debug:
        print 'faulty : ', faulty
        print 'faulty weight : ', pg_weights[faulty]
        print 'faulty correction : ', offset
    return pg_weights[faulty] + offset


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle07.txt', 'r') as input:
            with open('sols/puzzle07.txt', 'w') as f:
                f.write(str(find_bottom_program(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle07.txt', 'r') as input:
            with open('sols/puzzle07b.txt', 'w') as f:
                f.write(str(balance_weight(input)))
