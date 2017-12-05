import sys


# here it simply jumps through the list according to the values found
# and updates the list until the cursor reaches the end of the list
#
# depending on the input the default number of iterations could not be sufficient
def twisty_trampoline_steps(f, n_iter=10000000):
    seq = [int(s.rstrip('\n')) for s in f.readlines()]
    n = len(seq)
    nsteps = 0
    curr = 0
    for _ in xrange(n_iter):
        nsteps += 1
        new_curr = max(0, curr + seq[curr])
        if new_curr > n - 1:
            return nsteps
        seq[curr] += 1
        curr = new_curr
    raise ValueError('Reached max number of iterations without finding exit.')


# same as above with a distinction on the values encountered for the update
#
# depending on the input the default number of iterations could not be sufficient
#
# increased it because the old one was not enough for my input
def twisty_trampoline_steps_3m(f, n_iter=100000000):
    seq = [int(s.rstrip('\n')) for s in f.readlines()]
    n = len(seq)
    nsteps = 0
    curr = 0
    for _ in xrange(n_iter):
        nsteps += 1
        new_curr = max(0, curr + seq[curr])
        if new_curr > n - 1:
            return nsteps
        if seq[curr] > 2:
            seq[curr] -= 1
        else:
            seq[curr] += 1
        curr = new_curr
    raise ValueError('Reached max number of iterations without finding exit.')


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle05.txt', 'r') as input:
            with open('sols/puzzle05.txt', 'w') as f:
                f.write(str(twisty_trampoline_steps(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle05.txt', 'r') as input:
            with open('sols/puzzle05b.txt', 'w') as f:
                f.write(str(twisty_trampoline_steps_3m(input)))
