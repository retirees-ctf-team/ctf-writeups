from pwn import *


def xor(a, b):
    return bytes(aa ^ bb for aa, bb in zip(a, b))


r = remote('babymac.hackable.software', 1337)
# r = remote('localhost', 1234)

m = (b'\x10' * 16).hex()
print(r.sendlineafter(b'> ', b'sign').decode(), 'sign')
print(r.sendlineafter(b'> ', b''), '')
t = bytes.fromhex(r.recvline().decode().strip())[:16]
print("t is : ", t.hex())

m_pream = (b'gimme flag' + b'\x00' * 6).hex()
print(r.sendlineafter(b'> ', b'sign').decode(), 'sign')
sg = xor(bytes.fromhex(m_pream), t)
print(r.sendlineafter(b'> ', sg.hex().encode()).decode(), sg.hex())
t_pream = bytes.fromhex(r.recvline().decode().strip())[:16]
print("t_pream is : ", t_pream.hex())


payload = (t_pream + bytes.fromhex(m) + b'\x00' * 16 + bytes.fromhex(m_pream)).hex()
print(r.sendlineafter(b'> ', b'verify').decode(), 'verify')
print(r.sendlineafter(b'> ', payload.encode()).decode(), payload)
r.interactive()
