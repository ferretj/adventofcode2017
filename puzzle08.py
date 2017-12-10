import sys


# FIRST PROBLEM
# the solution consists in updating a dictionary
# whose keys are variable names according to
# parsed instructions, and returning the max value
def largest_register_value(f):
    vdict = dict()
    for line in f.readlines():
        elems = line.rstrip('\n').split()
        
        a1 = elems[0]
        a2 = elems[4]
        
        if elems[1] == 'inc':
            sign = 1
        else:
            sign = -1
        incr = sign * int(elems[2])
        
        cond_op = elems[5]
        cond_val = int(elems[6])

        if cond_op == '==':
            cond = (vdict.get(a2, 0) == cond_val)
        elif cond_op == '>':
            cond = (vdict.get(a2, 0) > cond_val)
        elif cond_op == '>=':
            cond = (vdict.get(a2, 0) >= cond_val)
        elif cond_op == '<':
            cond = (vdict.get(a2, 0) < cond_val)
        elif cond_op == '<=':
            cond = (vdict.get(a2, 0) <= cond_val)
        else:
            cond = (vdict.get(a2, 0) != cond_val)

        if cond:
            vdict[a1] = vdict.get(a1, 0) + incr

    return max(list(vdict.values()))


# SECOND PROBLEM
# same as above, with the addition of an extra
# variable to store and update maximum register value
def largest_intermediate_register_value(f):
    vdict = dict()
    lval = 0
    for line in f.readlines():
        elems = line.rstrip('\n').split()
        
        a1 = elems[0]
        a2 = elems[4]
        
        if elems[1] == 'inc':
            sign = 1
        else:
            sign = -1
        incr = sign * int(elems[2])
        
        cond_op = elems[5]
        cond_val = int(elems[6])

        if cond_op == '==':
            cond = (vdict.get(a2, 0) == cond_val)
        elif cond_op == '>':
            cond = (vdict.get(a2, 0) > cond_val)
        elif cond_op == '>=':
            cond = (vdict.get(a2, 0) >= cond_val)
        elif cond_op == '<':
            cond = (vdict.get(a2, 0) < cond_val)
        elif cond_op == '<=':
            cond = (vdict.get(a2, 0) <= cond_val)
        else:
            cond = (vdict.get(a2, 0) != cond_val)

        if cond:
            val = vdict.get(a1, 0) + incr
            vdict[a1] = val
            if val > lval:
                lval = val

    return lval


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle08.txt', 'r') as input:
            with open('sols/puzzle08.txt', 'w') as f:
                f.write(str(largest_register_value(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle08.txt', 'r') as input:
            with open('sols/puzzle08b.txt', 'w') as f:
                f.write(str(largest_intermediate_register_value(input)))