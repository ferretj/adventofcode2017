import sys


# the solution consists in checking that each line
# contains the same number of elements than its set
# (which by design does not store redundant versions of elements)
def check_passphrases(f):
    n_valid = 0
    for line in f.readlines():
        words = line.rstrip('\n').split()
        if len(words) == len(list(set(words))):
            n_valid += 1
    return n_valid


# the solution is the same than for the above
# except that each word is converted to a hash
# that is constituted of each of its letters followed
# by its count in the word
# e.g. 'aeaea' -> 'a3e2'
# this allows to spot the potential anagrams since
# anagrams will produce the same hash 
def check_passphrases_anagrams(f):

    # hash function producing similar hashes for anagrams
    def anagram_hash(w):
        d = {}
        for c in w:
            d[c] = d.get(c, 0) + 1
        chars = list(d.keys())
        chars.sort()
        h = ''
        for char in chars:
            h += char + str(d[char])
        return h

    n_valid = 0
    for line in f.readlines():
        words = line.rstrip('\n').split()
        hashes = [anagram_hash(w) for w in words]
        if len(hashes) == len(list(set(hashes))):
            n_valid += 1
    return n_valid


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        with open('data/puzzle04.txt', 'r') as input:
            with open('sols/puzzle04.txt', 'w') as f:
                f.write(str(check_passphrases(input)))
    elif int(sys.argv[1]) == 1:
        with open('data/puzzle04.txt', 'r') as input:
            with open('sols/puzzle04b.txt', 'w') as f:
                f.write(str(check_passphrases_anagrams(input)))