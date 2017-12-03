import sys


# the function simply parses the input
# into lists of ints and substract the
# max and min of each list
def spreadsheet_checksum(f):
    lines = f.readlines()
    cpt = 0
    for line in lines:
        digits = [int(d) for d in line.split()]
        cpt += max(digits) - min(digits)
    return cpt


# first version of function to solve version b of problem
# (see below for smarter function)
#
# parses the input into lists of ints and
# for each element of the list checks divisions wrt to
# all remaining elements
def spreadsheet_checksum_evendiv_v1(f):

    def search_evendiv(digits, d, i, nd):
        for dj in digits[i + 1: nd]:
            if d % dj == 0:
                return d // dj
            elif dj % d == 0:
                return dj // d
        return None

    lines = f.readlines()
    cpt = 0
    for line in lines:
        curr = 0
        digits = [int(d) for d in line.split()]
        nd = len(digits)
        for i, d in enumerate(digits):
            ediv = search_evendiv(digits, d, i, nd)
            if ediv is not None: 
                cpt += ediv
                break
    return cpt


# parses the input into sorted lists of ints and
# for each element of the sorted list checks divisions wrt to
# all remaining elements
#
# checks that the following value is not equal to itself
#
# stops if a value that is smaller than twice its value is found
# (for efficiency)
def spreadsheet_checksum_evendiv_v2(f):

    def search_evendiv(digits, d, i, nd):
        if digits[i + 1] == d:
            return 1
        for dj in digits[nd: i: -1]:
            if dj % d == 0:
                return dj // d
            elif dj < 2 * d:
                break
        return None

    lines = f.readlines()
    cpt = 0
    for line in lines:
        curr = 0
        digits = [int(d) for d in line.split()]
        digits.sort()
        nd = len(digits)
        for i, d in enumerate(digits):
            ediv = search_evendiv(digits, d, i, nd)
            if ediv is not None: 
                cpt += ediv
                break
    return cpt


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle02.txt', 'r') as sheet:
            with open('sols/puzzle02.txt', 'w') as f:
                f.write(str(spreadsheet_checksum(sheet)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle02.txt', 'r') as sheet:
            with open('sols/puzzle02b.txt', 'w') as f:
                f.write(str(spreadsheet_checksum_evendiv_v2(sheet)))
