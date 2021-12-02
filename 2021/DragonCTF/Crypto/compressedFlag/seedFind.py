import random

# make 25 character flag
flag_format = b"DrgnS{" + b"A" * 18 + b"}"

seed = 0
while True:
    flag_copy = bytearray(flag_format)
    random.seed(seed)
    random.shuffle(flag_copy)
    if flag_copy.startswith(b'DrgnS'):
        print("Seed:", seed)
        print("Shuffled:", flag_copy)
    seed += 1
