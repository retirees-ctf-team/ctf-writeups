import random


def unshuffle(seed: int, shuffled: bytes):
    random.seed(seed)
    shuffled = bytearray(shuffled)
    flag = ['_' for _ in range(len(shuffled))]

    mapp = [i for i in range(len(shuffled))]
    random.shuffle(mapp)

    for i in range(len(mapp)):
        flag[mapp[i]] = chr(shuffled[i])

    return "".join(flag)


# print(unshuffle(3723664, b'DrgnS}EFLRKAGBMNQIHOCD{PJ'))
