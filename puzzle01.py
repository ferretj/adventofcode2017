import sys

def solve_captcha_next(capt):
    cdelta = capt[1:] + capt[0]
    cpt = 0
    for c, cd in zip(capt, cdelta):
        if c == cd:
            cpt += int(c)
    return cpt


def solve_captcha_halfway(capt):
    h = len(capt) // 2
    cdelta = capt[h:] + capt[:h]
    cpt = 0
    for c, cd in zip(capt, cdelta):
        if c == cd:
            cpt += int(c)
    return cpt


if __name__ == '__main__':
    if int(sys.argv[1]) == 0:
        capt = open('data/puzzle01.txt', 'r').next()
        with open('sols/puzzle01.txt', 'w') as f:
            f.write(str(solve_captcha_next(capt)))
    elif int(sys.argv[1]) == 1:
        capt = open('data/puzzle01.txt', 'r').next()
        with open('sols/puzzle01b.txt', 'w') as f:
            f.write(str(solve_captcha_halfway(capt)))