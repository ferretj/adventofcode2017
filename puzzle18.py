import sys
from cStringIO import StringIO
from collections import defaultdict


# PROBLEM 1
# we store register states in a dictionary and overwrite a
# frequency variable each time a sound is played
#
# instructions are represented by functions that are applied following
# the order and values defined in input
#
# we simply return the freq variable at the first rcv instruction
def recover_freq(f, n_iter=100000):

    # updates the register, frequency and cursor after applying next instruction
    def update(reg, freq, curr, ops, args1, args2):

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
        stop = False
        
        # apply instruction
        if op == 'set':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] = arg2
        elif op == 'add':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] += arg2
        elif op == 'mul':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] *= arg2
        elif op == 'mod':
            arg2 = retrieve_val(arg2, reg)
            reg[arg1] = reg[arg1] % arg2
        elif op == 'snd':
            arg1 = retrieve_val(arg1, reg)
            freq = arg1
        elif op == 'rcv':
            arg1 = retrieve_val(arg1, reg)
            # only apply if first arg is nonzero
            if arg1 != 0: 
                stop = True
        elif op == 'jgz':
            arg1 = retrieve_val(arg1, reg)
            arg2 = retrieve_val(arg2, reg)
            # only apply if first arg is strictly positive
            if arg1 > 0: 
                curr += arg2 - 1
        else:
            raise ValueError('Unknown operation : {}'.format(op))

        # stop if reaching either end of instruction list
        npg = len(ops)
        if curr >= npg or curr < 0:
            stop = True

        return reg, freq, curr, stop

    reg = defaultdict(int)
    freq = None
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
    curr = 0
    for i in xrange(n_iter):
        reg, freq, curr, stop = update(reg, freq, curr, ops, args1, args2)
        # stop and return latest frequency at first rcv instruction
        if stop:
            return freq
    raise ValueError('Exceeded max number of iterations without finding rcv instruction.')


# PROBLEM 2
# the above script is slightly modified : register, cursor are duplicated
# and buffers are added for communication between both programs
#
# as before, we sequentially apply the instructions in the list until a rcv
# instruction on an empty buffer is called, at which point we go on to the second
# program and only stop when both programs are locked 
def duet(f, n_iter=10000000):

    def inverse(p):
        if p == 0:
            return 1
        return 0

    # updates the registers, buffers and cursors after applying next instruction
    def update(regs, buffs, currs, ops, args1, args2, p, cpt):

        # returns value or register value depending on the nature
        # of the input string
        def retrieve_val(arg, regs, p):
            if not arg.isdigit() and not '-' in arg:
                arg = regs[p][arg]
            return int(arg)

        # recv instruction
        def receive_val(arg, regs, buffs, p):
            pinv = inverse(p)
            print 'pinv : ', pinv
            buff = buffs[pinv]
            stop = False
            print buff
            print len(buff)
            if len(buff) == 0:
                stop = True
            else:
                val = buff.pop()
                regs[p][arg] = val
            return buffs, stop

        # snd instruction
        def send_val(val, buffs, p, cpt):
            buffs[p].insert(0, val)
            if p == 1:
                cpt += 1
            return buffs, cpt

        # retrieve next instruction parameters
        op = ops[currs[p]]
        arg1 = args1[currs[p]]
        arg2 = args2[currs[p]]
        currs[p] += 1
        stop = False

        # apply instruction
        if op == 'set':
            arg2 = retrieve_val(arg2, regs, p)
            regs[p][arg1] = arg2
        elif op == 'add':
            arg2 = retrieve_val(arg2, regs, p)
            regs[p][arg1] += arg2
        elif op == 'mul':
            arg2 = retrieve_val(arg2, regs, p)
            regs[p][arg1] *= arg2
        elif op == 'mod':
            arg2 = retrieve_val(arg2, regs, p)
            regs[p][arg1] = regs[p][arg1] % arg2
        elif op == 'snd':
            arg1 = retrieve_val(arg1, regs, p)
            buffs, cpt = send_val(arg1, buffs, p, cpt)
        elif op == 'rcv':
            buffs, stop = receive_val(arg1, regs, buffs, p)
            if stop:
                currs[p] -= 1
        elif op == 'jgz':
            arg1 = retrieve_val(arg1, regs, p)
            arg2 = retrieve_val(arg2, regs, p)
            if arg1 > 0: 
                currs[p] += arg2 - 1
        else:
            raise ValueError('Unknown operation : {}'.format(op))

        return regs, buffs, currs, stop, cpt

    regs = [defaultdict(int) for _ in xrange(2)]
    regs[1]['p'] = 1
    buffs = [[] for _ in xrange(2)]
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
    cpt = 0
    p = 0
    currs = [0] * 2
    fstp = False
    for i in xrange(n_iter):
        regs, buffs, currs, stop, cpt = update(regs, buffs, currs, ops, args1, args2, p, cpt)
        if stop:
            # stop when both programs are deadlocked
            if fstp:
                return cpt
            else:
                p = inverse(p)
                fstp = True
        else:
            fstp = False
    raise ValueError('Exceeded max number of iterations without finding rcv instruction.')



if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('data/puzzle18.txt', 'r') as input:
            with open('sols/puzzle18.txt', 'w') as f:
                f.write(str(recover_freq(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle18.txt', 'r') as input:
            with open('sols/puzzle18b.txt', 'w') as f:
                f.write(str(duet(input)))

