import sys
import cStringIO


# retrieves starting and ending character indices
# for the first highest level group of a character
# sequence
def find_group_indices(seq):
    n = len(seq)
    if n == 0:
        return None, None

    start = None
    curr = 0
    cpt_b1 = 0
    cpt_b2 = 0
    is_garbage = False

    for _ in xrange(n + 1):
        
        try:
            char = seq[curr]
        except IndexError:
            return None, None
        
        if char == '!':
            curr += 1
        elif is_garbage:
            if char == '>':
                is_garbage = False
        else:
            if char == '{':
                if start is None:
                    start = curr
                cpt_b1 += 1
            elif char == '}' and start is not None:
                cpt_b2 += 1
                if cpt_b1 == cpt_b2:
                    return start, curr
            elif char == '<':
                is_garbage = True
        
        curr += 1


# PROBLEM 1
# the idea is to recursively count groups in sequence,
# starting from the highest level group and all subgroups
def stream_group_score(stream, level=1, n_iter=1000):

    # processing input to a list of characters
    if isinstance(stream, file):
        seq = list(stream.next())
    elif isinstance(stream, cStringIO.InputType):
        seq = list(stream.next())
    elif isinstance(stream, str):
        seq = list(stream)
    elif isinstance(stream, list):
        seq = stream
    else:
        raise TypeError('Wrong type : {}'.format(type(stream)))
    
    level_score = 0
    for _ in xrange(n_iter):
        # find indices of first highest level group of sequence
        start, end = find_group_indices(seq)
        # if no group is found, stop
        # else repeat process for the contents of the group found
        if start is None:
            break
        else:
            # increase global count according to group level
            level_score += level
            # score subgroups of group
            subseq = seq[start + 1: end]
            level_score += stream_group_score(subseq, level + 1)

        # process other groups starting from the end of previous
        # highest level group
        seq = seq[end + 1:]

    return level_score


# counts garbage characters before first group in a sequence
#
# addtionally : 
# retrieves starting and ending character indices
# for the first highest level group of a character
# sequence
def garbage_count_before_group(seq):
    n = len(seq)
    if n == 0:
        return None, None, 0

    start = None
    curr = 0
    cpt_b1 = 0
    cpt_b2 = 0
    cpt_g = 0
    is_garbage = False

    for _ in xrange(n + 1):
        
        try:
            char = seq[curr]
        except IndexError:
            return None, None, cpt_g
        
        if char == '!':
            curr += 1
        elif is_garbage:
            if char == '>':
                is_garbage = False
            elif start is None:
                cpt_g += 1
        else:
            if char == '{':
                if start is None:
                    start = curr
                cpt_b1 += 1
            elif char == '}' and start is not None:
                cpt_b2 += 1
                if cpt_b1 == cpt_b2:
                    return start, curr, cpt_g
            elif char == '<':
                is_garbage = True
        
        curr += 1


# PROBLEM 2
# the idea is to recursively count garbage characters in groups,
# starting from the highest level group and all subgroups
#
# one key point is to pay attention not to count several times
# garbage elements in the recursive structure. To do that, I 
# chose to only count garbage that precedes a group structure
# in a group content.
def stream_garbage_count(stream, n_iter=1000):

    # processing input to a list of characters
    if isinstance(stream, file):
        seq = list(stream.next())
    elif isinstance(stream, cStringIO.InputType):
        seq = list(stream.next())
    elif isinstance(stream, str):
        seq = list(stream)
    elif isinstance(stream, list):
        seq = stream
    else:
        raise TypeError('Wrong type : {}'.format(type(stream)))
    
    level_garbage = 0
    for _ in xrange(n_iter):
        # find indices of first highest level group of sequence
        # also count hypothetical garbage characters before it
        start, end, cpt_g = garbage_count_before_group(seq)
        level_garbage += cpt_g
        # if no group is found, stop
        # else repeat process for the contents of the group found
        if start is None:
            break
        else:
            subseq = seq[start + 1: end]
            # count garbage characters in subgroups of group
            level_garbage += stream_garbage_count(subseq)

        # process other groups starting from the end of previous
        # highest level group
        seq = seq[end + 1:]

    return level_garbage


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle09.txt', 'r') as input:
            with open('sols/puzzle09.txt', 'w') as f:
                f.write(str(stream_group_score(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle09.txt', 'r') as input:
            with open('sols/puzzle09b.txt', 'w') as f:
                f.write(str(stream_garbage_count(input)))