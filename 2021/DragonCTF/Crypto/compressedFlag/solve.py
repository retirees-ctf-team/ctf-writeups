from pwn import *
from string import ascii_uppercase
from unShuffle import unshuffle

# r = remote('compresstheflag.hackable.software', 1337)
r = remote('localhost', 1337)

print(r.recvuntil(b'DrgnS{[A-Z]+}\n').decode())

seed = '3723664'
shuffled_flag = "DrgnS"

while len(shuffled_flag) < 25:
    min_zlib = 100000
    best_payload = ""
    for i in ascii_uppercase + '{}':
        payload = seed + ':' + shuffled_flag + i
        print(payload)
        r.sendline(payload.encode())
        r.recvuntil(b'zlib')
        zlib = int(r.recvline().decode().strip())
        r.recvline()
        if zlib < min_zlib:
            best_payload = i
            min_zlib = zlib
    shuffled_flag += best_payload

print("\nShuffled Flag: ", shuffled_flag)
print("Unshuffled flag:", unshuffle(int(seed), shuffled_flag.encode()))
