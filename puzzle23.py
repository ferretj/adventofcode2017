import sys
from cStringIO import StringIO
from collections import defaultdict


# PROBLEM 1
# we store register states in a dictionary and iteratively
# apply modifications encountered.
#
# instructions are represented by functions that are applied following
# the order and values defined in input
#
# we simply return the amount of mul instructions found
def count_mul(f, n_iter=10000000):

    # updates the register, number of mul and cursor after applying next instruction
    def update(reg, nmul, curr, ops, args1, args2, hval):

        # returns value or register value depending on the nature
        # of the input string
        def retrieve_val(arg, reg):
            if not arg.isdigit() and not '-' in arg:
                arg = reg[arg]
            return int(arg)

        # retrieve next instruction parameters
        op = ops[curr]
        arg1 = args1[curr]
        arg2 = args2[curr]
        curr += 1

        # apply instruction
        if op == 'set':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] = arg2
        elif op == 'sub':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] -= arg2
        elif op == 'mul':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] *= arg2
            nmul += 1
        elif op == 'jnz':
            arg1 = retrieve_val(arg1, reg)
            arg2 = retrieve_val(arg2, reg)
            # only apply if first arg is nonzero
            if arg1 != 0:
                curr += arg2 - 1
        else:
            raise ValueError('Unknown operation : {}'.format(op))

        # stop if reaching either end of instruction list
        npg = len(ops)
        if curr >= npg or curr < 0:
            stop = True

        return reg, nmul, curr, stop

    nmul = 0
    # parse input
    ops = []
    args1 = []
    args2 = []
    for line in f.readlines():
        line = line.rstrip('\n')
        elems = line.split()
        ops.append(elems[0])
        args1.append(elems[1])
        if len(elems) == 3:
            args2.append(elems[2])
        else:
            args2.append(None)
    # sequentially eval operations
    for i in xrange(n_iter):
        reg, nmul, curr, stop = update(reg, nmul, curr, ops, args1, args2)
        # stop and return latest frequency at first rcv instruction
        if stop:
            return nmul
    raise ValueError('Reached max number of iterations without stopping.')


# PROBLEM 2
# for problem 2 I wrote an optimized function mimicking
# the behaviour of the set of instructions, getting rid
# of unnecessary loops
#
# here is the result based on my input (DOES NOT work for other inputs)
def calc_h(n_iter=10000000):
    b = 108400
    c = b + 17000
    cpt = 0
    h = 0
    while c != b:
        if cpt != 0:
            b += 17
        f = 1
        
        for d in range(2, b):
            if b % d == 0 and b >= min(2*d, b*d) and b <= max(2*d, b*d):
                f = 0
        d = b

        e = b
        if f == 0:
            h += 1
        cpt += 1

    return h


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('sols/puzzle23.txt', 'r') as f:
            with open('data/puzzle23.txt', 'r') as input:
                f.write(str(count_mul(input)))
    if int(sys.argv[1]) == 0:
        with open('sols/puzzle23b.txt', 'r') as f:
            with open('data/puzzle23.txt', 'r') as input:
                f.write(str(calc_h(input)))