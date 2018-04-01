import sys
from cStringIO import StringIO
import numpy as np


class Tape(object):

    def __init__(self):
        self.array = np.zeros(8)
        self.h = 4

    def __len__(self):
        return len(self.array)

    def __getitem__(self, k):
        if (k + self.h < 0) or (k + self.h > len(self) - 1):
            self._double_array()
        return self.array[k + self.h]

    def __setitem__(self, k, val):
        if (k + self.h < 0) or (k + self.h > len(self) - 1):
            self._double_array()
        self.array[k + self.h] = val

    @property
    def checksum(self):
        return int(self.array.sum())

    def _double_array(self):
        new_array = np.zeros(2 * len(self))
        new_array[self.h: 3 * self.h] = self.array
        self.array = new_array
        self.h *= 2


# PROBLEM 1
# once the complexity lying in parsing the input ruled out,
# the problem can be solved by applying all state rules.
# A dictionary keeps track of the rules while the Turing machine
# tape is a custom data structure wrapped around a numpy array
# that is resized each time its bounds are reached
def turing_steps(f):
    state_rules = dict()
    # parse input
    for i, line in enumerate(f.readlines()):
        line = line.lstrip()
        line = line.rstrip('\n')
        # get starting state
        if i == 0:
            start_state = line.split('state ')[1].rstrip('.')
        # get amount of steps before checksum
        elif i == 1:
            n_steps = int(line.split('after ')[1].split(' steps')[0])
        # iteratively build all state rules
        else:
            if line.startswith('In state'):
                curr_state = line.split('In state ')[1].split(':')[0]
                state_rules[curr_state] = dict()
            elif line.startswith('If the current value'):
                curr_val = int(line.split('is ')[1].split(':')[0])
                state_rules[curr_state][curr_val] = dict()
            elif line.startswith('-'):
                if 'Write' in line:
                    val = int(line.split('value ')[1].split('.')[0])
                    state_rules[curr_state][curr_val]['write'] = val
                elif 'Move' in line:
                    move = line.split('the ')[1].split('.')[0]
                    state_rules[curr_state][curr_val]['move'] = move
                elif 'Continue' in line:
                    state = line.split('state ')[1].split('.')[0]
                    state_rules[curr_state][curr_val]['next_state'] = state
    # check
    print 'State rules :'
    print state_rules
    # loop on states until reaching checksum time
    state = start_state
    pos = 0
    tape = Tape()
    for _ in xrange(n_steps):
        val = tape[pos]
        # overwrite value
        tape[pos] = state_rules[state][val]['write']
        # move on tape
        if state_rules[state][val]['move'] == 'right':
            pos += 1
        else:
            pos -= 1
        # update state
        state = state_rules[state][val]['next_state']
    return tape.checksum


if __name__ == '__main__':

    if int(sys.argv[1]) == 0:
        with open('sols/puzzle25.txt', 'w') as f:
            with open('data/puzzle25.txt', 'r') as input:
                f.write(str(turing_steps(input)))
